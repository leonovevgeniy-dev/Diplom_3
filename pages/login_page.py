import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.locators import LoginPageLocators


class LoginPage(BasePage):
    
    @allure.step('Авторизация пользователя с email: {email}')
    def login(self, email, password):
        self.send_keys(LoginPageLocators.EMAIL_INPUT, email)
        self.send_keys(LoginPageLocators.PASSWORD_INPUT, password)
        self.click(LoginPageLocators.LOGIN_BUTTON)
    
    @allure.step('Ввод текста в поле {locator}')
    def send_keys(self, locator, text, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)