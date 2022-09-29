import time
import random
import allure

from pages.BasePage import BasePage
from selenium.webdriver.common.by import By


class CardPade(BasePage):
    CART_TOTAL = (By.CSS_SELECTOR, "span#cart-total")
    BUTTON_ADDTOCART = (By.CSS_SELECTOR, "button#button-cart")
    QUANTITY = (By.CSS_SELECTOR, "#input-quantity")
    REVIEWS = (By.CSS_SELECTOR, "[href='#tab-review']")
    REVIEW_NAME = (By.CSS_SELECTOR, "#input-name")
    REVIEW_TEXT = (By.CSS_SELECTOR, "#input-review")
    RATING = (By.CSS_SELECTOR, "[name='rating']")
    BUTTON_CONTINUE = (By.CSS_SELECTOR, "button#button-review")

    @allure.step
    def add_to_card(self, value):
        self._input(self.element(self.QUANTITY), value)
        self.element(self.BUTTON_ADDTOCART).click()
        time.sleep(2)

    @allure.step
    def create_review(self, username, review_text):
        self.element(self.REVIEWS).click()
        self._input(self.element(self.REVIEW_NAME), username)
        self._input(self.element(self.REVIEW_TEXT), review_text)
        self.elements(self.RATING)[random.randint(0, 4)].click()
        self.element(self.BUTTON_CONTINUE).click()

    @allure.step
    def verify_count_prod_in_card(self):
        return self.element(self.CART_TOTAL).text.split()[0]
