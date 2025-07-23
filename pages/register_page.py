from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class RegisterPage(BasePage):
    NAME_INPUT = (By.XPATH, "//label[text()='Имя']/following-sibling::input")
    EMAIL_INPUT = (By.XPATH, "//label[text()='Email']/following-sibling::input")
    PASSWORD_INPUT = (By.XPATH, "//label[text()='Пароль']/following-sibling::input")
    REGISTER_BUTTON = (By.XPATH, "//button[text()='Зарегистрироваться']")

    def register_user(self, name, email, password):
        self.find(*self.NAME_INPUT).send_keys(name)
        self.find(*self.EMAIL_INPUT).send_keys(email)
        self.find(*self.PASSWORD_INPUT).send_keys(password)
        self.click(self.find(*self.REGISTER_BUTTON))

    def wait_for_redirect_to_login(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.visibility_of_element_located((By.XPATH, "//button[text()='Войти']")))

    def wait_for_page_to_load(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[text()='Зарегистрироваться']"))
        )
