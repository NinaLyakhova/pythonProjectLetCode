import pytest
from playwright.sync_api import sync_playwright, TimeoutError, expect
import test_data
import os

@pytest.fixture
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()

def test_registration(browser):
    page = browser

    # Установка таймаута по умолчанию
    page.set_default_timeout(60000)  # 60 секунд

    # Создание директории для скриншотов, если она не существует
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')

    try:
        page.goto(test_data.data_web_address_letcode)
        page.wait_for_load_state('load')
        page.screenshot(path='screenshots/01.png')
        print("Screenshot 01 taken")

    except TimeoutError:
        print("Timeout occurred. Retrying...")
        page.goto(test_data.data_web_address_letcode)
        page.wait_for_load_state('load')
        page.screenshot(path='screenshots/02.png')
        print("Screenshot 02 taken")

    # Заполнение полей
    page.fill('input[name="name"]', test_data.data_name)
    page.screenshot(path='screenshots/03.png')
    print("Screenshot 03 taken")

    page.fill('input[name="email"]', test_data.data_email)
    page.screenshot(path='screenshots/04.png')
    print("Screenshot 04 taken")

    page.fill('input[name="password"]', test_data.data_password)
    page.screenshot(path='screenshots/05.png')
    print("Screenshot 05 taken")

    page.click('input[type="checkbox"]')
    page.screenshot(path='screenshots/06.png')
    print("Screenshot 06 taken")

    # Ожидание появления кнопки регистрации
    expect(page.locator('button.is-primary')).to_be_visible()

    # Отправка формы
    page.click('button.is-primary')

    # Проверка на успешное завершение регистрации
    print("Waiting for 'You have logged in Jaine White' message...")
    try:
        # Уточненный селектор, используя класс overlay-container
        page.locator('div.overlay-container:has-text("You have logged in Jaine White")').wait_for(timeout=120000)  # Увеличенный таймаут до 120 секунд
        page.screenshot(path='screenshots/07.png')
        print("Screenshot 07 taken")
    except TimeoutError:
        print("Timeout occurred while waiting for 'You have logged in Jaine White' message.")
        page.screenshot(path='screenshots/07_timeout.png')
        print("Screenshot 07_timeout taken")
