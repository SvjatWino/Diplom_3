import allure
from locators.order_feed_page_locators import OrderFeedPageLocators
from pages.base_page import BasePage
from urls import BASE_URL


class OrderFeedPage(BasePage):
    base_url = BASE_URL

    def __init__(self, driver):
        super().__init__(driver)

    def wait_for_page_to_load(self):
        with allure.step("Ожидание загрузки страницы ленты заказов"):
            self.wait_until_visible(OrderFeedPageLocators.ORDER_FEED_HEADER)

    def get_total_orders_count(self):
        with allure.step("Получение общего количества заказов"):
            element = self.wait_until_visible(OrderFeedPageLocators.TOTAL_ORDERS)
            return int(element.text.replace(" ", ""))

    def get_today_orders_count(self):
        with allure.step("Получение количества заказов за сегодня"):
            element = self.wait_until_visible(OrderFeedPageLocators.TODAY_ORDERS)
            return int(element.text.replace(" ", ""))

    def is_order_in_progress(self, order_number):
        with allure.step(f"Проверка, что заказ №{order_number} отображается в разделе 'В работе'"):
            elements = self.find_elements(OrderFeedPageLocators.IN_PROGRESS_ORDERS)
            numbers = [el.text.strip() for el in elements]
            return str(order_number) in numbers

    def get_first_order_number(self):
        with allure.step("Получение номера первого заказа в ленте"):
            element = self.wait_until_visible(OrderFeedPageLocators.FIRST_ORDER)
            return element.text.strip()

    def get_today_orders_count_from_feed(self):
        with allure.step("Получение количества заказов за сегодня (из ленты)"):
            element = self.wait_until_visible(OrderFeedPageLocators.TODAY_ORDERS)
            return int(element.text.strip().replace(" ", ""))

    def wait_for_order_in_work(self, order_number: str, timeout: int = 15):
        with allure.step(f"Ожидание появления заказа №{order_number} в работе"):
            self.wait_until(
                lambda driver: order_number in self.get_in_work_order_numbers(),
                timeout=timeout
            )

    def get_in_work_order_numbers(self):
        with allure.step("Получение списка номеров заказов 'В работе'"):
            elements = self.find_elements(OrderFeedPageLocators.IN_WORK_ORDER_NUMBER)
            return [
                el.get_attribute("textContent").replace("\n", "").strip()
                for el in elements
                if el.get_attribute("textContent").replace("\n", "").strip().isdigit()
            ]
