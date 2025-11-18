from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class OrderPage(BasePage):
    # ---------- Шаг 1. Для кого самокат ----------

    # поля ввода
    FIRST_NAME_FIELD = (By.XPATH, "//input[@placeholder='* Имя']")
    LAST_NAME_FIELD = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS_FIELD = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_INPUT = (By.XPATH, "//input[@placeholder='* Станция метро']")
    METRO_FIRST_OPTION = (By.CLASS_NAME, "Order_SelectOption__82bhS")
    PHONE_FIELD = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")

    # кнопка «Далее»
    NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")

    # ---------- Шаг 2. Про аренду ----------

    DATE_INPUT = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    # срок аренды
    RENT_DROPDOWN = (By.CLASS_NAME, "Dropdown-placeholder")
    RENT_OPTION_SUTKI = (By.XPATH, "//div[@class='Dropdown-option' and text()='сутки']")
    # цвет
    COLOR_BLACK_CHECKBOX = (By.ID, "black")
    # комментарий
    COMMENT_INPUT = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")

    # кнопки оформления заказа
    ORDER_BUTTON = (By.XPATH, "//div[contains(@class,'Order_Buttons')]/button[text()='Заказать']")
    YES_BUTTON = (By.XPATH, "//button[text()='Да']")

    # модалка об успешном заказе
    SUCCESS_MODAL = (By.CLASS_NAME, "Order_Modal__YZ-d3")

    # ---------- Логотипы в шапке ----------

    SCOOTER_LOGO = (By.CLASS_NAME, "Header_LogoScooter__3lsAR")
    YANDEX_LOGO = (By.CLASS_NAME, "Header_LogoYandex__3ST0t")

    def __init__(self, driver):
        super().__init__(driver)

    # ---------- Методы шагов оформления заказа ----------

    def fill_first_step(self, name, surname, address, phone):
        """Заполнить шаг 1: данные пользователя."""
        self.driver.find_element(*self.FIRST_NAME_FIELD).send_keys(name)
        self.driver.find_element(*self.LAST_NAME_FIELD).send_keys(surname)
        self.driver.find_element(*self.ADDRESS_FIELD).send_keys(address)

        # выбор метро
        self.driver.find_element(*self.METRO_INPUT).click()
        # ждём, пока появится хотя бы один вариант и он станет кликабельным
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.METRO_FIRST_OPTION)
        ).click()

        self.driver.find_element(*self.PHONE_FIELD).send_keys(phone)
        self.driver.find_element(*self.NEXT_BUTTON).click()

    def fill_second_step(self, date_text, comment=""):
        """Заполнить шаг 2: дата, срок аренды, цвет и комментарий."""
        # дата
        date_input = self.driver.find_element(*self.DATE_INPUT)
        date_input.send_keys(date_text)
        date_input.send_keys(Keys.ENTER)

        # срок аренды — «сутки»
        self.driver.find_element(*self.RENT_DROPDOWN).click()
        self.driver.find_element(*self.RENT_OPTION_SUTKI).click()

        # цвет
        self.driver.find_element(*self.COLOR_BLACK_CHECKBOX).click()

        # комментарий
        if comment:
            self.driver.find_element(*self.COMMENT_INPUT).send_keys(comment)

        # оформить заказ и подтвердить
        self.driver.find_element(*self.ORDER_BUTTON).click()
        self.driver.find_element(*self.YES_BUTTON).click()

    def is_success_modal_visible(self):
        """Проверка, что модалка с текстом 'Заказ оформлен' появилась."""
        text = self.driver.find_element(*self.SUCCESS_MODAL).text
        return "Заказ оформлен" in text

    # ---------- Методы работы с логотипами ----------

    def click_scooter_logo(self):
        self.driver.find_element(*self.SCOOTER_LOGO).click()

    def click_yandex_logo(self):
        self.driver.find_element(*self.YANDEX_LOGO).click()
