from selenium.webdriver.common.by import By

class AccountPageLocators:
    PAGE_HEADER = (By.XPATH, "//h1[text()='Профиль']")
    PROFILE_TAB = (By.XPATH, "//a[@href='/account/profile']")
    ORDER_HISTORY_TAB = (By.XPATH, "//a[@href='/account/orders']")
    LOGOUT_BUTTON = (By.XPATH, "//button[text()='Выход']")
    ACCOUNT_BUTTON_HEADER = (By.XPATH, "//p[text()='Личный Кабинет']")
    CONSTRUCTOR_BUTTON_HEADER = (By.XPATH, "//p[text()='Конструктор']")
    LOGO_BUTTON = (By.XPATH, "//div[@class='AppHeader_header__logo__2D0X2']")
    LOGIN_FORM = (By.XPATH, "//h2[text()='Вход']")
