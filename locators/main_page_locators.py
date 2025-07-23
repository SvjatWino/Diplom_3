from selenium.webdriver.common.by import By

class MainPageLocators:
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[text()='Лента Заказов']")
    INGREDIENT_CARD = (By.XPATH, "//a[contains(@class, 'BurgerIngredient_ingredient') and .//p[text()='Флюоресцентная булка R2-D3']]")
    INGREDIENT_CARDS = (By.XPATH, "//a[contains(@class, 'BurgerIngredient_ingredient')]")  # <--- добавлено
    INGREDIENT_COUNTER = (By.XPATH, ".//div[contains(@class, 'counter_counter')]")
    MODAL_WINDOW = (By.XPATH, "//div[contains(@class, 'Modal_modal__container')]")
    MODAL_HEADER = (By.XPATH, "//h2[text()='Детали ингредиента']")
    MODAL_TITLE = (By.XPATH, "//h2[text()='Детали ингредиента']")  # <--- добавлено
    CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
    ADD_BUTTON = (By.XPATH, "//button[contains(text(), 'Добавить')]")
    BUN_SECTION = (By.XPATH, "//h2[text()='Булки']")
    CONSTRUCTOR_DROP_AREA = (By.CLASS_NAME, "constructor-element_pos_top")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти в аккаунт']")
    REGISTER_LINK = (By.XPATH, "//a[text()='Зарегистрироваться']")
    LOGIN_ACCOUNT_BUTTON = (By.XPATH, "//p[text()='Личный Кабинет']")
    ORDER_NUMBER = (By.XPATH, "//h2[contains(@class, 'Modal_modal__title') and string-length(text()) > 0]")
    ORDER_MODAL_CLOSE_BUTTON = (By.XPATH,
                                "//div[contains(@class, 'Modal_modal__container')]//button[contains(@class, 'Modal_modal__close')]")
    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")
    MODAL_TOTAL_ORDERS = (By.XPATH,
                          "//p[contains(@class, 'OrderDetails_total__') or contains(text(),'выполнено за всё время')]")
    ORDER_MODAL_TOTAL_ORDERS_COUNT = (
        By.XPATH,
        "//h2[contains(@class, 'Modal_modal__title_shadow') and contains(@class, 'text_type_digits-large')]"
    )
    TOTAL_ORDERS = (By.CSS_SELECTOR, "p.OrderFeed_number__2MbrQ")
    ORDER_MODAL_OVERLAY = (By.CLASS_NAME, "Modal_modal_overlay__x2ZCr")
    TODAY_ORDERS_COUNT = (By.XPATH,
                          "//p[text()='Выполнено за сегодня:']/following-sibling::p[contains(@class, 'text_type_digits-large')]")
