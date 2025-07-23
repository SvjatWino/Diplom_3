import allure
import pytest
from pages.main_page import MainPage
from pages.ingredient_modal import IngredientModal


@allure.suite("Главная страница")
@allure.sub_suite("Основной функционал и интерфейс")
@allure.epic("Основной функционал главной страницы")
class TestMainPage:

    @allure.title("Переход по клику на 'Конструктор'")
    def test_go_to_constructor(self, driver):
        page = MainPage(driver)

        with allure.step("Переходим в 'Ленту заказов'"):
            page.click_order_feed_button()

        with allure.step("Кликаем на 'Конструктор'"):
            page.click_constructor_button()

        with allure.step("Проверяем, что раздел 'Булки' отображается"):
            assert page.is_buns_section_displayed(), "Раздел 'Булки' не отображается"

    @allure.title("Переход по клику на раздел 'Лента заказов'")
    def test_go_to_order_feed(self, driver):
        page = MainPage(driver)

        with allure.step("Кликаем на 'Лента заказов'"):
            page.click_order_feed_button()

        with allure.step("Проверяем, что URL изменился на /feed"):
            assert "/feed" in driver.current_url, "URL не содержит '/feed' после перехода"

    @allure.title("При клике на ингредиент появляется модальное окно с деталями")
    def test_ingredient_modal_opens(self, driver):
        page = MainPage(driver)

        with allure.step("Кликаем по первому ингредиенту"):
            page.click_first_ingredient()

        with allure.step("Проверяем, что модальное окно открылось"):
            modal = IngredientModal(driver)
            assert modal.is_modal_visible(), "Модальное окно с ингредиентом не открылось"

    @allure.title("Модальное окно ингредиента закрывается по крестику")
    def test_close_ingredient_modal(self, driver):
        page = MainPage(driver)

        with allure.step("Открываем модальное окно ингредиента"):
            page.click_first_ingredient()
            modal = IngredientModal(driver)

        with allure.step("Закрываем модальное окно"):
            modal.close_modal()

        with allure.step("Проверяем, что модалка закрылась"):
            assert modal.is_modal_closed(), "Модальное окно не закрылось"

    @allure.title("Добавление ингредиента увеличивает счётчик")
    def test_ingredient_counter_increases(self, driver):
        page = MainPage(driver)

        with allure.step("Получаем текущее значение счётчика"):
            initial = page.get_ingredient_counter()

        with allure.step("Перетаскиваем ингредиент в конструктор"):
            page.drag_and_drop_ingredient()

        with allure.step("Проверяем, что счётчик увеличился"):
            updated = page.get_ingredient_counter()
            assert updated == initial + 2, f"Булка должна добавлять 2 позиции: было {initial}, стало {updated}"
