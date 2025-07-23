from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def open(self, url):
        self.driver.get(url)

    def find(self, by, value):
        return self.driver.find_element(by, value)

    def finds(self, by, value):
        return self.driver.find_elements(by, value)

    def click(self, element):
        element.click()

    def is_visible(self, by, value):
        try:
            return self.find(by, value).is_displayed()
        except:
            return False

    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def wait_for_overlay_to_disappear(self, timeout=10):
        overlay_locator = (By.CLASS_NAME, "Modal_modal_overlay__x2ZCr")
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(overlay_locator)
        )

    def wait_and_hide_overlay(self, timeout=10):
        """
        Ожидает исчезновения overlay, если timeout — принудительно скрывает через JS
        """
        overlay_locator = (By.CLASS_NAME, "Modal_modal_overlay__x2ZCr")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(overlay_locator)
            )
        except TimeoutException:
            self.driver.execute_script("""
                const overlays = document.getElementsByClassName('Modal_modal_overlay__x2ZCr');
                for (let overlay of overlays) {
                    overlay.style.display = 'none';
                }
            """)

    def wait_for_text_in_elements(self, locator, text, timeout=10):
        """Ждёт, пока текст появится в одном из элементов, найденных по локатору"""
        WebDriverWait(self.driver, timeout).until(
            lambda driver: any(
                text in el.text for el in driver.find_elements(*locator)
            ),
            message=f"Текст '{text}' не найден ни в одном из элементов {locator} в течение {timeout} секунд"
        )