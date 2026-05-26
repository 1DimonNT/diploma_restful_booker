from selene import browser
import time

browser.open("https://www.demoblaze.com")
time.sleep(2)

print("=" * 60)
print("ПОИСК СЕЛЕКТОРОВ НА DEMOBLAZE")
print("=" * 60)

# 1. Кнопка Sign Up
try:
    el = browser.element("#signin2")
    print(f"✅ Кнопка Sign Up: #signin2 -> текст: {el.text}")
except:
    print("❌ #signin2 не найден")

# 2. Кнопка Log In
try:
    el = browser.element("#login2")
    print(f"✅ Кнопка Log In: #login2 -> текст: {el.text}")
except:
    print("❌ #login2 не найден")

# Нажимаем Sign Up
print("\nНажимаем Sign Up...")
browser.element("#signin2").click()
time.sleep(1)

# 3. Поле username в регистрации
try:
    el = browser.element("#sign-username")
    print(f"✅ Поле Username (регистрация): #sign-username -> placeholder: {el.get_attribute('placeholder')}")
except:
    print("❌ #sign-username не найден")

# 4. Поле password в регистрации
try:
    el = browser.element("#sign-password")
    print(f"✅ Поле Password (регистрация): #sign-password -> placeholder: {el.get_attribute('placeholder')}")
except:
    print("❌ #sign-password не найден")

# 5. Кнопка регистрации в модалке
try:
    el = browser.element("button[onclick='register()']")
    print(f"✅ Кнопка регистрации: button[onclick='register()'] -> текст: {el.text}")
except:
    print("❌ button[onclick='register()'] не найден")

# Закрываем модалку
try:
    browser.element(".close").click()
    print("✅ Модалка закрыта")
except:
    print("❌ Не удалось закрыть модалку")

# Нажимаем Log In
print("\nНажимаем Log In...")
browser.element("#login2").click()
time.sleep(1)

# 6. Поле username в логине
try:
    el = browser.element("#loginusername")
    print(f"✅ Поле Username (логин): #loginusername -> placeholder: {el.get_attribute('placeholder')}")
except:
    print("❌ #loginusername не найден")

# 7. Поле password в логине
try:
    el = browser.element("#loginpassword")
    print(f"✅ Поле Password (логин): #loginpassword -> placeholder: {el.get_attribute('placeholder')}")
except:
    print("❌ #loginpassword не найден")

# 8. Кнопка логина
try:
    el = browser.element("button[onclick='logIn()']")
    print(f"✅ Кнопка логина: button[onclick='logIn()'] -> текст: {el.text}")
except:
    print("❌ button[onclick='logIn()'] не найден")

# Закрываем модалку
try:
    browser.element(".close").click()
    print("✅ Модалка логина закрыта")
except:
    print("❌ Не удалось закрыть модалку логина")

# 9. Кнопка Cart
try:
    el = browser.element("#cartur")
    print(f"✅ Кнопка Cart: #cartur -> текст: {el.text}")
except:
    print("❌ #cartur не найден")

# 10. Категории товаров
print("\nКатегории товаров:")
categories = [
    ("Phones", "//a[contains(text(), 'Phones')]"),
    ("Laptops", "//a[contains(text(), 'Laptops')]"),
    ("Monitors", "//a[contains(text(), 'Monitors')]")
]

for name, selector in categories:
    try:
        el = browser.element(selector)
        print(f"✅ {name}: {selector}")
    except:
        print(f"❌ {name}: {selector} не найден")

# 11. Элемент после логина (проверим после ручного входа)
print("\n" + "=" * 60)
print("Для проверки элемента #nameofuser нужно войти вручную")
print("Введи логин и пароль в открывшемся браузере и нажми Enter здесь")
print("=" * 60)

input("Нажми Enter после ручного входа...")

try:
    el = browser.element("#nameofuser")
    print(f"✅ #nameofuser -> текст: {el.text}")
except:
    print("❌ #nameofuser не найден")

print("\nСкрипт завершен. Браузер закроется через 10 секунд...")
time.sleep(10)
browser.quit()