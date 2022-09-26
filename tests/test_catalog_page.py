import pytest

from pages.ProductPage import ProductPage


def test_back_home(browser):
    ProductPage(browser).open()
    ProductPage(browser).go_home_page()
    assert ProductPage(browser).get_title() == "Your Store"


@pytest.mark.parametrize("locator, url_title", [(ProductPage.BUTTON_LAPTOPS, "Laptops & Notebooks"),
                                                (ProductPage.BUTTON_CAMERAS, "Cameras"),
                                                (ProductPage.BUTTON_MP3, "MP3 Players")],
                         ids=["Laptops & Notebooks", "Cameras", "MP3 Players"])
def test_title(browser, locator, url_title):
    ProductPage(browser).open()
    ProductPage(browser).navigation_in_catalog(locator)
    assert ProductPage(browser).get_title() == url_title


@pytest.mark.parametrize("view, class_name", [("list",
                                               "product-layout product-list col-xs-12"),
                                              ("grid",
                                               "product-layout product-grid col-lg-4 col-md-4 col-sm-6 col-xs-12")],
                         ids=["LIST", "GRID"])
def test_view(browser, view, class_name):
    ProductPage(browser).open()
    ProductPage(browser).change_prod_view(view)
    for el in ProductPage(browser).verify_prod_view():
        assert el == class_name


@pytest.mark.parametrize("locator", [ProductPage.BUTTON_LAPTOPS, ProductPage.BUTTON_CAMERAS, ProductPage.BUTTON_MP3],
                         ids=["Laptops & Notebooks", "Cameras", "MP3 Players"])
def test_per_product_on_page(browser, locator):
    ProductPage(browser).open()
    ProductPage(browser).navigation_in_catalog(locator)
    assert ProductPage(browser).verify_count_prod_on_page()
