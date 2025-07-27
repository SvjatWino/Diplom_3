from selenium.webdriver.common.by import By

class OrderFeedPageLocators:
    PAGE_HEADER = (By.XPATH, "//h1[text()='Лента заказов']")
    ORDERS_LIST = (By.XPATH, "//ul[contains(@class, 'OrderFeed_order_list__')]")
    FIRST_ORDER = (By.XPATH, "(//ul[contains(@class, 'OrderFeed_order_list__')]//li)[1]")
    TOTAL_ORDERS = (By.XPATH, "//p[text()='Выполнено за все время:']/following-sibling::p")
    TODAY_ORDERS = (By.XPATH, "//p[text()='Выполнено за сегодня:']/following-sibling::p")
    IN_PROGRESS_ORDERS = (By.XPATH, "//div[contains(@class, 'OrderFeed_order_status__column')]/ul")
    ORDER_FEED_HEADER = (By.XPATH, "//h2[text()='Лента заказов']")
    TOTAL_ORDERS_COUNT = (By.XPATH, "//p[contains(text(),'Выполнено за всё время')]/following-sibling::p")
    IN_WORK_ORDER_NUMBER = (
        By.CSS_SELECTOR,
        "ul.OrderFeed_orderListReady__1YFem li.text_type_digits-default"
    )
    READY_ORDERS_LIST = (By.CSS_SELECTOR, "ul.OrderFeed_orderListReady__1YFem li.text_type_digits-default")
