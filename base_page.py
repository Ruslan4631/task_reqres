import allure
from percy import percy_snapshot
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, browser, url, timeout=20):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)

    def open(self):
        self.browser.get(self.url)

    def close(self):
        self.browser.close()

    def scroll_to_element_and_click(self, locator, timeout=5):
        element = WebDriverWait(self.browser, timeout).until(
            EC.presence_of_element_located(locator), message=f"Не удается найти элементы по локатору {locator}")
        ActionChains(self.browser).move_to_element(element).perform()
        element.click()

    def is_element_present_contacts(self, locator, timeout=10):
        self.browser.implicitly_wait(timeout)
        try:
            self.browser.find_element(*locator)
        except NoSuchElementException:
            return False
        return True

    def send_keys(self, how, what, keys, timeout=10):
        WebDriverWait(self.browser, timeout).until(
            EC.element_to_be_clickable((how, what)), 'Время ожидания истекло')
        self.scroll_to_element(how, what)
        self.browser.find_element(how, what).send_keys(keys)

    def is_element_visible_wait(self, locator, timeout=5):
        try:
            WebDriverWait(self.browser, timeout).until(
                EC.visibility_of_element_located(locator), 'Время ожидания истекло')
            return True
        except TimeoutException:
            return False

    def scroll_to_element(self, how, what):
        elem = self.browser.find_element(how, what)
        self.browser.execute_script("return arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", elem)

    def send_text_input(self, locator, text):
        element = self.browser.find_element(*locator)
        ActionChains(self.browser).move_to_element(element).perform()
        element.send_keys(text)

    def scroll_to_element_my(self, locator, timeout=5):
        element = WebDriverWait(self.browser, timeout).until(
            EC.presence_of_element_located(locator), message=f"Не удается найти элементы по локатору {locator}")
        ActionChains(self.browser).move_to_element(element).perform()

    def get_href(self, locator):
        element = self.browser.find_element(*locator)
        return str(element.get_attribute('href'))

    def get_text_my(self, locator):
        element = self.browser.find_element(*locator)
        ActionChains(self.browser).move_to_element(element).perform()
        text = element.text
        return text

    def get_elements(self, locator):
        elements = self.browser.find_elements(*locator)
        return elements
