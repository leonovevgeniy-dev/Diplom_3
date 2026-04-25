import allure
from pages.base_page import BasePage
from locators.locators import MainPageLocators
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from urls import Urls


class ConstructorPage(BasePage):
    
    @allure.step('Клик на "Конструктор"')
    def click_constructor(self):
        self.click(MainPageLocators.CONSTRUCTOR_BUTTON)
    
    @allure.step('Клик на "Лента заказов"')
    def click_order_feed(self):
        self.click(MainPageLocators.ORDER_FEED_BUTTON)
    
    @allure.step('Клик на ингредиент')
    def click_bun_ingredient(self):
        self.click(MainPageLocators.BUN_INGREDIENT)
    
    @allure.step('Проверка видимости модального окна')
    def is_ingredient_modal_visible(self, timeout=5):
        return self.is_visible(MainPageLocators.INGREDIENT_MODAL, timeout)
    
    @allure.step('Закрыть модальное окно')
    def close_ingredient_modal(self):
        self.click(MainPageLocators.CLOSE_MODAL_BUTTON)
    
    @allure.step('Получение значения счётчика ингредиента')
    def get_bun_counter(self):
        text = self.get_text(MainPageLocators.BUN_COUNTER)
        return int(text) if text.isdigit() else 0
    
    @allure.step('Перетаскивание ингредиента в конструктор')
    def drag_bun_to_constructor(self):
        ingredient = self.get_element(MainPageLocators.BUN_INGREDIENT)
        constructor = self.get_element((By.CSS_SELECTOR, "section[class*='BurgerConstructor']"))
        actions = ActionChains(self.driver)
        actions.drag_and_drop(ingredient, constructor).perform()
        self.wait.until(lambda d: int(d.find_element(*MainPageLocators.BUN_COUNTER).text) > 0)
    
    @allure.step('Ожидание перехода на Ленту заказов')
    def wait_for_feed_page(self):
        return self.wait_for_url_contains('feed')
    
    @allure.step('Ожидание перехода на Конструктор')
    def wait_for_constructor_page(self):
        base_url = Urls.BASE_URL
        return self.wait_for_url_to_be(f"{base_url}/") or self.wait_for_url_to_be(base_url)