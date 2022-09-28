import time
import allure

from pages.BasePage import BasePage
from selenium.webdriver.common.by import By


class MainPage(BasePage):
    SEARCH = (By.CSS_SELECTOR, "input[name = 'search']")
    BUTTON_SEARCH = (By.CSS_SELECTOR, "button.btn.btn-default.btn-lg")
    SEARCH_FIELD = (By.CSS_SELECTOR, "div#product-search")
    PROD_CARD = (By.CSS_SELECTOR, "div.product-layout div.caption a")
    NAVBAR = (By.CSS_SELECTOR, "ul.nav.navbar-nav > li > a")
    SWIPER_ELEMENT = (By.CSS_SELECTOR, "div[class*='sw']:last-of-type > a[href] ")
    CHANGE_CURRENCY = (By.CSS_SELECTOR, "#form-currency [data-toggle]")
    EUR = (By.CSS_SELECTOR, "[name = 'EUR']")
    GBP = (By.CSS_SELECTOR, "[name = 'GBP']")
    USD = (By.CSS_SELECTOR, "[name = 'USD']")

    @allure.step
    def searching(self, what):
        self._input(self.element(self.SEARCH), what)
        self.element(self.BUTTON_SEARCH).click()

    @allure.step
    def verify_search_query(self, what):
        search_query = self.elements(self.PROD_CARD)
        result = False
        for el in search_query:
            if el.text.lower().find(what.lower()) == -1:
                result = False
                break
            elif el.text.lower().find(what.lower()) >= 0:
                result = True
        return result

    @allure.step
    def change_currency(self, currency):
        self.element(self.CHANGE_CURRENCY).click()
        self.element(currency).click()
        time.sleep(1)

    @allure.step
    def verify_currency(self, currency):
        presence_currency = False
        if len(self.browser.find_elements(By.XPATH, f"//*[contains(text(), '{currency}')]")) != 0:
            presence_currency = True
        return presence_currency

    @allure.step
    def verify_search_field(self):
        return self.element(self.SEARCH_FIELD)

    @allure.step
    def verify_navbar_elements(self):
        for el in self.elements(self.NAVBAR):
            yield el.text
