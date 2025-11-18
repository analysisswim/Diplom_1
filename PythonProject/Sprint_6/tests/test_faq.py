# tests/test_faq.py
import pytest
from selenium.webdriver.support.ui import WebDriverWait

from pages.main_page import MainPage


# На сайте 8 вопросов в FAQ (индексы 0–7)
@pytest.mark.parametrize("index", range(8))
def test_faq_answer_not_empty(driver, index):
    page = MainPage(driver)

    # скроллим до блока FAQ
    page.scroll_to_faq()

    # кликаем по нужному вопросу
    page.click_faq_question(index)

    # ждём, пока ответ появится (станет непустым)
    def answer_has_text(d):
        return page.get_faq_answer_text(index).strip() != ""

    WebDriverWait(driver, 10).until(answer_has_text)

    answer_text = page.get_faq_answer_text(index)
    assert answer_text.strip() != ""
