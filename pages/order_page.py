import allure
from pages.base_page import BasePage
from locators.locators import OrderFeedLocators


class OrderPage(BasePage):
    """Page Object для страницы ленты заказов"""
    
    @allure.step('Ожидание перехода на страницу ленты заказов')
    def wait_for_feed_page(self):
        return self.wait_for_url_contains('feed')
    
    @allure.step('Получение значения счётчика "Выполнено за всё время"')
    def get_total_orders_count(self):
        text = self.get_text(OrderFeedLocators.TOTAL_ORDERS_COUNTER)
        return int(text) if text.isdigit() else 0
    
    @allure.step('Получение значения счётчика "Выполнено за сегодня"')
    def get_today_orders_count(self):
        text = self.get_text(OrderFeedLocators.TODAY_ORDERS_COUNTER)
        return int(text) if text.isdigit() else 0
    
    @allure.step('Получение списка номеров заказов в работе')
    def get_orders_in_progress(self):
        elements = self.driver.find_elements(*OrderFeedLocators.ORDER_NUMBER)
        numbers = []
        for el in elements:
            text = el.text.strip()
            if text and text.isdigit():
                numbers.append(int(text))
        return numbers
    
    @allure.step('Ожидание появления заказа с номером {order_number} в ленте')
    def wait_for_order_number(self, order_number, timeout=20):
        self.wait.until(lambda d: order_number in self.get_orders_in_progress(),
                        message=f"Заказ №{order_number} не появился в ленте за {timeout} секунд")
    
    @allure.step('Проверка, что заказ с номером {order_number} появился в ленте')
    def is_order_number_displayed(self, order_number):
        return order_number in self.get_orders_in_progress()