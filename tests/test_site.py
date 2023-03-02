import allure
import pytest

from pages.site import SitePage
from src.locators import Urls


@pytest.mark.parametrize("url", [Urls.url_site])
def test_site_page(browser, url):
    page = SitePage(browser, url)
    page.open()
    page.test_first()
    page.check_first_logos()
    page.check_btn_and_scroll()
    page.correct_requests()


@pytest.mark.parametrize("amount", ['-1', '0', '10', '1000', 'test'])
def test_payment_url(browser, amount):
    page = SitePage(browser, Urls.url_site)
    page.open()
    page.check_payment(amount)


def test_request(browser):
    page = SitePage(browser, Urls.url_site)
    page.open()
    page.get_page_status(Urls.url_site)
    page.get_page_request()
