import pytest

from pages.MainPage import MainPage


def test_title(browser):
    MainPage(browser).open()
    assert MainPage(browser).get_title() == "Your Store"


@pytest.mark.parametrize("query", ["Mac", "Phone", "Apple", "Canon"])
def test_search_field(browser, query):
    MainPage(browser).open()
    MainPage(browser).searching(query)
    MainPage(browser).verify_search_field()
    assert MainPage(browser).verify_search_query(query), f"query result does not match query - {query}"


@pytest.mark.parametrize("result", [("Desktops", "Laptops & Notebooks", "Components", "Tablets", "Software",
                                     "Phones & PDAs", "Cameras", "MP3 Players")], ids=["name elements in navbar"])
def test_nav_bar(browser, result):
    MainPage(browser).open()
    for el in MainPage(browser).verify_navbar_elements():
        assert el in result, f"Not found element - '{el}' in Nav Bar"


@pytest.mark.parametrize("locator, currency", [(MainPage.EUR, "€"),
                                               (MainPage.GBP, "£"),
                                               (MainPage.USD, "$")], ids=["EUR", "GBP", "USD"])
def test_currency(browser, locator, currency):
    MainPage(browser).open()
    MainPage(browser).change_currency(locator)
    assert MainPage(browser).verify_currency(currency), f"Currency - '{currency}' not find in page"
