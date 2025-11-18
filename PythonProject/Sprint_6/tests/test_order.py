# tests/test_order.py
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.main_page import MainPage
from pages.order_page import OrderPage


# Два набора данных + две точки входа (верхняя и нижняя кнопка «Заказать»)
ORDER_DATA = [
    # (index кнопки, имя, фамилия, адрес, телефон, дата, комментарий)
    (0, "Иван", "Иванов", "ул. Тестовая, д. 1", "+79990000001", "30.11.2025", "Позвоните заранее"),
    (1, "Пётр", "Петров", "пр. Учебный, д. 2", "+79990000002", "01.12.2025", "Позвоните за 10 минут"),
]


@pytest.mark.parametrize(
    "button_index, name, surname, address, phone, date_text, comment",
    ORDER_DATA,
)
def test_make_order_positive_flow(driver, button_index, name, surname, address, phone, date_text, comment):
    main_page = MainPage(driver)
    # нажимаем нужную кнопку «Заказать» (0 — верхняя, 1 — нижняя)
    main_page.click_order_button(button_index)

    order_page = OrderPage(driver)
    order_page.fill_first_step(name, surname, address, phone)
    order_page.fill_second_step(date_text, comment)

    assert order_page.is_success_modal_visible()


def test_click_scooter_logo_returns_to_main(driver):
    # Открываем страницу заказа через кнопку "Заказать" сверху
    main_page = MainPage(driver)
    main_page.click_order_button(0)

    # На странице заказа жмём логотип "Самоката"
    order_page = OrderPage(driver)
    order_page.click_scooter_logo()

    # Должны оказаться на главной странице самоката
    assert "qa-scooter.praktikum-services.ru" in order_page.get_current_url()


def test_click_yandex_logo_opens_dzen(driver):
    main_page = MainPage(driver)

    # кликаем по логотипу Яндекса
    main_page.click_yandex_logo()

    # ждём, пока откроется вторая вкладка
    WebDriverWait(driver, 10).until(
        lambda d: len(d.window_handles) > 1
    )

    # переключаемся на новую вкладку
    driver.switch_to.window(driver.window_handles[1])

    # ждём, пока урл станет дзеновским
    WebDriverWait(driver, 15).until(
        EC.url_contains("dzen")
    )

    assert "dzen.ru" in driver.current_url
