from playwright.sync_api import sync_playwright, TimeoutError, expect
import test_data
import os


def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Создание директории для скриншотов, если она не существует
    #if not os.path.exists('screenshots'):
    #    os.makedirs('screenshots')

    try:
        page.goto(test_data.data_web_address_letcode, timeout=30000)
        page.wait_for_load_state('load')
        page.screenshot(path='screenshots/01_initial_load.png')

    except TimeoutError:
        print("Timeout occurred. Retrying...")
        page.goto(test_data.data_web_address_letcode, timeout=30000)
        page.wait_for_load_state('load')
        page.screenshot(path='screenshots/02_initial_load.png')

    # Заполнение полей
    page.fill('input[name="name"]', test_data.data_name)
    page.screenshot(path='screenshots/03_filled_name.png')
    page.fill('input[name="email"]', test_data.data_email)
    page.screenshot(path='screenshots/04_filled_email.png')
    page.fill('input[name="password"]', test_data.data_password)
    page.screenshot(path='screenshots/05_filled_password.png')
    page.click('input[type="checkbox"]')
    page.screenshot(path='screenshots/06_checked_checkbox.png')

    # Ожидание появления кнопки регистрации
    expect(page.locator('button.is-primary')).to_be_visible(timeout=60000)

    # Отправка формы
    page.click('button.is-primary')

    # Проверка на успешное завершение регистрации
    expect(page.locator('div:has-text("Registration successful')).to_be_visible(timeout=20000)
    page.screenshot(path='screenshots/07_registration_successful.png')

    browser.close()


with sync_playwright() as playwright:
    run(playwright)

