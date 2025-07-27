import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import requests
import uuid
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage
from urls import BASE_URL, REGISTER_API_URL, DELETE_USER_API_URL



@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = request.param

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.maximize_window()
    driver.implicitly_wait(15)
    driver.get(BASE_URL)
    yield driver
    driver.quit()


@pytest.fixture(autouse=True)
def close_ingredient_modal_after_test(driver):
    yield
    base_page = BasePage(driver)
    try:
        close_button_locator = (By.CLASS_NAME, "Modal_modal_close__TnseC")
        close_button = base_page.wait_until_visible(close_button_locator, timeout=5)
        close_button.click()
        base_page.wait_until_invisible(close_button_locator, timeout=5)
    except (TimeoutException, NoSuchElementException):
        pass


@pytest.fixture
def user_data():
    login = f"autotest_{uuid.uuid4().hex[:8]}@example.com"
    password = "123456"

    # Регистрация пользователя через API
    payload = {
        "email": login,
        "password": password,
        "name": "Test User"
    }
    response = requests.post(REGISTER_API_URL, json=payload)
    assert response.status_code == 200, "Не удалось создать пользователя через API"

    yield {"email": login, "password": password}

    # Удаление пользователя после теста
    token = response.json().get("accessToken")
    if token:
        headers = {"Authorization": token}
        requests.delete(DELETE_USER_API_URL, headers=headers)


@pytest.fixture
def authorized_driver(driver):
    base_page = BasePage(driver)
    driver.get(BASE_URL)

    try:
        base_page.wait_until_visible(MainPageLocators.MODAL_OVERLAY, timeout=5)
        base_page.wait_until_invisible(MainPageLocators.MODAL_OVERLAY, timeout=10)
    except TimeoutException:
        pass

    try:
        base_page.click_by_locator(MainPageLocators.LOGIN_ACCOUNT_BUTTON, timeout=10)
    except (TimeoutException, ElementClickInterceptedException):
        base_page.click_element_via_js(MainPageLocators.LOGIN_ACCOUNT_BUTTON)

    base_page.wait_until_clickable((By.LINK_TEXT, "Зарегистрироваться"), timeout=10).click()

    register_page = RegisterPage(driver)
    register_page.wait_for_page_to_load()
    unique_email = f"test_{uuid.uuid4().hex[:8]}@mail.ru"
    password = "123456"
    name = "TestUser"
    register_page.register_user(name, unique_email, password)

    login_page = LoginPage(driver)
    login_page.wait_for_page_to_load()
    login_page.login(unique_email, password)
    login_page.wait_for_login_success()

    driver.get(BASE_URL)

    main_page = MainPage(driver)
    main_page.wait_for_page_to_load()

    yield main_page
