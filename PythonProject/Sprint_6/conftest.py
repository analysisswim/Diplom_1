# conftest.py
import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    # geckodriver уже должен быть в PATH (через brew install geckodriver)
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get("https://qa-scooter.praktikum-services.ru/")
    yield driver
    driver.quit()
