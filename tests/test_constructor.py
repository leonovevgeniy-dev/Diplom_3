import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from locators.locators import MainPageLocators


@allure.feature('Конструктор бургеров')
class TestConstructor:
    
    @allure.title('Переход по клику на "Конструктор"')
    def test_click_constructor(self, browser, base_url):
        wait = WebDriverWait(browser, 10)
        
        order_feed = wait.until(EC.element_to_be_clickable(MainPageLocators.ORDER_FEED_BUTTON))
        order_feed.click()
        
        wait.until(EC.url_contains("feed"))
        assert "feed" in browser.current_url
        
        constructor = wait.until(EC.element_to_be_clickable(MainPageLocators.CONSTRUCTOR_BUTTON))
        constructor.click()
        
        wait.until(EC.url_to_be(base_url + "/"))
        assert browser.current_url == base_url + "/" or browser.current_url == base_url
    
    @allure.title('Клик на ингредиент — открывается всплывающее окно')
    def test_ingredient_modal_opens(self, browser, base_url):
        wait = WebDriverWait(browser, 10)
        
        ingredient = wait.until(EC.element_to_be_clickable(MainPageLocators.BUN_INGREDIENT))
        ingredient.click()
        
        modal = wait.until(EC.visibility_of_element_located(MainPageLocators.INGREDIENT_MODAL))
        assert modal.is_displayed()
    
    @allure.title('Всплывающее окно закрывается кликом по крестику')
    def test_ingredient_modal_closes(self, browser, base_url):
        wait = WebDriverWait(browser, 10)
        
        ingredient = wait.until(EC.element_to_be_clickable(MainPageLocators.BUN_INGREDIENT))
        ingredient.click()
        
        modal = wait.until(EC.visibility_of_element_located(MainPageLocators.INGREDIENT_MODAL))
        assert modal.is_displayed()
        
        close_button = wait.until(EC.element_to_be_clickable(MainPageLocators.CLOSE_MODAL_BUTTON))
        close_button.click()
        
        wait.until(EC.invisibility_of_element_located(MainPageLocators.INGREDIENT_MODAL))
    
    @allure.title('При добавлении ингредиента счётчик увеличивается')
    def test_ingredient_counter_increases(self, browser, base_url):
        wait = WebDriverWait(browser, 10)
        
        ingredient = wait.until(EC.presence_of_element_located(MainPageLocators.BUN_INGREDIENT))
        constructor = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section[class*='BurgerConstructor']")))
        
        counters = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p[class*='counter_counter__num']")))
        count_before = int(counters[0].text) if counters else 0
        
        actions = ActionChains(browser)
        actions.drag_and_drop(ingredient, constructor).perform()
        
        wait.until(lambda d: int(d.find_elements(By.CSS_SELECTOR, "p[class*='counter_counter__num']")[0].text) > count_before)
        
        count_after = int(browser.find_elements(By.CSS_SELECTOR, "p[class*='counter_counter__num']")[0].text)
        assert count_after > count_before