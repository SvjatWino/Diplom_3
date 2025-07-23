from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from locators.main_page_locators import MainPageLocators


class IngredientModal:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 7)

    def is_modal_visible(self):
        return self.wait.until(EC.visibility_of_element_located(MainPageLocators.MODAL_WINDOW))

    def get_modal_header_text(self):
        element = self.wait.until(EC.visibility_of_element_located(MainPageLocators.MODAL_HEADER))
        return element.text

    def close_modal(self):
        close_button = self.wait.until(EC.element_to_be_clickable(MainPageLocators.CLOSE_BUTTON))
        close_button.click()
        self.wait.until(EC.invisibility_of_element_located(MainPageLocators.MODAL_WINDOW))

    def is_modal_closed(self):
        return self.wait.until(EC.invisibility_of_element_located(MainPageLocators.MODAL_WINDOW))

    def click_add_button(self):
        add_button = self.wait.until(EC.element_to_be_clickable(MainPageLocators.ADD_BUTTON))
        add_button.click()
