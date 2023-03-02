import json
import time

import requests

from base_page import BasePage
from src.locators import Urls, Locators, PaymentLocators


class SitePage(BasePage):
    def test_first(self):
        assert True

    # check site web
    def check_web(self):
        assert Urls.url_site == self.browser.current_url, 'Некорректная ссылка'

    def check_first_logos(self):
        self.is_element_present_contacts(Locators.ICONS)
        self.is_element_visible_wait(Locators.ICONS)
        assert len(self.get_elements(Locators.ICONS)) == 3, 'Количество иконок не равно 3'

    def check_btn_and_scroll(self):
        position_before = self.browser.execute_script('return window.pageYOffset;')
        self.is_element_visible_wait(Locators.BTN_SUPPORT)
        self.scroll_to_element_and_click(Locators.BTN_SUPPORT)
        assert '#support-heading' in self.browser.current_url, 'Отсутствует скролл к позиции'
        time.sleep(3)
        position_after = self.browser.execute_script('return window.pageYOffset;')
        assert position_after > position_before, 'Страница не проскролилась'

    def correct_requests(self):
        reqs = self.get_elements(Locators.LIST_REQUESTS)
        for i in reqs:
            i.click()
            time.sleep(0.7)
            self.is_element_visible_wait(Locators.TABLE_RESPONSE)
            assert self.is_element_present_contacts(Locators.ICONS), 'Отсутствует таблица ответа'
            self.get_page_request()

    def check_payment(self, amount):
        self.scroll_to_element_my(Locators.INPUT)
        self.send_text_input(Locators.INPUT, amount)
        self.scroll_to_element_and_click(Locators.BTN_SUPPORT_ACCEPT)
        self.is_element_visible_wait(PaymentLocators.SUM)
        assert Urls.payment_url in self.browser.current_url, 'Произошёл переход на другую страницу'
        assert self.is_element_present_contacts(PaymentLocators.SUM), 'Отсутствует сумма оплаты'
        assert amount in self.get_text_my(PaymentLocators.SUM), 'Сумма оплаты отличается'

        assert self.is_element_present_contacts(PaymentLocators.CARD_EMAIL), 'Отсутствует инпут почты'
        assert self.is_element_present_contacts(PaymentLocators.CARD_NUMBER), 'Отсутствует номер карты'
        assert self.is_element_present_contacts(PaymentLocators.CARD_EXPIRE), 'Отсутствует срок действия карты'
        assert self.is_element_present_contacts(PaymentLocators.CARD_BILLING_NAME), 'Отсутствует cvv'
        assert self.is_element_present_contacts(PaymentLocators.CARD_NAME), 'Отсутствует инпут ФИ'
        assert self.is_element_present_contacts(PaymentLocators.CARD_COUNTRY), 'Отсутствует селектор страны'
        assert self.is_element_present_contacts(PaymentLocators.CARD_ACCEPT_BTN), 'Отсутствует кнопка оплаты'

    def get_page_status(self, url_check):
        response = requests.get(url_check)
        assert response.status_code == 200, 'Сервис недоступен'

    # Функция для проверки реквеста и респонса
    def get_page_request(self):
        text_response = self.get_text_my(Locators.TABLE_RESPONSE)
        json_response = json.loads(text_response)
        url = self.get_text_my(Locators.URL_REQUEST)
        response = requests.get(f'https://reqres.in{url}')
        response_body = response.json()
        assert response_body == json_response, f'error'

# Необходимо на Python + PyTest написать:
# 1) Проверки API с главной страницы, которые представлены как образец, позитивные и негативные

# 2) Проверить WEB на главной странице,
# проверить что при нажатии на кнопку отправки образца запроса
# результат такой же как и через API

# 3)Реализовать фикстуры и парамтеризацию

# Результат залить на github и предоставить ссылку
