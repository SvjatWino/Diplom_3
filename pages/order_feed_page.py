from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from locators.order_feed_page_locators import OrderFeedPageLocators
from pages.base_page import BasePage
from urls import BASE_URL


class OrderFeedPage(BasePage):
    base_url = BASE_URL

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(self.driver, 5)

    def wait_for_page_to_load(self):
        self.wait.until(EC.visibility_of_element_located(OrderFeedPageLocators.ORDER_FEED_HEADER))

    def get_total_orders_count(self):
        element = self.wait.until(EC.visibility_of_element_located(OrderFeedPageLocators.TOTAL_ORDERS))
        return int(element.text.replace(" ", ""))

    def get_today_orders_count(self):
        element = self.wait.until(EC.visibility_of_element_located(OrderFeedPageLocators.TODAY_ORDERS))
        return int(element.text.replace(" ", ""))

    def is_order_in_progress(self, order_number):
        # Получаем список номеров заказов "В работе" и ищем нужный
        elements = self.driver.find_elements(*OrderFeedPageLocators.IN_PROGRESS_ORDERS)
        numbers = [el.text.strip() for el in elements]
        return str(order_number) in numbers

    def get_first_order_number(self):
        element = self.wait.until(EC.visibility_of_element_located(OrderFeedPageLocators.FIRST_ORDER))
        return element.text.strip()

    def get_today_orders_count_from_feed(self):
        element = self.wait.until(EC.visibility_of_element_located(OrderFeedPageLocators.TODAY_ORDERS))
        return int(element.text.strip().replace(" ", ""))

    def wait_for_order_in_work(self, order_number: str, timeout: int = 15):
        self.wait.until(
            lambda driver: order_number in self.get_in_work_order_numbers()
        )

    def get_in_work_order_numbers(self):
        elements = self.driver.find_elements(*OrderFeedPageLocators.IN_WORK_ORDER_NUMBER)
        return [
            el.get_attribute("textContent").replace("\n", "").strip()
            for el in elements
            if el.get_attribute("textContent").replace("\n", "").strip().isdigit()
        ]

