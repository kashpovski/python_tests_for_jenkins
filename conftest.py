import pytest
import logging
import datetime
import json
import allure
import os

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from browsermobproxy import Server, Client


PATH_LOGS_TEST = "logs/logs_tests/"
PATH_LOGS_BROWSER = "logs/logs_browser/"
PATH_LOGS_PROXY = "logs/logs_proxy/"

def pytest_addoption(parser):
    parser.addoption("--browser",
                     default="chrome",
                     choices=["chrome", "firefox", "MicrosoftEdge", "opera", "yandex"],
                     help="Browser to run tests")
    parser.addoption("--driver_path", default=r"D:\Mars\QA\tools\WebDrivers", help="Directory to the webdriver")
    parser.addoption("--url", default="http://192.168.31.185:8081/", help="Base url")
    parser.addoption("--headless", action="store_true", help="Browser in headless mode")
    parser.addoption("--fullscreen", action="store_true", help="Open browser in full-screen mode")
    parser.addoption("--log_level", default="DEBUG", help="Set log level")
    parser.addoption("--log_proxy", action="store_true", help="Open browser in log proxy")
    parser.addoption("--log_browser", action="store_true", help="Open browser in log browser")
    parser.addoption("--remote",
                     default="local",
                     choices=["selenium", "selenoid"],
                     help="Open browser in remote (selenium or selenoid)")
    parser.addoption("--remote_executor", default="192.168.31.185", help="Remote ip address")
    parser.addoption("--remote_platform_name", help="Selenium: Platform name for remote ran")
    parser.addoption("--remote_bv", help="Selenoid: change browser version (ex. 104.0)")
    parser.addoption("--remote_vnc", action="store_true", help="Selenoid: switch vnc")
    parser.addoption("--remote_video", action="store_true", help="Selenoid: switch recording video")
    parser.addoption("--remote_log", action="store_true", help="Selenoid: switch log")
    parser.addoption("--remote_name", help="Selenoid: name user")
    parser.addoption("--remote_sr", help="Selenoid: change screen resolution (ex. 1280x1024)")
    parser.addoption("--remote_mobile", help="Selenoid: mobile mod only Chrome browser (ex. 'iPhone 5/SE')")


@pytest.fixture
def proxy_server(request):
    log_proxy = request.config.getoption("--log_proxy")

    if log_proxy:
        server = Server(rf"{os.getcwd()}\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat",
                        {"port": 8082})
        server.start({"log_path": PATH_LOGS_PROXY})
        client = Client("localhost:8082")
        server.create_proxy()
        request.addfinalizer(client.close)
        request.addfinalizer(server.stop)
        client.new_har()  # Архив сетевой активнти браузера (список словарей)
        return client
    else:
        pass


