import time
import allure
import pytest
from selene import browser, be, have
from ui.pages.demoblaze_page import demoblaze
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@allure.epic("UI Testing")
@allure.feature("Demoblaze Store")
@pytest.mark.ui
class TestDemoblaze:

    @allure.title("Открытие главной страницы")
    @pytest.mark.smoke
    def test_1_open_main_page(self):
        demoblaze.open()
        WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "contcont"))
        )

    @allure.title("Регистрация нового пользователя")
    def test_2_signup_new_user(self):
        username = f"testuser_{int(time.time())}"
        demoblaze.open()
        demoblaze.click_signup()
        demoblaze.fill_signup_username(username)
        demoblaze.fill_signup_password("test123")
        demoblaze.click_signup_button()

        WebDriverWait(browser.driver, 10).until(EC.alert_is_present())
        browser.driver.switch_to.alert.accept()

    @allure.title("Выбор категории товаров")
    def test_3_select_category(self):
        demoblaze.open()
        browser.element("//a[contains(text(), 'Phones')]").click()
        WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".card-title a"))
        )
        browser.element(".card-title a").should(be.visible)

    @allure.title("Просмотр карточки товара")
    def test_4_view_product(self):
        demoblaze.open()
        browser.element("//a[contains(text(), 'Phones')]").click()
        WebDriverWait(browser.driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".card-title a"))
        )
        browser.element(".card-title a").click()
        WebDriverWait(browser.driver, 15).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "name"))
        )
        browser.element(".name").should(be.visible)

    @allure.title("Логин созданным пользователем")
    def test_5_login_new_user(self):
        username = f"testuser_{int(time.time())}"

        demoblaze.open()
        demoblaze.click_signup()
        demoblaze.fill_signup_username(username)
        demoblaze.fill_signup_password("test123")
        demoblaze.click_signup_button()

        WebDriverWait(browser.driver, 10).until(EC.alert_is_present())
        browser.driver.switch_to.alert.accept()

        WebDriverWait(browser.driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "signInModal"))
        )

        demoblaze.click_login()
        demoblaze.fill_login_username(username)
        demoblaze.fill_login_password("test123")
        demoblaze.click_login_button()

        WebDriverWait(browser.driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "logInModal"))
        )

        browser.element("#login2").should(be.not_.visible)

    @allure.title("Добавление товара в корзину")
    def test_6_add_to_cart(self):
        demoblaze.open()
        browser.element("//a[contains(text(), 'Phones')]").click()
        WebDriverWait(browser.driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".card-title a"))
        )
        browser.element(".card-title a").click()
        WebDriverWait(browser.driver, 15).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".name"), "Samsung")
        )
        browser.element("a.btn.btn-success").click()
        WebDriverWait(browser.driver, 10).until(EC.alert_is_present())
        browser.driver.switch_to.alert.accept()

        browser.element("#cartur").click()
        WebDriverWait(browser.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "success"))
        )

    @allure.title("Отправка сообщения через форму Contact")
    def test_7_send_contact_message(self):
        demoblaze.open()
        browser.element("//a[contains(text(), 'Contact')]").click()

        WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "exampleModal"))
        )

        browser.element("#recipient-email").type("hr@example.com")
        browser.element("#recipient-name").type("Dmitry")

        message = "Привет! Меня зовут Дмитрий. Ищу работу AQA Python разработчиком."
        message_field = browser.element("#message-text")
        for char in message:
            message_field.type(char)

        browser.element("button[onclick='send()']").click()

        WebDriverWait(browser.driver, 10).until(EC.alert_is_present())
        alert_text = browser.driver.switch_to.alert.text
        print(f"\n✅ Alert текст: {alert_text}")
        browser.driver.switch_to.alert.accept()

    @allure.title("Переключение между категориями товаров")
    def test_8_switch_categories(self):
        from selene import have

        demoblaze.open()

        # Категория Phones
        browser.element("//a[contains(text(), 'Phones')]").click()
        WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".card-title a"))
        )
        browser.element(".card-title a").should(have.text("Samsung") or have.text("Nokia"))

        # Категория Laptops
        browser.element("//a[contains(text(), 'Laptops')]").click()
        WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".card-title a"))
        )
        browser.element(".card-title a").should(have.text("Sony") or have.text("MacBook"))

        # Категория Monitors
        browser.element("//a[contains(text(), 'Monitors')]").click()
        WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".card-title a"))
        )
        browser.element(".card-title a").should(have.text("Apple") or have.text("ASUS"))