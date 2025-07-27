import allure
from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage


class IngredientModal(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def is_modal_visible(self):
        with allure.step("Проверка, что модальное окно отображается"):
            return self.wait_until_visible(MainPageLocators.MODAL_WINDOW, timeout=7)

    def get_modal_header_text(self):
        with allure.step("Получение заголовка модального окна"):
            element = self.wait_until_visible(MainPageLocators.MODAL_HEADER, timeout=7)
            return element.text

    def close_modal(self):
        with allure.step("Закрытие модального окна"):
            close_button = self.wait_until_clickable(MainPageLocators.CLOSE_BUTTON, timeout=7)
            self.driver.execute_script("arguments[0].click();", close_button)
            self.wait_until_invisible(MainPageLocators.MODAL_WINDOW, timeout=7)

    def is_modal_closed(self):
        with allure.step("Проверка, что модальное окно закрыто"):
            return self.wait_until_invisible(MainPageLocators.MODAL_WINDOW, timeout=7)

    def click_add_button(self):
        with allure.step("Нажатие на кнопку 'Добавить' в модальном окне"):
            add_button = self.wait_until_clickable(MainPageLocators.ADD_BUTTON, timeout=7)
            add_button.click()
