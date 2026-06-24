from allure import step
from selene import be, browser, have
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class DemoblazePage:
    """Главная страница Demoblaze"""

    @step("Открыть главную страницу")
    def open(self):
        browser.open("https://www.demoblaze.com")
        self._wait_for_page_load()
        return self

    def _wait_for_page_load(self):
        """Ожидание загрузки главной страницы"""
        WebDriverWait(browser.driver, 10).until(EC.visibility_of_element_located((By.ID, "contcont")))

    def _wait_for_alert(self, timeout: int = 10):
        """Ожидание появления alert"""
        WebDriverWait(browser.driver, timeout).until(EC.alert_is_present())
        return browser.driver.switch_to.alert

    # ========== Регистрация ==========

    @step("Нажать Sign up")
    def click_signup(self):
        browser.element("#signin2").click()
        return self

    @step("Ввести username для регистрации")
    def fill_signup_username(self, username: str):
        browser.element("#sign-username").type(username)
        return self

    @step("Ввести password для регистрации")
    def fill_signup_password(self, password: str):
        browser.element("#sign-password").type(password)
        return self

    @step("Нажать кнопку регистрации")
    def click_signup_button(self):
        browser.element("button[onclick='register()']").click()
        return self

    @step("Принять alert")
    def accept_alert(self):
        alert = self._wait_for_alert()
        text = alert.text
        alert.accept()
        return text

    # ========== Логин ==========

    @step("Нажать Log in")
    def click_login(self):
        # Ждем, пока модальное окно регистрации закроется
        WebDriverWait(browser.driver, 10).until(EC.invisibility_of_element_located((By.ID, "signInModal")))
        browser.element("#login2").click()
        return self

    @step("Ввести username для входа")
    def fill_login_username(self, username: str):
        browser.element("#loginusername").type(username)
        return self

    @step("Ввести password для входа")
    def fill_login_password(self, password: str):
        browser.element("#loginpassword").type(password)
        return self

    @step("Нажать кнопку входа")
    def click_login_button(self):
        browser.element("button[onclick='logIn()']").click()
        return self

    @step("Проверить успешный вход")
    def should_have_logged_in(self, username: str):
        browser.element("#nameofuser").should(have.text(f"Welcome {username}"))
        return self

    @step("Проверить, что кнопка Login не отображается (пользователь авторизован)")
    def should_not_show_login_button(self):
        browser.element("#login2").should(be.not_.visible)
        return self

    # ========== Категории товаров ==========

    @step("Выбрать категорию: {category}")
    def select_category(self, category: str):
        browser.element(f"//a[contains(text(), '{category}')]").click()
        return self

    @step("Дождаться загрузки товаров в категории")
    def wait_for_products(self):
        WebDriverWait(browser.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".card-title a")))
        return self

    @step("Проверить, что товар с названием {expected_text} присутствует")
    def should_have_product_with_text(self, expected_text: str):
        browser.element(f"//*[contains(text(), '{expected_text}')]").should(be.visible)
        return self

    @step("Открыть первый товар")
    def open_first_product(self):
        browser.element(".card-title a").click()
        return self

    @step("Проверить, что страница товара открыта")
    def should_be_on_product_page(self):
        browser.element(".name").should(be.visible)
        return self

    @step("Нажать кнопку 'Add to cart'")
    def add_to_cart(self):
        browser.element("a.btn.btn-success").click()
        return self

    # ========== Корзина ==========

    @step("Перейти в корзину")
    def go_to_cart(self):
        browser.element("#cartur").click()
        return self

    @step("Проверить, что корзина содержит товары")
    def should_have_items_in_cart(self):
        browser.element(".success").should(be.visible)
        return self

    # ========== Contact форма ==========

    @step("Открыть форму Contact")
    def open_contact_form(self):
        browser.element("//a[contains(text(), 'Contact')]").click()
        WebDriverWait(browser.driver, 10).until(EC.visibility_of_element_located((By.ID, "exampleModal")))
        return self

    @step("Ввести email в Contact форме")
    def fill_contact_email(self, email: str):
        browser.element("#recipient-email").type(email)
        return self

    @step("Ввести имя в Contact форме")
    def fill_contact_name(self, name: str):
        browser.element("#recipient-name").type(name)
        return self

    @step("Ввести сообщение в Contact форме")
    def fill_contact_message(self, message: str):
        browser.element("#message-text").type(message)
        return self

    @step("Отправить сообщение из Contact формы")
    def send_contact_message(self):
        browser.element("button[onclick='send()']").click()
        return self


demoblaze = DemoblazePage()
