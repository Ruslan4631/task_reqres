from selenium.webdriver.common.by import By


class Urls:
    url_site = 'https://reqres.in/'
    payment_url = 'https://checkout.stripe.com/'


class Locators:
    ICONS = (By.CSS_SELECTOR, '.sell')
    BTN_SUPPORT = (By.XPATH, "//a[contains(text(),'Support ReqRes')]")
    LIST_REQUESTS = (By.XPATH, "//li[@data-key='endpoint']")
    TABLE_RESPONSE = (By.XPATH, "//pre[@data-key='output-response']")
    INPUT = (By.XPATH, "//input[@name='oneTimeAmount']")
    BTN_SUPPORT_ACCEPT = (By.XPATH, "//button[text()='Support ReqRes']")
    URL_REQUEST = (By.XPATH, "//span[@data-key='url']")
    RESULT = (By.TAG_NAME, 'pre')


class PaymentLocators:
    SUM = (By.CSS_SELECTOR, '#ProductSummary-totalAmount > span')
    CARD_EMAIL = (By.ID, 'email')
    CARD_NUMBER = (By.ID, 'cardNumber')
    CARD_EXPIRE = (By.ID, 'cardExpiry')
    CARD_BILLING_NAME = (By.ID, 'cardCvc')
    CARD_NAME = (By.ID, 'billingName')
    CARD_COUNTRY = (By.ID, 'billingCountry')
    CARD_ACCEPT_BTN = (By.CSS_SELECTOR, '.SubmitButton-IconContainer')
