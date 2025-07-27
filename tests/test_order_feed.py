import allure
from urls import FEED_URL, BASE_URL
from pages.order_feed_page import OrderFeedPage


@allure.suite("Лента заказов")
@allure.sub_suite("Проверка отображения и счётчиков заказов")
class TestOrderFeed:

    @allure.title("Проверка увеличения счётчика общего количества заказов после оформления нового заказа")
    def test_total_orders_counter_increases(self, authorized_driver):
        main_page = authorized_driver

        with allure.step("Перейти на страницу 'Лента заказов' и получить начальное значение счётчика"):
            main_page.open(FEED_URL)
            initial_count = main_page.get_total_orders_count()

        with allure.step("Перейти на страницу 'Конструктор'"):
            main_page.open(BASE_URL)

        with allure.step("Добавить булку и ингредиенты в конструктор"):
            main_page.drag_and_drop_ingredient()

        with allure.step("Оформить заказ и получить обновлённое значение счётчика из модального окна"):
            main_page.click_order_button()
            main_page.wait_for_order_modal(timeout=15)
            updated_count = main_page.get_order_modal_total_orders_count(initial_count)
            main_page.close_order_modal()

        with allure.step("Проверить, что счётчик увеличился минимум на 1"):
            assert updated_count >= initial_count + 1, (
                f"Ожидалось, что счётчик заказов ({updated_count}) минимум на 1 больше начального ({initial_count})"
            )

    @allure.title("Проверка увеличения счётчика 'Выполнено за сегодня' после оформления нового заказа")
    def test_today_orders_counter_increases(self, authorized_driver):
        main_page = authorized_driver
        feed_page = OrderFeedPage(main_page.driver)

        with allure.step("Перейти на страницу 'Лента заказов' и получить начальное значение счётчика"):
            main_page.open(FEED_URL)
            initial_count = feed_page.get_today_orders_count_from_feed()

        with allure.step("Перейти на страницу 'Конструктор'"):
            main_page.open(BASE_URL)

        with allure.step("Добавить булку и ингредиенты в конструктор"):
            main_page.drag_and_drop_ingredient()

        with allure.step("Оформить заказ"):
            main_page.click_order_button()
            main_page.wait_for_order_modal(timeout=15)
            main_page.close_order_modal()

        with allure.step("Перейти на страницу 'Лента заказов' и получить обновлённое значение счётчика"):
            main_page.open(FEED_URL)
            updated_count = feed_page.get_today_orders_count_from_feed()

        with allure.step("Проверить, что счётчик 'Выполнено за сегодня' увеличился минимум на 1"):
            assert updated_count >= initial_count + 1, (
                f"Ожидалось, что счётчик 'Выполнено за сегодня' ({updated_count}) минимум на 1 больше начального ({initial_count})"
            )

    @allure.title("Проверка появления номера оформленного заказа в разделе 'В работе'")
    def test_order_number_appears_in_work_section(self, authorized_driver):
        main_page = authorized_driver

        with allure.step("Перейти на страницу 'Конструктор' и добавить булку с ингредиентами"):
            main_page.open(BASE_URL)
            main_page.drag_and_drop_ingredient()

        with allure.step("Оформить заказ и получить номер из модального окна"):
            main_page.click_order_button()
            main_page.wait_for_order_modal(timeout=7)
            order_number = main_page.get_final_order_number_from_modal()
            main_page.close_order_modal()

        formatted_order_number = str(order_number).zfill(7)

        with allure.step("Перейти на страницу 'Лента заказов'"):
            order_feed = OrderFeedPage(main_page.driver)
            order_feed.open(FEED_URL)

        with allure.step("Ожидание появления номера заказа в разделе 'В работе'"):
            order_feed.wait_for_order_in_work(formatted_order_number)

        with allure.step("Проверка, что номер заказа присутствует в разделе 'В работе'"):
            order_numbers = order_feed.get_in_work_order_numbers()
            assert formatted_order_number in order_numbers, (
                f"Номер заказа {formatted_order_number} не найден. "
                f"Текущие номера в работе: {order_numbers}"
            )
