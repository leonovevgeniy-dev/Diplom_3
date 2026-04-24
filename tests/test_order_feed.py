# tests/test_order_feed.py
import allure
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.constructor_page import ConstructorPage
from locators.locators import MainPageLocators, OrderFeedLocators


@allure.feature('Лента заказов')
class TestOrderFeed:

    @allure.title('Переход по клику на "Лента заказов"')
    def test_click_order_feed(self, browser, base_url):
        constructor_page = ConstructorPage(browser)
        constructor_page.click_order_feed()
        WebDriverWait(browser, 10).until(EC.url_contains("feed"))
        assert "feed" in browser.current_url.lower()

    @allure.title('Счётчик "Выполнено за всё время" увеличивается')
    def test_total_orders_counter_increases(self, browser, base_url, access_token):
        wait = WebDriverWait(browser, 15)
        
        try:
            close_button = wait.until(EC.element_to_be_clickable(MainPageLocators.CLOSE_MODAL_BUTTON))
            close_button.click()
        except:
            pass
        
        constructor_page = ConstructorPage(browser)
        constructor_page.click_order_feed()

        total_before_el = wait.until(
            EC.visibility_of_element_located(OrderFeedLocators.TOTAL_ORDERS_COUNTER)
        )
        total_before = int(total_before_el.text) if total_before_el.text.isdigit() else 0

        ingredients_resp = requests.get(f'{base_url}/api/ingredients', timeout=10)
        ingredients = ingredients_resp.json().get('data', [])[:2]
        ingredient_ids = [ing['_id'] for ing in ingredients]

        headers = {"Authorization": access_token}
        order_resp = requests.post(
            f'{base_url}/api/orders',
            json={'ingredients': ingredient_ids},
            headers=headers,
            timeout=10
        )
        assert order_resp.status_code == 200, f"API error: {order_resp.text}"

        browser.refresh()
        
        wait.until(lambda d: d.find_element(*OrderFeedLocators.TOTAL_ORDERS_COUNTER).text != str(total_before))
        
        def counter_increased(driver):
            current = driver.find_element(*OrderFeedLocators.TOTAL_ORDERS_COUNTER).text
            current_val = int(current) if current.isdigit() else 0
            return current_val > total_before

        wait.until(counter_increased, message="Счётчик 'Выполнено за всё время' не изменился")
        
        total_after = int(browser.find_element(*OrderFeedLocators.TOTAL_ORDERS_COUNTER).text)
        assert total_after > total_before

    @allure.title('Счётчик "Выполнено за сегодня" увеличивается')
    def test_today_orders_counter_increases(self, browser, base_url, access_token):
        wait = WebDriverWait(browser, 15)

        constructor_page = ConstructorPage(browser)
        constructor_page.click_order_feed()

        today_before_el = wait.until(
            EC.visibility_of_element_located(OrderFeedLocators.TODAY_ORDERS_COUNTER)
        )
        today_before = int(today_before_el.text) if today_before_el.text.isdigit() else 0

        ingredients_resp = requests.get(f'{base_url}/api/ingredients', timeout=10)
        ingredients = ingredients_resp.json().get('data', [])[:2]
        ingredient_ids = [ing['_id'] for ing in ingredients]

        headers = {"Authorization": access_token}
        order_resp = requests.post(
            f'{base_url}/api/orders',
            json={'ingredients': ingredient_ids},
            headers=headers,
            timeout=10
        )
        assert order_resp.status_code == 200, f"API error: {order_resp.text}"

        browser.refresh()

        def today_counter_increased(driver):
            current = driver.find_element(*OrderFeedLocators.TODAY_ORDERS_COUNTER).text
            current_val = int(current) if current.isdigit() else 0
            return current_val > today_before

        wait.until(today_counter_increased, message="Счётчик 'Выполнено за сегодня' не изменился")

        today_after = int(browser.find_element(*OrderFeedLocators.TODAY_ORDERS_COUNTER).text)
        assert today_after > today_before

    @allure.title('Номер заказа появляется в разделе "В работе"')
    def test_order_number_appears_in_progress(self, browser, base_url, access_token):
        wait = WebDriverWait(browser, 20)
        
        ingredients_resp = requests.get(f'{base_url}/api/ingredients', timeout=10)
        ingredients = ingredients_resp.json().get('data', [])

        headers = {"Authorization": access_token}
        order_resp = requests.post(
            f'{base_url}/api/orders',
            json={'ingredients': [ingredients[0]['_id'], ingredients[1]['_id']]},
            headers=headers,
            timeout=10
        )
        assert order_resp.status_code == 200, f"API error: {order_resp.text}"
        order_number = order_resp.json().get('order', {}).get('number')
        assert order_number is not None, "Order number not found in API response"

        constructor_page = ConstructorPage(browser)
        if "feed" not in browser.current_url:
            constructor_page.click_order_feed()
            wait.until(EC.url_contains("feed"))

        order_number_locator = OrderFeedLocators.ORDER_NUMBER
        
        wait.until(lambda d: order_number in [
            int(el.text.strip()) for el in d.find_elements(*order_number_locator)
            if el.text.strip().isdigit()
        ], message=f"Заказ №{order_number} не появился в ленте за 20 секунд")

        order_numbers = [
            int(el.text.strip()) for el in browser.find_elements(*order_number_locator)
            if el.text.strip().isdigit()
        ]
        assert order_number in order_numbers