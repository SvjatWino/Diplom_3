import allure
from pages.base_page import BasePage
from locators.account_page_locators import AccountPageLocators


class LoginPage(BasePage):
    def login(self, email, password):
        with allure.step(f"Вход в систему с email: {email}"):
            email_field = self.wait_until_visible(AccountPageLocators.EMAIL_INPUT, timeout=10)
            password_field = self.wait_until_visible(AccountPageLocators.PASSWORD_INPUT, timeout=10)
            login_button = self.wait_until_clickable(AccountPageLocators.LOGIN_BUTTON, timeout=10)

            email_field.clear()
            password_field.clear()

            email_field.send_keys(email)
            password_field.send_keys(password)

            login_button.click()

    def wait_for_login_success(self):
        with allure.step("Ожидание успешной авторизации (кнопка 'Оформить заказ')"):
            return self.wait_until_visible(AccountPageLocators.ORDER_BUTTON, timeout=10)

    def wait_for_page_to_load(self):
        with allure.step("Ожидание загрузки страницы логина (кнопка 'Войти')"):
            self.wait_until_visible(AccountPageLocators.LOGIN_BUTTON, timeout=10)
