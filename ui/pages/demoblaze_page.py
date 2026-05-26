from selene import browser, have, be
from allure import step
import time


class DemoblazePage:

    @step("Открыть главную страницу")
    def open(self):
        browser.open("https://www.demoblaze.com")
        return self

    @step("Нажать Sign up")
    def click_signup(self):
        browser.element("#signin2").click()
        return self

    @step("Нажать Log in")
    def click_login(self):
        browser.element("#login2").click()
        return self

    @step("Ввести username для регистрации")
    def fill_signup_username(self, username: str):
        browser.element("#sign-username").type(username)
        return self

    @step("Ввести password для регистрации")
    def fill_signup_password(self, password: str):
        browser.element("#sign-password").type(password)
        return self

    @step("Ввести username для входа")
    def fill_login_username(self, username: str):
        browser.element("#loginusername").type(username)
        return self

    @step("Ввести password для входа")
    def fill_login_password(self, password: str):
        browser.element("#loginpassword").type(password)
        return self

    @step("Нажать кнопку регистрации")
    def click_signup_button(self):
        browser.element("button[onclick='register()']").click()
        return self

    @step("Нажать кнопку входа")
    def click_login_button(self):
        browser.element("button[onclick='logIn()']").click()
        return self

    @step("Принять alert с ожиданием")
    def accept_alert_with_wait(self):
        time.sleep(1)
        alert = browser.driver.switch_to.alert
        text = alert.text
        alert.accept()
        return text

    @step("Проверить успешный вход")
    def should_have_logged_in(self, username: str):
        browser.element("#nameofuser").should(have.text(f"Welcome {username}"))
        return self


demoblaze = DemoblazePage()