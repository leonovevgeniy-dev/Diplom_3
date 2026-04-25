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
from urls import Urls


ssl._create_default_https_context = ssl._create_unverified_context
os.environ["WDM_SSL_VERIFY"] = "0"
os.environ["CURL_CA_BUNDLE"] = ""

# Убираем прокси
for key in list(os.environ.keys()):
    if key.lower() in ("http_proxy", "https_proxy", "all_proxy"):
        del os.environ[key]


def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='chrome', help='Browser: chrome or firefox')


@pytest.fixture(scope="session")
def access_token():
    """Получает токен авторизации."""
    base = Urls.BASE_URL
    email = 'test_lee_2024@yandex.ru'
    password = 'SecurePass123!'
    name = 'Test User'
    

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
    
    # Регистрируем нового пользователя
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
    
    raise RuntimeError(f"Не удалось получить токен. Login: {login_resp.status_code}, Register: {reg_resp.status_code}")


@pytest.fixture
def browser(request):
    """Фикстура браузера"""
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

    driver.get(Urls.BASE_URL)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()