import allure
import requests
from pages.constructor_page import ConstructorPage
from pages.order_page import OrderPage
from urls import Urls


@allure.feature('Лента заказов')
class TestOrderFeed:

    @allure.title('Переход по клику на "Лента заказов"')
    def test_click_order_feed(self, browser):
        constructor_page = ConstructorPage(browser)
        constructor_page.click_order_feed()
        
        order_page = OrderPage(browser)
        assert order_page.wait_for_feed_page()
        assert "feed" in browser.current_url.lower()

    @allure.title('Счётчик "Выполнено за всё время" увеличивается')
    def test_total_orders_counter_increases(self, browser, access_token):
        constructor_page = ConstructorPage(browser)
        constructor_page.click_order_feed()
        
        order_page = OrderPage(browser)
        total_before = order_page.get_total_orders_count()
        
        
        ingredients_resp = requests.get(f'{Urls.BASE_URL}/api/ingredients', timeout=10, verify=False)
        ingredients = ingredients_resp.json().get('data', [])[:2]
        ingredient_ids = [ing['_id'] for ing in ingredients]
        
        headers = {"Authorization": access_token}
        requests.post(
            f'{Urls.BASE_URL}/api/orders',
            json={'ingredients': ingredient_ids},
            headers=headers,
            timeout=10,
            verify=False
        )
        
        browser.refresh()
        
        total_after = order_page.get_total_orders_count()
        assert total_after > total_before

    @allure.title('Счётчик "Выполнено за сегодня" увеличивается')
    def test_today_orders_counter_increases(self, browser, access_token):
        constructor_page = ConstructorPage(browser)
        constructor_page.click_order_feed()
        
        order_page = OrderPage(browser)
        today_before = order_page.get_today_orders_count()
        
        # Создаём заказ через API
        ingredients_resp = requests.get(f'{Urls.BASE_URL}/api/ingredients', timeout=10, verify=False)
        ingredients = ingredients_resp.json().get('data', [])[:2]
        ingredient_ids = [ing['_id'] for ing in ingredients]
        
        headers = {"Authorization": access_token}
        requests.post(
            f'{Urls.BASE_URL}/api/orders',
            json={'ingredients': ingredient_ids},
            headers=headers,
            timeout=10,
            verify=False
        )
        
        browser.refresh()
        
        today_after = order_page.get_today_orders_count()
        assert today_after > today_before

    @allure.title('Номер заказа появляется в разделе "В работе"')
    def test_order_number_appears_in_progress(self, browser, access_token):
        # Создаём заказ через API
        ingredients_resp = requests.get(f'{Urls.BASE_URL}/api/ingredients', timeout=10, verify=False)
        ingredients = ingredients_resp.json().get('data', [])
        
        headers = {"Authorization": access_token}
        order_resp = requests.post(
            f'{Urls.BASE_URL}/api/orders',
            json={'ingredients': [ingredients[0]['_id'], ingredients[1]['_id']]},
            headers=headers,
            timeout=10,
            verify=False
        )
        order_number = order_resp.json().get('order', {}).get('number')
        assert order_number is not None, "Order number not found in API response"
        
        constructor_page = ConstructorPage(browser)
        constructor_page.click_order_feed()
        
        order_page = OrderPage(browser)
        order_page.wait_for_feed_page()
        order_page.wait_for_order_number(order_number)
        
        assert order_page.is_order_number_displayed(order_number)