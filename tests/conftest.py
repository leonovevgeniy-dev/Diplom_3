# conftest.py
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pytest
import os
import ssl
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


ssl._create_default_https_context = ssl._create_unverified_context
os.environ["WDM_SSL_VERIFY"] = "0"
os.environ["CURL_CA_BUNDLE"] = ""

for key in list(os.environ.keys()):
    if key.lower() in ("http_proxy", "https_proxy", "all_proxy"):
        del os.environ[key]


class Config:
    BASE_URL = 'https://stellarburgers.education-services.ru'
    TEST_EMAIL = 'test_lee_2024@yandex.ru'
    TEST_PASSWORD = 'SecurePass123!'
    TEST_NAME = 'Test User'


def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='chrome', help='Browser: chrome or firefox')


@pytest.fixture(scope="session")
def access_token():
    """
    Получает токен авторизации.
    Сначала пробуем залогиниться с фиксированными данными.
    Если пользователя нет — регистрируем его.
    """
    base = Config.BASE_URL
    email = Config.TEST_EMAIL
    password = Config.TEST_PASSWORD
    name = Config.TEST_NAME
    
    login_resp = requests.post(
        f"{base}/api/auth/login",
        json={"email": email, "password": password},
        timeout=10,
        verify=False
    )
    
    if login_resp.status_code == 200:
        token = login_resp.json().get("accessToken")
        if token:
            return token
    
    reg_resp = requests.post(
        f"{base}/api/auth/register",
        json={"email": email, "password": password, "name": name},
        timeout=10,
        verify=False
    )
    
    if reg_resp.status_code == 200:
        token = reg_resp.json().get("accessToken")
        if token:
            return token
    
    login_resp2 = requests.post(
        f"{base}/api/auth/login",
        json={"email": email, "password": password},
        timeout=10,
        verify=False
    )
    
    if login_resp2.status_code == 200:
        token = login_resp2.json().get("accessToken")
        if token:
            return token
    
    raise RuntimeError(
        f"Не удалось получить токен авторизации.\n"
        f"Login: {login_resp.status_code} - {login_resp.text}\n"
        f"Register: {reg_resp.status_code} - {reg_resp.text}"
    )


@pytest.fixture
def browser(request):
    """Фикстура браузера с обходом SSL-проблем"""
    browser_name = request.config.getoption('--browser')
    
    if browser_name == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-insecure-localhost')
        
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), 
            options=options
        )
        
    elif browser_name == 'firefox':
        options = webdriver.FirefoxOptions()
        options.add_argument('--width=1920')
        options.add_argument('--height=1080')
        options.set_preference('security.enterprise_roots.enabled', True)
        options.set_preference('security.ssl.enable_ocsp_stapling', False)
        
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()), 
            options=options
        )
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    driver.get(Config.BASE_URL)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.fixture
def base_url():
    return Config.BASE_URL