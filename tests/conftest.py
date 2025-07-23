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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from urls import BASE_URL
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from locators.main_page_locators import MainPageLocators
from selenium.common.exceptions import ElementClickInterceptedException


MODAL_OVERLAY = (By.CLASS_NAME, "Modal_modal_overlay__x2ZCr")


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
    try:
        close_button = driver.find_element(By.CLASS_NAME, "Modal_modal_close__TnseC")
        close_button.click()
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "Modal_modal__P3_V5"))
        )
    except (NoSuchElementException, TimeoutException):
        pass

@pytest.fixture
def user_data():
    login = f"autotest_{uuid.uuid4().hex[:8]}@example.com"
    password = "123456"

    # Регистрация пользователя через API
    url = "https://stellarburgers.nomoreparties.site/api/auth/register"
    payload = {
        "email": login,
        "password": password,
        "name": "Test User"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200, "Не удалось создать пользователя через API"

    yield {"email": login, "password": password}

    # Удаление пользователя после теста
    token = response.json().get("accessToken")
    if token:
        headers = {"Authorization": token}
        requests.delete("https://stellarburgers.nomoreparties.site/api/auth/user", headers=headers)

@pytest.fixture
def authorized_driver(driver):
    driver.get(BASE_URL)

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Modal_modal_overlay__x2ZCr"))
        )
        WebDriverWait(driver, 10).until_not(
            EC.presence_of_element_located((By.CLASS_NAME, "Modal_modal_overlay__x2ZCr"))
        )
    except TimeoutException:
        pass

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(MainPageLocators.LOGIN_ACCOUNT_BUTTON)
        )
        driver.find_element(*MainPageLocators.LOGIN_ACCOUNT_BUTTON).click()
    except (TimeoutException, ElementClickInterceptedException):
        element = driver.find_element(*MainPageLocators.LOGIN_ACCOUNT_BUTTON)
        driver.execute_script("arguments[0].click();", element)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Зарегистрироваться"))
    ).click()

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


@pytest.fixture
def base_url():
    return BASE_URL