@pytest.fixture
def browser(request, proxy_server):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    driver_path = request.config.getoption("--driver_path")
    url = request.config.getoption("--url")
    fullscreen = request.config.getoption("--fullscreen")
    log_level = request.config.getoption("--log_level")
    log_proxy = request.config.getoption("--log_proxy")
    log_browser = request.config.getoption("--log_browser")
    remote = request.config.getoption("--remote")
    remote_executor = request.config.getoption("--remote_executor")
    remote_platform_name = request.config.getoption("--remote_platform_name")
    remote_bv = request.config.getoption("--remote_bv")
    remote_vnc = request.config.getoption("--remote_vnc")
    remote_video = request.config.getoption("--remote_video")
    remote_log = request.config.getoption("--remote_log")
    remote_name = request.config.getoption("--remote_name")
    remote_sr = request.config.getoption("--remote_sr")
    remote_mobile = request.config.getoption("--remote_mobile")

    logger = logging.getLogger(request.node.name)
    file_handler = logging.FileHandler(f"{PATH_LOGS_TEST}{request.module.__name__}-{request.function.__name__}.log")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s %(funcName)s [%(module)s] | %(levelname)s :  %(message)s"))
    logger.addHandler(file_handler)

    start_time = datetime.datetime.now()
    logger.info("======== Test started ========")

    if browser_name == "chrome":
        _driver = webdriver.Chrome
        executable_path = driver_path + "\chromedriver"
        options = webdriver.ChromeOptions()
        capabilities = DesiredCapabilities.CHROME
    elif browser_name == "MicrosoftEdge":
        _driver = webdriver.Chrome
        executable_path = driver_path + "\msedgedriver"
        options = webdriver.EdgeOptions()
        capabilities = DesiredCapabilities.EDGE
    elif browser_name == "firefox":
        _driver = webdriver.Firefox
        executable_path = driver_path + "\geckodriver"
        options = webdriver.FirefoxOptions()
        capabilities = DesiredCapabilities.FIREFOX
    elif browser_name == "yandex":
        _driver = webdriver.Chrome
        executable_path = driver_path + "\yandexdriver"
        options = webdriver.ChromeOptions()
        capabilities = DesiredCapabilities.CHROME
    elif browser_name == "opera":
        _driver = webdriver.Chrome
        executable_path = driver_path + "\operadriver"
        options = None
        capabilities = {"browserName": browser_name}
    else:
        raise ValueError(f"Browser '{browser_name}' is not supported")

    if headless:
        options.headless = True
        logger.info("headless mode")
    if log_proxy:
        options.accept_insecure_certs = True
        proxy_server.add_to_webdriver_capabilities(capabilities)
        logger.info("log proxy on")
    if log_browser:
        capabilities['goog:loggingPrefs'] = {
            'browser': 'ALL',
            'performance': 'ALL',
        }
        logger.info("log browser on")

    if remote == "local":
        _browser = _driver(executable_path=executable_path,
                           options=options,
                           desired_capabilities=capabilities)
        logger.info("local started")

    else:
        if remote == "selenium":
            capabilities.update({"platformName": remote_platform_name})
            logger.info(f"remote mode (Selenium server: {remote_executor}, Platform name: {remote_platform_name})")
        elif remote == "selenoid":
            capabilities.update({
                "browserVersion": remote_bv,
                "acceptSslCerts": True,
                "acceptInsecureCerts": True,
                "selenoid:options": {
                    "screenResolution": remote_sr,
                    "name": remote_name,
                    "enableVNC": remote_vnc,
                    "enableVideo": remote_video,
                    "enableLog": remote_log,
                },
                # "timeZone": 'Europe/Moscow',
            })
            if remote_mobile:
                capabilities.update({"goog:chromeOptions": {"mobileEmulation": {"deviceName": remote_mobile}}})
            logger.info(f"remote mode (Selenoid: {remote_executor})")
        _browser = webdriver.Remote(command_executor=f"{remote_executor}:4444/wd/hub",
                                    desired_capabilities=capabilities,
                                    options=options)

    if fullscreen:
        _browser.maximize_window()
        logger.info("fullscreen mode")

    _browser.url = url
    _browser.test_file = request.function.__name__
    _browser.test_name = request.node.name
    _browser.log_level = log_level
    _browser.logger = logger
    _browser.proxy = proxy_server

    _browser.implicitly_wait(3)

    logger.info(f"Browser: {browser_name} ({_browser.session_id})")

    def dump_log_proxy_to_json(file_name, log_proxy):
        if log_proxy:
            har_log = _browser.proxy.har['log']
            logs = []
            with open(file_name, "w+") as f:
                for i, el in enumerate(har_log["entries"], start=1):
                    logs.append({i: {"request": el["request"], "response": el["response"]}})
                f.write(json.dumps(logs))
        else:
            pass

    def logs_browser(log_path, log_browser):
        if log_browser:
            # Логиирование производительности страницы
            performance_logs = []
            for line in _browser.get_log("performance"):
                performance_logs.append(line)
            with open(f"{log_path}_performance.json", "w+") as f:
                f.write(json.dumps(performance_logs))

            # Логи консоли браузера собирает WARNINGS, ERRORS
            browser_logs = []
            for line in _browser.get_log("browser"):
                browser_logs.append(line)
            with open(f"{log_path}_browser.json", "w+") as f:
                f.write(json.dumps(browser_logs))
        else:
            pass

    def fin():
        logs_browser(f"{PATH_LOGS_BROWSER}{request.module.__name__}-{request.function.__name__}",
                     log_browser)
        dump_log_proxy_to_json(f"{PATH_LOGS_PROXY}{request.module.__name__}-{request.function.__name__}_proxy.json",
                               log_proxy)
        # _browser.proxy.close()
        _browser.quit()
        logger.info(f"^^^^^^^^ Test finished. {datetime.datetime.now() - start_time} ^^^^^^^^")

    request.addfinalizer(fin)

    return _browser


@pytest.hookimpl()
def pytest_sessionstart():
    try:
        os.makedirs(PATH_LOGS_TEST)
        os.makedirs(PATH_LOGS_BROWSER)
        os.makedirs(PATH_LOGS_PROXY)
    except FileExistsError:
        pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()
    if result.when == "call" and result.failed:
        if "browser" in item.fixturenames:
            allure.attach(item.funcargs["browser"].get_screenshot_as_png(),
                          name="Test FAILED (screenshot error)",
                          attachment_type=allure.attachment_type.PNG)
            item.funcargs["browser"].logger.warning("Test FAILED (make screenshot error)")
