from playwright.async_api import expect
from playwright.sync_api import sync_playwright, TimeoutError
import test_data


def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    try:
        page.goto(test_data.data_web_address_letcode, timeout=60000)
        page.wait_for_load_state('load')
    except TimeoutError:
        print("Timeout occurred. Retrying...")
        page.goto(test_data.data_web_address_letcode, timeout=60000)
        page.wait_for_load_state('load')

    # Заполнение полей
    page.fill('input[name="name"]', test_data.data_name)
    page.fill('input[name="email"]', test_data.data_email)
    page.fill('input[name="password"]', test_data.data_password)
    page.click('input[type="checkbox"]')
    # Отправка формы
    expect(page.locator(['button_sign_up'])).to_be_visible()
    page.click('button[type="is-primary"]')

    # Добавьте проверки, если необходимо
    # Например, проверка на успешное завершение регистрации

    browser.close()

with sync_playwright() as playwright:
    run(playwright)