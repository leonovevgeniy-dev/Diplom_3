import allure
from pages.constructor_page import ConstructorPage


@allure.feature('Навигация')
class TestNavigation:
    
    @allure.title('Переход между страницами')
    def test_switch_between_pages(self, browser):
        constructor_page = ConstructorPage(browser)
        
        constructor_page.click_order_feed()
        assert constructor_page.wait_for_feed_page()
        
        constructor_page.click_constructor()
        assert constructor_page.wait_for_constructor_page()