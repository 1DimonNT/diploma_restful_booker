import time

import allure
import pytest
from selene import be, browser

from ui.pages.demoblaze_page import demoblaze


@allure.epic("UI Testing")
@allure.feature("Demoblaze Store")
@pytest.mark.ui
class TestDemoblaze:
    @allure.title("Открытие главной страницы")
    @pytest.mark.smoke
    def test_1_open_main_page(self):
        demoblaze.open()

    @allure.title("Регистрация нового пользователя")
    def test_2_signup_new_user(self):
        username = f"testuser_{int(time.time())}"

        demoblaze.open()
        demoblaze.click_signup()
        demoblaze.fill_signup_username(username)
        demoblaze.fill_signup_password("test123")
        demoblaze.click_signup_button()

        alert_text = demoblaze.accept_alert()
        assert "Sign up successful" in alert_text or "registered" in alert_text.lower()

    @allure.title("Выбор категории товаров")
    def test_3_select_category(self):
        demoblaze.open()
        demoblaze.select_category("Phones")
        demoblaze.wait_for_products()
        demoblaze.should_have_product_with_text("Samsung")

    @allure.title("Просмотр карточки товара")
    def test_4_view_product(self):
        demoblaze.open()
        demoblaze.select_category("Phones")
        demoblaze.wait_for_products()
        demoblaze.open_first_product()
        demoblaze.should_be_on_product_page()

    @allure.title("Логин созданным пользователем")
    def test_5_login_new_user(self):
        username = f"testuser_{int(time.time())}"

        # Регистрация
        demoblaze.open()
        demoblaze.click_signup()
        demoblaze.fill_signup_username(username)
        demoblaze.fill_signup_password("test123")
        demoblaze.click_signup_button()
        demoblaze.accept_alert()

        # Логин
        demoblaze.click_login()
        demoblaze.fill_login_username(username)
        demoblaze.fill_login_password("test123")
        demoblaze.click_login_button()

        demoblaze.should_not_show_login_button()

    @allure.title("Добавление товара в корзину")
    def test_6_add_to_cart(self):
        demoblaze.open()
        demoblaze.select_category("Phones")
        demoblaze.wait_for_products()
        demoblaze.open_first_product()
        demoblaze.should_be_on_product_page()
        demoblaze.add_to_cart()

        alert_text = demoblaze.accept_alert()
        assert "Product added" in alert_text

        demoblaze.go_to_cart()
        demoblaze.should_have_items_in_cart()

    @allure.title("Отправка сообщения через форму Contact")
    def test_7_send_contact_message(self):
        demoblaze.open()
        demoblaze.open_contact_form()
        demoblaze.fill_contact_email("hr@example.com")
        demoblaze.fill_contact_name("Dmitry")

        message = "Привет! Меня зовут Дмитрий. Ищу работу AQA Python разработчиком."
        demoblaze.fill_contact_message(message)
        demoblaze.send_contact_message()

        alert_text = demoblaze.accept_alert()
        assert "Thanks for the message" in alert_text

    @allure.title("Переключение между категориями товаров")
    def test_8_switch_categories(self):
        demoblaze.open()

        categories = ["Phones", "Laptops", "Monitors"]

        for category in categories:
            with allure.step(f"Выбор категории {category}"):
                demoblaze.select_category(category)
                demoblaze.wait_for_products()
                # Проверяем, что товары отображаются
                browser.element(".card-title a").should(be.visible)
