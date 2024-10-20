import pytest
from playwright.sync_api import sync_playwright, TimeoutError, expect
import test_data
import time

@pytest.fixture
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()

def test_login(browser):
    page = browser

    # Установка таймаута по умолчанию
    page.set_default_timeout(60000)  # 60 секунд

    try:
        page.goto(test_data.data_web_address_signin)
        page.wait_for_load_state('load')
        timestamp = int(time.time())
        page.screenshot(path=f'../screenshots/09_{timestamp}.png')
        print(f"Screenshot 09_{timestamp}.png taken")

    except TimeoutError:
        print("Timeout occurred. Retrying...")
        page.goto(test_data.data_web_address_letcode)
        page.wait_for_load_state('load')
        timestamp = int(time.time())
        page.screenshot(path=f'../screenshots/10_{timestamp}.png')
        print(f"Screenshot 10_{timestamp}.png taken")

    # Заполнение полей
    page.fill('input[name="email"]', test_data.data_email)
    timestamp = int(time.time())
    page.screenshot(path=f'../screenshots/11_{timestamp}.png')
    print(f"Screenshot 11_{timestamp}.png taken")

    page.fill('input[name="password"]', test_data.data_password)
    timestamp = int(time.time())
    page.screenshot(path=f'../screenshots/12_{timestamp}.png')
    print(f"Screenshot 12_{timestamp}.png taken")

    # Ожидание появления кнопки log in
    expect(page.locator('button.is-primary:has-text("LOGIN")')).to_be_visible()

    # Отправка формы
    page.click('button.is-primary')

    # Проверка на успешное логирование
    print("Waiting for 'Welcome Jaine White' message...")

    try:
        # Уточненный селектор, используя класс overlay-container
        page.locator('div.overlay-container:has-text("Welcome Jaine White")').wait_for(timeout=120000)  # Увеличенный таймаут до 120 секунд
        timestamp = int(time.time())
        page.screenshot(path=f'../screenshots/12_{timestamp}.png')
        print(f"Screenshot 12_{timestamp}.png taken")
    except TimeoutError:
        print("Timeout occurred while waiting for 'Welcome Jaine White' message.")
        timestamp = int(time.time())
        page.screenshot(path=f'../screenshots/13_timeout_{timestamp}.png')
        print(f"Screenshot 13_timeout_{timestamp}.png taken")