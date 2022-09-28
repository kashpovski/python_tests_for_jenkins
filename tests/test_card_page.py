import allure
import pytest

from pages.CardPage import CardPade
from data_for_test import *


@allure.feature("Page title")
@allure.title("Check title in card page")
@pytest.mark.parametrize("add_url, url_title", [("iphone", "iPhone"), ("imac", "iMac"), ("macbook", "MacBook")])
def test_title(browser, add_url, url_title):
    CardPade(browser).open(add_url)
    assert CardPade(browser).get_title() == url_title


@allure.feature("Add product to card")
@pytest.mark.parametrize("amount", ["1", "5", "33"])
@pytest.mark.parametrize("add_url", ["iphone", "imac", "macbook"])
def test_add_to_cart(browser, add_url, amount):
    CardPade(browser).open(add_url)
    CardPade(browser).add_to_card(amount)
    assert CardPade(browser).verify_count_prod_in_card() == amount


@allure.feature("Navigation")
@pytest.mark.parametrize("add_url", ["iphone", "imac", "macbook"])
def test_reviews(browser, add_url):
    CardPade(browser).open(add_url)
    username = get_userdata(long=10, letters=True, digits=False, simbols=False)
    text = get_userdata(long=25, letters=True, digits=False, simbols=False)
    CardPade(browser).create_review(username, text)
    assert CardPade(browser).alert() == \
           "Thank you for your review. It has been submitted to the webmaster for approval."
