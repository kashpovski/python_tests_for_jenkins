import allure
import pytest

from pages.UserPage import UserPage
from data_for_test import *


@allure.link("https://docs.qameta.io/allure-report/#_about")
@allure.feature("Page title")
@allure.title("Check title in user page")
def test_title(browser):
    UserPage(browser).open()
    assert UserPage(browser).get_title() == "Register Account"


@allure.link("https://docs.qameta.io/allure-report/#_about", name="Docs allure")
@allure.feature("Alert")
def test_privacy_policy(browser):
    UserPage(browser).open()
    UserPage(browser).verify_privacy_policy()


@allure.issue("https://docs.qameta.io/allure-report/#_about", name="Docs allure")
@allure.feature("Alert")
@pytest.mark.parametrize("locator, text_danger", [(UserPage.FIRSTNAME,
                                                   "First Name must be between 1 and 32 characters!"),
                                                  (UserPage.LASTNAME,
                                                   "Last Name must be between 1 and 32 characters!"),
                                                  (UserPage.EMAIL,
                                                   "E-Mail Address does not appear to be valid!"),
                                                  (UserPage.TELEPHONE,
                                                   "Telephone must be between 3 and 32 characters!"),
                                                  (UserPage.PASSWORD, "Password must be between 4 and 20 characters!")],
                         ids=["FIRSTNAME", "LASTNAME", "EMAIL", "TELEPHONE", "PASSWORD"])
def test_text_danger(browser, locator, text_danger):
    UserPage(browser).open()
    assert UserPage(browser).verify_text_danger(locator) == text_danger


@allure.feature("Registration")
@allure.severity(severity_level="valid")
def test_success_account_created(browser):
    UserPage(browser).open()
    username = get_userdata(long=10, letters=True, digits=False, simbols=False)
    email = get_email(long=10, letters=True, digits=False, simbols=False)
    phone_number = get_userdata(long=10, letters=False, digits=True, simbols=False)
    password = get_userdata(long=10, letters=True, digits=False, simbols=False)
    UserPage(browser).registration(username, email, phone_number, password)
    assert UserPage(browser).verify_registration() == "Your Account Has Been Created!"
