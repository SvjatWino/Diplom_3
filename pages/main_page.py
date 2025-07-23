from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators
from selenium.webdriver import ActionChains
from locators.main_page_locators import MainPageLocators as Locators
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from urls import BASE_URL
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class MainPage(BasePage):
    base_url = BASE_URL

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.wait_for_overlay_to_disappear()

    def click_constructor_button(self):
        self.click(self.find(*MainPageLocators.CONSTRUCTOR_BUTTON))

    def click_order_feed_button(self):
        self.wait_and_hide_overlay(timeout=10)
        self.click(self.find(*MainPageLocators.ORDER_FEED_BUTTON))

    def click_first_ingredient(self):
        self.wait_and_hide_overlay(timeout=10)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(MainPageLocators.INGREDIENT_CARDS)
        )

        ingredients = self.driver.find_elements(*MainPageLocators.INGREDIENT_CARDS)
        ingredients[0].click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(MainPageLocators.MODAL_HEADER)
        )

    def get_ingredient_counter(self, index=0):
        ingredients = self.finds(*MainPageLocators.INGREDIENT_CARD)
        try:
            counter_element = ingredients[index].find_element(*MainPageLocators.INGREDIENT_COUNTER)
            return int(counter_element.text) if counter_element.text else 0
        except (NoSuchElementException, IndexError):
            return 0

    def is_buns_section_displayed(self):
        return self.find(*MainPageLocators.BUN_SECTION).is_displayed()

    def drag_and_drop_ingredient(self):
        ingredient = self.find_element(Locators.INGREDIENT_CARD)
        target = self.find_element(Locators.CONSTRUCTOR_DROP_AREA)

        browser_name = self.driver.capabilities.get("browserName", "").lower()

        if browser_name == "firefox":
            js_code = """
            const dataTransfer = new DataTransfer();

            const fireEvent = (element, type, dataTransfer) => {
                const event = new DragEvent(type, {
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: dataTransfer
                });
                element.dispatchEvent(event);
            };

            const source = arguments[0];
            const target = arguments[1];

            fireEvent(source, 'dragstart', dataTransfer);
            fireEvent(target, 'dragenter', dataTransfer);
            fireEvent(target, 'dragover', dataTransfer);
            fireEvent(target, 'drop', dataTransfer);
            fireEvent(source, 'dragend', dataTransfer);
            """
            self.driver.execute_script(js_code, ingredient, target)
        else:
            ActionChains(self.driver).drag_and_drop(ingredient, target).perform()

    def go_to_login_page(self):
        self.click(self.find(*MainPageLocators.LOGIN_BUTTON))

    def go_to_register_page(self):
        self.go_to_login_page()
        self.wait.until(EC.element_to_be_clickable(MainPageLocators.REGISTER_LINK))
        self.click(self.find(*MainPageLocators.REGISTER_LINK))

    def add_ingredient_to_constructor(self):
        self.drag_and_drop_ingredient()

    def click_order_button(self):
        button = self.wait.until(EC.element_to_be_clickable(MainPageLocators.ORDER_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        self.driver.execute_script("arguments[0].click();", button)
        self.wait_for_overlay_to_disappear(timeout=15)

    def submit_order(self):
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(MainPageLocators.ORDER_NUMBER)
        )

        try:
            close_button = self.wait.until(
                EC.element_to_be_clickable(MainPageLocators.ORDER_MODAL_CLOSE_BUTTON)
            )
            close_button.click()
        except:
            pass

    def wait_for_page_to_load(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(MainPageLocators.CONSTRUCTOR_BUTTON)
        )

    def get_total_orders_count(self):
        element = self.wait.until(EC.visibility_of_element_located(MainPageLocators.TOTAL_ORDERS))
        return int(element.text.replace(" ", ""))

    def go_to_constructor(self):
        self.click(self.find(*MainPageLocators.CONSTRUCTOR_BUTTON))
        self.wait_for_page_to_load()

    def get_total_orders_count_from_modal(self):
        element = self.wait.until(
            EC.visibility_of_element_located(MainPageLocators.MODAL_TOTAL_ORDERS)
        )
        return int(element.text.replace(" ", ""))

    def close_order_modal(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.invisibility_of_element_located(MainPageLocators.ORDER_MODAL_OVERLAY)
            )
        except TimeoutException:
            pass

        close_btn = self.wait.until(
            EC.element_to_be_clickable(MainPageLocators.ORDER_MODAL_CLOSE_BUTTON)
        )
        close_btn.click()

    def get_order_modal_total_orders_count(self, initial_count: int) -> int:
        long_wait = WebDriverWait(self.driver, 15)

        def text_is_updated(driver):
            try:
                el = driver.find_element(*MainPageLocators.ORDER_MODAL_TOTAL_ORDERS_COUNT)
                text = el.text.replace(" ", "")
                return text.isdigit() and int(text) > initial_count
            except:
                return False

        long_wait.until(text_is_updated)

        element = self.driver.find_element(*MainPageLocators.ORDER_MODAL_TOTAL_ORDERS_COUNT)
        return int(element.text.replace(" ", ""))

    def wait_for_order_modal(self, timeout=15):
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(MainPageLocators.ORDER_MODAL_TOTAL_ORDERS_COUNT)
        )

    def wait_for_overlay_to_disappear(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "Modal_modal_overlay__x2ZCr"))
        )

    def get_order_number_from_modal(self, timeout=15):
        """Ждёт появления валидного номера заказа в модальном окне и возвращает его"""

        def is_valid_number(driver):
            try:
                el = driver.find_element(*MainPageLocators.ORDER_NUMBER)
                text = el.text.strip()
                return text.isdigit() and len(text) >= 4  # или == 7, если всегда 7-значный
            except:
                return False

        WebDriverWait(self.driver, timeout).until(is_valid_number)
        el = self.driver.find_element(*MainPageLocators.ORDER_NUMBER)
        return el.text.strip()

    def get_final_order_number_from_modal(self, timeout=15) -> str:
        """
        Ждёт появления валидного (финального) номера заказа в модальном окне и возвращает его.
        """
        wait = WebDriverWait(self.driver, timeout)

        def is_final_number(driver):
            try:
                el = driver.find_element(*MainPageLocators.ORDER_MODAL_TOTAL_ORDERS_COUNT)
                text = el.text.strip()
                return text.isdigit() and len(text) >= 6
            except:
                return False

        wait.until(is_final_number)

        el = self.driver.find_element(*MainPageLocators.ORDER_MODAL_TOTAL_ORDERS_COUNT)
        return el.text.strip()