import allure
from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from locators.main_page_locators import MainPageLocators as Locators
from urls import BASE_URL


class MainPage(BasePage):
    base_url = BASE_URL

    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_overlay_to_disappear(timeout=30)

    def click_constructor_button(self):
        with allure.step("Клик по кнопке 'Конструктор'"):
            self.wait_and_hide_overlay(timeout=20)
            self.click(self.find(*MainPageLocators.CONSTRUCTOR_BUTTON))

    def click_order_feed_button(self):
        with allure.step("Переход во вкладку 'Лента заказов'"):
            self.wait_and_hide_overlay()
            element = self.find(*MainPageLocators.ORDER_FEED_BUTTON)
            self.driver.execute_script("arguments[0].click();", element)

    def click_first_ingredient(self):
        with allure.step("Клик по первому ингредиенту в списке"):
            self.wait_and_hide_overlay(timeout=20)
            self.wait_until_visible(MainPageLocators.INGREDIENT_CARDS)
            ingredients = self.find_elements(MainPageLocators.INGREDIENT_CARDS)
            self.driver.execute_script("arguments[0].click();", ingredients[0])
            self.wait_until_visible(MainPageLocators.MODAL_HEADER)

    def get_ingredient_counter(self, index=0):
        with allure.step(f"Получение счётчика у ингредиента с индексом {index}"):
            ingredients = self.finds(*MainPageLocators.INGREDIENT_CARD)
            try:
                counter_element = ingredients[index].find_element(*MainPageLocators.INGREDIENT_COUNTER)
                return int(counter_element.text) if counter_element.text else 0
            except (NoSuchElementException, IndexError):
                return 0

    def is_buns_section_displayed(self):
        with allure.step("Проверка отображения секции с булками"):
            return self.find(*MainPageLocators.BUN_SECTION).is_displayed()

    def drag_and_drop_ingredient(self):
        with allure.step("Перетаскивание ингредиента в конструктор"):
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
        with allure.step("Переход на страницу логина"):
            self.click(self.find(*MainPageLocators.LOGIN_BUTTON))

    def go_to_register_page(self):
        with allure.step("Переход на страницу регистрации"):
            self.go_to_login_page()
            self.wait_until_clickable(MainPageLocators.REGISTER_LINK)
            self.click(self.find(*MainPageLocators.REGISTER_LINK))

    def add_ingredient_to_constructor(self):
        with allure.step("Добавление ингредиента в конструктор"):
            self.drag_and_drop_ingredient()

    def click_order_button(self):
        with allure.step("Клик по кнопке 'Оформить заказ'"):
            self.wait_until_clickable(MainPageLocators.ORDER_BUTTON, timeout=20)
            button = self.find(*MainPageLocators.ORDER_BUTTON)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            self.driver.execute_script("arguments[0].click();", button)
            self.wait_for_overlay_to_disappear(timeout=20)

    def submit_order(self):
        with allure.step("Подтверждение заказа и закрытие модального окна"):
            self.wait_until_visible(MainPageLocators.ORDER_NUMBER, timeout=20)
            try:
                self.wait_until_clickable(MainPageLocators.ORDER_MODAL_CLOSE_BUTTON)
                self.click(self.find(*MainPageLocators.ORDER_MODAL_CLOSE_BUTTON))
            except:
                pass

    def wait_for_page_to_load(self):
        self.wait_until_visible(MainPageLocators.CONSTRUCTOR_BUTTON)

    def get_total_orders_count(self):
        with allure.step("Получение общего количества заказов (на странице)"):
            element = self.wait_until_visible(MainPageLocators.TOTAL_ORDERS)
            return int(element.text.replace(" ", ""))

    def go_to_constructor(self):
        with allure.step("Переход в раздел 'Конструктор'"):
            self.click(self.find(*MainPageLocators.CONSTRUCTOR_BUTTON))
            self.wait_for_page_to_load()

    def get_total_orders_count_from_modal(self):
        with allure.step("Получение общего количества заказов из модального окна"):
            element = self.wait_until_visible(MainPageLocators.MODAL_TOTAL_ORDERS)
            return int(element.text.replace(" ", ""))

    def close_order_modal(self):
        with allure.step("Закрытие модального окна заказа"):
            self.wait_and_hide_overlay(timeout=7)
            self.wait_until_clickable(MainPageLocators.ORDER_MODAL_CLOSE_BUTTON)
            self.click(self.find(*MainPageLocators.ORDER_MODAL_CLOSE_BUTTON))

    def get_order_modal_total_orders_count(self, initial_count: int) -> int:
        with allure.step("Ожидание увеличения счётчика заказов в модалке"):
            def text_is_updated(driver):
                try:
                    el = driver.find_element(*MainPageLocators.ORDER_MODAL_TOTAL_ORDERS_COUNT)
                    text = el.text.replace(" ", "")
                    return text.isdigit() and int(text) > initial_count
                except:
                    return False

            self.wait_until(text_is_updated, timeout=20)
            element = self.find(*MainPageLocators.ORDER_MODAL_TOTAL_ORDERS_COUNT)
            return int(element.text.replace(" ", ""))

    def wait_for_order_modal(self, timeout=20):
        self.wait_until_visible(MainPageLocators.ORDER_MODAL_TOTAL_ORDERS_COUNT, timeout=timeout)

    def get_order_number_from_modal(self, timeout=20):
        with allure.step("Получение номера заказа из модального окна"):
            def is_valid_number(driver):
                try:
                    el = driver.find_element(*MainPageLocators.ORDER_NUMBER)
                    text = el.text.strip()
                    return text.isdigit() and len(text) >= 4
                except:
                    return False

            self.wait_until(is_valid_number, timeout=timeout)
            el = self.find(*MainPageLocators.ORDER_NUMBER)
            return el.text.strip()

    def get_final_order_number_from_modal(self, timeout=20) -> str:
        with allure.step("Получение финального номера заказа из модального окна"):
            def is_final_number(driver):
                try:
                    el = driver.find_element(*MainPageLocators.ORDER_MODAL_TOTAL_ORDERS_COUNT)
                    text = el.text.strip()
                    return text.isdigit() and len(text) >= 6
                except:
                    return False

            self.wait_until(is_final_number, timeout=timeout)
            el = self.find(*MainPageLocators.ORDER_MODAL_TOTAL_ORDERS_COUNT)
            return el.text.strip()
