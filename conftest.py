import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService


failed_test = pytest.StashKey[bool]()


def pytest_addoption(parser):
    parser.addoption('--browser_name',
                     action='store',
                     default="",
                     help="Choose browser: chrome, firefox or opera")
    parser.addoption('--browser_version',
                     action='store',
                     default="",
                     help="Choose browser version (only for selenoid). Example: 100.0 ")
    parser.addoption('--language',
                     action='store',
                     default='ru',
                     help="Choose language: ru, en-gb, ... (etc)")
    parser.addoption('--selenoid',
                     action='store_true',
                     default=False,
                     help="Run tests on selenoid")
    parser.addoption('--resolution',
                     action='store',
                     default='1920x1080',
                     help="Choose resolution: <WIDTH>x<HEIGTH>")
    parser.addoption('--stage',
                     action='store_true',
                     default=False,
                     help="Run tests on stage")
    parser.addoption('--vnc',
                     action='store_true',
                     default=False,
                     help="Enable VNC")
    parser.addoption('--video',
                     action='store_true',
                     default=False,
                     help="Enable VNC")


@pytest.fixture(autouse=True)
def selenoid_enabled(request):
    return request.config.getoption("selenoid")


@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("browser_name")
    browser_version = request.config.getoption('browser_version')
    user_language = request.config.getoption("language")
    selenoid = request.config.getoption("selenoid")
    browser_resolution = request.config.getoption("resolution")
    width = browser_resolution.split('x')[0]
    height = browser_resolution.split('x')[1]
    vnc = request.config.getoption("vnc")
    video = request.config.getoption("video")
    if selenoid is True:
        print(f"\nstart {browser_name} browser on selenoid for test..")
        if browser_name == 'chrome':

            options = ChromeOptions()
            options.set_capability('selenoid:options', {
                "enableVNC": vnc,
                "enableVideo": video,
                "sessionTimeout": '5m',
                "videoFrameRate": 12,
            })

            options.set_capability('browserVersion', browser_version)
            options.add_argument(f'--window-size={width},{height}')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--ignore-certificate-error")
            options.add_argument("--ignore-ssl-errors")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-gpu")
            # options.add_argument('--proxy-server=%s' % proxy)
            options.add_experimental_option(
                'prefs',
                {'intl.accept_languages': user_language, "download.default_directory": os.getcwd() + "/documents/"})

            browser = webdriver.Remote(
                command_executor=f"http://192.168.1.129:4444/wd/hub",
                options=options)

        elif browser_name == 'firefox':
            options = FirefoxOptions()
            options.set_capability('enableVNC', True)
            options.set_capability('enableVideo', False)
            options.set_capability('browserVersion', browser_version)
            options.set_capability('screenResolution', browser_resolution)
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.manager.showWhenStarting", False)
            options.set_preference("browser.download.dir", os.getcwd() + "/documents/")
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")

            browser = webdriver.Remote(
                command_executor=f"http://192.168.1.129:4444/wd/hub",
                options=options)

            browser.maximize_window()

        # elif browser_name == 'opera':
        #     options = OperaOptions()
        #     options.set_capability('enableVNC', True)
        #     options.set_capability('enableVideo', False)
        #     options.set_capability('browserVersion', browser_version)
        #     options.set_capability('screenResolution', browser_resolution)
        #
        #     browser = webdriver.Remote(
        #         command_executor=f"{selenoid_url}/wd/hub",
        #         options=options)
        #     browser.maximize_window()
        else:
            raise pytest.UsageError("--browser_name should be chrome, firefox or opera")

    else:
        if browser_name == "chrome":
            print("\nstart chrome browser for test..")
            options = ChromeOptions()
            options.set_capability('enableVNC', True)
            options.add_argument(f'--window-size={width},{height}')
            options.add_argument("--ignore-certificate-error")
            options.add_argument("--ignore-ssl-errors")
            options.add_experimental_option(
                'prefs',
                {'intl.accept_languages': user_language, "download.default_directory": os.getcwd() + "/documents/"})
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            browser = webdriver.Chrome(service=ChromeService(), options=options)

        elif browser_name == "firefox":
            print("\nstart firefox browser for test..")
            options = FirefoxOptions()
            options.add_argument(f'--width={width}')
            options.add_argument(f'--height={height}')
            options.headless = False
            browser = webdriver.Firefox(service=FirefoxService(), options=options)
        else:
            raise pytest.UsageError("--browser_name should be chrome, firefox or opera")

        browser.maximize_window()

    yield browser

    print("\nquit browser..")
    browser.quit()
