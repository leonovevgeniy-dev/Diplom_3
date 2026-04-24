import allure
import time
from pages.constructor_page import ConstructorPage
from locators.locators import MainPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature('Навигация')
class TestNavigation:
    
    @allure.title('Переход между страницами')
    def test_switch_between_pages(self, browser, base_url):
        wait = WebDriverWait(browser, 10)
        
        try:
            close_button = wait.until(EC.element_to_be_clickable(MainPageLocators.CLOSE_MODAL_BUTTON))
            close_button.click()
        except:
            pass
        
        constructor_page = ConstructorPage(browser)
        
        constructor_page.click_order_feed()
        wait.until(EC.url_contains("feed"))
        assert "feed" in browser.current_url.lower()
        
        constructor_page.click_constructor()
        wait.until(EC.url_to_be(base_url + "/"))
        assert browser.current_url == base_url + "/" or browser.current_url == base_url