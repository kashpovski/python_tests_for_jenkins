from pages.BasePage import BasePage
from selenium.webdriver.common.by import By


class UserPage(BasePage):
    PATH = "index.php?route=account/register"
    FIRSTNAME = (By.CSS_SELECTOR, "input[name='firstname']")
    LASTNAME = (By.CSS_SELECTOR, "input[name='lastname']")
    EMAIL = (By.CSS_SELECTOR, "input[name='email']")
    TELEPHONE = (By.CSS_SELECTOR, "input[name='telephone']")
    PASSWORD = (By.CSS_SELECTOR, "input[name='password']")
    TEXT_DANGER = " ~ div"
    PASSWORD_CONFIRM = (By.CSS_SELECTOR, "input[name='confirm']")
    BUTTON_CONTINUE = (By.CSS_SELECTOR, "input[value='Continue']")
    CHECKBOX_PRIVACY_POLICY = (By.CSS_SELECTOR, "input[name='agree']")
    BUTTON_PRIVACY_POLICY = (By.CSS_SELECTOR, "a.agree")
    PRIVACY_POLICY = (By.CSS_SELECTOR, "div.modal-content")
    ACCOUNT_CREATED = (By.CSS_SELECTOR, "div#content>h1")

    def registration(self, username="", email="", phone_number="", password=""):
        self._input(self.element(self.FIRSTNAME), username)
        self._input(self.element(self.LASTNAME), username)
        self._input(self.element(self.EMAIL), email)
        self._input(self.element(self.TELEPHONE), phone_number)
        self._input(self.element(self.PASSWORD), password)
        self._input(self.element(self.PASSWORD_CONFIRM), password)
        self.element(self.CHECKBOX_PRIVACY_POLICY).click()
        self.element(self.BUTTON_CONTINUE).click()
        return self

    def verify_privacy_policy(self):
        self.element(self.BUTTON_PRIVACY_POLICY).click()
        return self.element(self.PRIVACY_POLICY)

    def verify_text_danger(self, locator):
        self.element(self.BUTTON_CONTINUE).click()
        return self.element((locator[0], locator[1] + self.TEXT_DANGER)).text

    def verify_registration(self):
        return self.element(self.ACCOUNT_CREATED).text
