def _get_driver(request):
    """Создание и настройка WebDriver (локально или через Selenoid)"""

    browser_name = settings.BROWSER
    log.info(f"🌐 Initializing {browser_name} browser")

    options = ChromeOptions()
    options.add_argument(f"--window-size={settings.WINDOW_WIDTH},{settings.WINDOW_HEIGHT}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ПРЯМОЕ УКАЗАНИЕ SELENOID (без чтения из settings)
    # Временно для отладки
    log.info("🔧 Принудительное использование Selenoid")
    selenoid_full_url = "http://user1:1234@selenoid.autotests.cloud/wd/hub"

    capabilities = {
        "browserName": "chrome",
        "browserVersion": "128.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True,
            "videoName": f"{request.node.name}.mp4",
            "videoScreenSize": "1920x1080"
        }
    }

    for key, value in capabilities.items():
        options.set_capability(key, value)

    driver = webdriver.Remote(command_executor=selenoid_full_url, options=options)
    log.info("✅ Selenoid driver created")
    return driver