import allure
import pytest

from pages.AdminLoginPage import AdminLoginPage
from data_for_test import *


@allure.story("Page title")
@allure.title("Check title in login page")
def test_title(browser):
    AdminLoginPage(browser).open()
    assert AdminLoginPage(browser).get_title() == "Administration"


@allure.feature("Authorization")
def test_valid_login(browser):
    AdminLoginPage(browser).open()
    AdminLoginPage(browser).login(username_admin_login_page, password_admin_login_page)
    AdminLoginPage(browser).verify_login()


@allure.feature("Authorization")
def test_invalid_login_attempts(browser):
    AdminLoginPage(browser).open()
    username = get_userdata()
    password = get_userdata()
    for i in range(6):
        AdminLoginPage(browser).login(username, password)
    assert AdminLoginPage(browser).alert() == "Warning: Your account has " \
                                              "exceeded allowed number of " \
                                              "login attempts. Please try " \
                                              "again in 1 hour or reset " \
                                              "password.\n×"


@allure.feature("Authorization")
@pytest.mark.parametrize("username, password", [(get_userdata(letters=True, digits=False, simbols=False),
                                                 get_userdata(letters=False, digits=False, simbols=True)),
                                                (get_userdata(letters=False, digits=True, simbols=False),
                                                 get_userdata(letters=True, digits=False, simbols=False)),
                                                (get_userdata(letters=False, digits=False, simbols=True),
                                                 get_userdata(letters=False, digits=True, simbols=False)),
                                                ("", "")],
                         ids=["U-letters, P-simbols",
                              "U-digits, P-letters",
                              "U-simbols, P-digits",
                              "U-nothing, P-nothing"])
def test_invalid_login(browser, username, password):
    AdminLoginPage(browser).open()
    AdminLoginPage(browser).login(username, password)
    assert AdminLoginPage(browser).alert() == "No match for Username and/or Password.\n×"


@allure.feature("Authorization")
def test_forgotten_password(browser):
    AdminLoginPage(browser).open()
    assert AdminLoginPage(browser).verify_help_block().text == "Forgotten Password"\
        , "Don't have button 'Forgotten Password'"
    assert AdminLoginPage(browser).verify_forgotten_password()\
        , "Don't have field email"
