import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locators.main_page_locators import MainPageLocators
from selenium.webdriver.common.by import By



class BasePage:
    def __init__(self, driver):
        self.driver = driver
        with allure.step("Инициализация BasePage и WebDriverWait"):
            self.wait = WebDriverWait(driver, 30)

    def open(self, url):
        with allure.step(f"Открытие страницы: {url}"):
            self.driver.get(url)

    def find(self, by, value):
        with allure.step(f"Поиск элемента по: ({by}, {value})"):
            return self.driver.find_element(by, value)

    def finds(self, by, value):
        with allure.step(f"Поиск всех элементов по: ({by}, {value})"):
            return self.driver.find_elements(by, value)

    def click(self, element):
        with allure.step("Клик по элементу"):
            element.click()

    def click_by_locator(self, locator, timeout=20):
        with allure.step(f"Ожидание кликабельности и клик по локатору: {locator}"):
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            with allure.step("Выполнение клика по найденному элементу"):
                element.click()

    def is_visible(self, by, value):
        with allure.step(f"Проверка видимости элемента: ({by}, {value})"):
            try:
                return self.find(by, value).is_displayed()
            except Exception:
                with allure.step("Элемент не найден или не видим"):
                    return False

    def find_element(self, locator):
        with allure.step(f"Ожидание видимости элемента по локатору: {locator}"):
            return self.wait_until_visible(locator)

    def find_elements(self, locator):
        with allure.step(f"Поиск всех элементов по локатору: {locator}"):
            return self.driver.find_elements(*locator)

    def wait_until_visible(self, locator, timeout=20):
        with allure.step(f"Ожидание видимости элемента: {locator}"):
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )

    def wait_until_clickable(self, locator, timeout=20):
        with allure.step(f"Ожидание кликабельности элемента: {locator}"):
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )

    def wait_until_invisible(self, locator, timeout=20):
        with allure.step(f"Ожидание, что элемент станет невидим: {locator}"):
            return WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )

    def wait_until_invisible_by_locator(self, locator, timeout=20):
        with allure.step(f"Вызов ожидания невидимости элемента по локатору: {locator}"):
            return self.wait_until_invisible(locator, timeout)

    def wait_until(self, condition_function, timeout=20):
        with allure.step("Ожидание пользовательского условия"):
            return WebDriverWait(self.driver, timeout).until(condition_function)

    def wait_for_overlay_to_disappear(self, timeout=20):
        with allure.step("Ожидание исчезновения overlay"):
            overlay_locator = MainPageLocators.MODAL_OVERLAY
            self.wait_until_invisible(overlay_locator, timeout)

    def wait_and_hide_overlay(self, timeout=15):
        with allure.step("Удаление overlay (всегда)"):
            overlay_locator = (By.CLASS_NAME, "Modal_modal_overlay__x2ZCr")

            try:
                self.wait_until_invisible(overlay_locator, timeout)
            except TimeoutException:
                pass  # Даже если не исчез — продолжаем

            # Принудительное удаление overlay
            self.driver.execute_script("""
                const overlays = document.getElementsByClassName('Modal_modal_overlay__x2ZCr');
                for (let overlay of overlays) {
                    overlay.remove();
                }
            """)

    def wait_for_text_in_elements(self, locator, text, timeout=20):
        with allure.step(f"Ожидание текста '{text}' в элементах по локатору: {locator}"):
            self.wait_until(
                lambda driver: any(
                    text in el.text for el in driver.find_elements(*locator)
                ),
                timeout=timeout
            )

    def click_element_via_js(self, locator, timeout=20):
        with allure.step(f"Клик по элементу через JS по локатору: {locator}"):
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            self.driver.execute_script("arguments[0].click();", element)
