# pages/main_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    # кнопки «Заказать» (верх и низ страницы)
    ORDER_BUTTONS = (By.XPATH, "//button[text()='Заказать']")

    # вопросы и ответы в блоке «Вопросы о важном»
    FAQ_QUESTIONS = (By.CLASS_NAME, "accordion__button")
    FAQ_ANSWERS = (By.CLASS_NAME, "accordion__panel")

    # логотипы
    SCOOTER_LOGO = (By.CLASS_NAME, "Header_LogoScooter__3lsAR")
    # более стабильный вариант: ищем по ссылке на яндекс
    YANDEX_LOGO = (By.CSS_SELECTOR, "a[href*='yandex.ru']")

    # кнопка в баннере с куками (любой button внутри контейнера App_CookieConsent)
    COOKIE_BUTTON = (By.CSS_SELECTOR, "div[class^='App_CookieConsent'] button")

    def close_cookie_banner(self):
        """Пытается закрыть баннер с куками, если он есть."""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.COOKIE_BUTTON)
            ).click()
        except Exception:
            # баннера нет или уже закрыт — просто игнорируем
            pass

    def click_order_button(self, index):
        """Клик по кнопке «Заказать» (0 — верхняя, 1 — нижняя)."""
        self.close_cookie_banner()
        # ждём, пока хотя бы одна кнопка станет кликабельной
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ORDER_BUTTONS)
        )
        self.driver.find_elements(*self.ORDER_BUTTONS)[index].click()

    def scroll_to_faq(self):
        first_question = self.driver.find_elements(*self.FAQ_QUESTIONS)[0]
        self.driver.execute_script("arguments[0].scrollIntoView();", first_question)

    def click_faq_question(self, index):
        element = self.driver.find_elements(*self.FAQ_QUESTIONS)[index]
        # скроллим конкретный вопрос в видимую область
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        # кликаем по нему через JS, чтобы не мешала картинка
        self.driver.execute_script("arguments[0].click();", element)

    def get_faq_answer_text(self, index):
        return self.driver.find_elements(*self.FAQ_ANSWERS)[index].text

    def click_scooter_logo(self):
        self.close_cookie_banner()
        self.driver.find_element(*self.SCOOTER_LOGO).click()

    def click_yandex_logo(self):
        self.close_cookie_banner()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.YANDEX_LOGO)
        ).click()
