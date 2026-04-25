import allure
from selenium.webdriver.support import expected_conditions as EC
from pages.constructor_page import ConstructorPage
from locators.locators import MainPageLocators


@allure.feature('Конструктор бургеров')
class TestConstructor:
    
    @allure.title('Переход по клику на "Конструктор"')
    def test_click_constructor(self, browser):
        constructor_page = ConstructorPage(browser)
        
        constructor_page.click_order_feed()
        assert constructor_page.wait_for_feed_page()
        
        constructor_page.click_constructor()
        assert constructor_page.wait_for_constructor_page()
    
    @allure.title('Клик на ингредиент — открывается всплывающее окно')
    def test_ingredient_modal_opens(self, browser):
        constructor_page = ConstructorPage(browser)
        
        constructor_page.click_bun_ingredient()
        
        assert constructor_page.is_ingredient_modal_visible()
    
    @allure.title('Всплывающее окно закрывается кликом по крестику')
    def test_ingredient_modal_closes(self, browser):
        constructor_page = ConstructorPage(browser)
        
        constructor_page.click_bun_ingredient()
        assert constructor_page.is_ingredient_modal_visible()
        
        constructor_page.close_ingredient_modal()
        
        # Явное ожидание закрытия модального окна
        constructor_page.wait.until(EC.invisibility_of_element_located(MainPageLocators.INGREDIENT_MODAL))
        
        assert not constructor_page.is_ingredient_modal_visible()
    
    @allure.title('При добавлении ингредиента счётчик увеличивается')
    def test_ingredient_counter_increases(self, browser):
        constructor_page = ConstructorPage(browser)
        
        count_before = constructor_page.get_bun_counter()
        
        constructor_page.drag_bun_to_constructor()
        
        count_after = constructor_page.get_bun_counter()
        assert count_after > count_before