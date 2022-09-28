import allure

from pages.BasePage import BasePage
from selenium.webdriver.common.by import By


class ProductPage(BasePage):
    PATH = "desktops"
    BUTTON_HOME = (By.CSS_SELECTOR, ".breadcrumb li:first-child a")
    BUTTON_LAPTOPS = (By.XPATH, "//*[@id='column-left']/*/*[contains(text(), 'Laptops & Notebooks')]")
    BUTTON_CAMERAS = (By.XPATH, "//*[@id='column-left']/*/*[contains(text(), 'Cameras')]")
    BUTTON_MP3 = (By.XPATH, "//*[@id='column-left']/*/*[contains(text(), 'MP3 Players')]")
    BUTTON_LIST = (By.CSS_SELECTOR, "#list-view")
    BUTTON_GRID = (By.CSS_SELECTOR, "#grid-view")
    PRODUCT = (By.CSS_SELECTOR, ".row .product-layout")
    COUNT_TEXT = (By.CSS_SELECTOR, ".text-right")

    @allure.step
    def go_home_page(self):
        self.element(self.BUTTON_HOME).click()

    @allure.step
    def navigation_in_catalog(self, category_prod):
        self.element(category_prod).click()

    @allure.step
    def change_prod_view(self, view):
        if view == "list":
            self.element(self.BUTTON_LIST).click()
        elif view == "grid":
            self.element(self.BUTTON_GRID).click()
        else:
            return "viwe - list or grid"

    @allure.step
    def verify_prod_view(self):
        for el in self.elements(self.PRODUCT):
            yield el.get_attribute("class")

    @allure.step
    def verify_count_prod_on_page(self):
        prod_count = len(self.elements(self.PRODUCT))
        count_in_page = int(self.element(self.COUNT_TEXT).text.split()[5])
        return prod_count == count_in_page
