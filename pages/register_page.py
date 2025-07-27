import allure
from pages.base_page import BasePage
from locators.account_page_locators import AccountPageLocators


class RegisterPage(BasePage):

    def register_user(self, name, email, password):
        with allure.step(f"Регистрация пользователя: {name}, {email}"):
            self.find(*AccountPageLocators.NAME_INPUT).send_keys(name)
            self.find(*AccountPageLocators.EMAIL_INPUT).send_keys(email)
            self.find(*AccountPageLocators.PASSWORD_INPUT).send_keys(password)
            self.click(self.find(*AccountPageLocators.REGISTER_BUTTON))

    def wait_for_redirect_to_login(self):
        with allure.step("Ожидание редиректа на страницу логина"):
            return self.wait_until_visible(AccountPageLocators.LOGIN_BUTTON)

    def wait_for_page_to_load(self):
        with allure.step("Ожидание загрузки страницы регистрации"):
            self.wait_until_visible(AccountPageLocators.REGISTER_BUTTON)
