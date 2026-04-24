# locators/locators.py
from selenium.webdriver.common.by import By


class MainPageLocators:
    """Локаторы главной страницы"""
    CONSTRUCTOR_BUTTON = (By.XPATH, "//*[@id='root']/div/header/nav/ul/li[1]/a/p")
    ORDER_FEED_BUTTON = (By.XPATH, "//*[@id='root']/div/header/nav/ul/li[2]/a/p")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//*[@id='root']/div/header/nav/ul/li[3]/a/p")

    # Ингредиенты
    BUN_INGREDIENT = (By.XPATH, "//img[@alt='Флюоресцентная булка R2-D3']")
    BUN_INGREDIENT_PARENT = (By.XPATH, "//img[@alt='Флюоресцентная булка R2-D3']/parent::a")

    # Счётчик ингредиента
    BUN_COUNTER = (By.CSS_SELECTOR, "p[class*='counter_counter__num']")
    
    # Модальное окно
    INGREDIENT_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal__')]")
    CLOSE_MODAL_BUTTON = (By.XPATH, "//div[contains(@class, 'Modal_modal__')]//button")
    CHECKOUT_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")


class OrderFeedLocators:
    ORDER_FEED_TITLE = (By.XPATH, "//h1[text()='Лента заказов']")
    
    # ✅ ИСПРАВЛЕНО: добавлено '*' после '//'
    TOTAL_ORDERS_COUNTER = (By.XPATH, "//*[@id='root']/div/main/div/div/div/div[2]/p[2]")
    TODAY_ORDERS_COUNTER = (By.XPATH, "//*[@id='root']/div/main/div/div/div/div[3]/p[2]")
    
    # ✅ Локатор для номеров заказов
    ORDER_NUMBER = (By.CSS_SELECTOR, "li[class*='text_type_digits-default']")
    ORDER_LIST = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady')]//li")


class LoginPageLocators:
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")