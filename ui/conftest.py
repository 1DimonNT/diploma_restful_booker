def _get_driver(request):
    """Создание и настройка WebDriver (локально или через Selenoid)"""

    browser_name = settings.BROWSER
    log.info(f"🌐 Initializing {browser_name} browser")

    options = ChromeOptions()
    options.add_argument(f"--window-size={settings.WINDOW_WIDTH},{settings.WINDOW_HEIGHT}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--headless=new")  # Добавляем headless для Jenkins
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    selenoid_url = settings.SELENOID_URL
    if selenoid_url:
        log.info(f"🚀 Running on Selenoid: {selenoid_url}")
        selenoid_host = selenoid_url.replace('https://', '').replace('http://', '').rstrip('/')
        selenoid_full_url = f'http://{settings.SELENOID_USER}:{settings.SELENOID_PASSWORD}@{selenoid_host}'

        capabilities = {
            "browserName": browser_name,
            "browserVersion": settings.BROWSER_VERSION,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True,
                "videoName": f"{request.node.name}.mp4",
                "videoScreenSize": f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}"
            }
        }

        for key, value in capabilities.items():
            options.set_capability(key, value)

        driver = webdriver.Remote(command_executor=selenoid_full_url, options=options)
    else:
        log.info("🖥️ Running locally")
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service

        # Указываем правильный путь к драйверу
        driver_path = ChromeDriverManager().install()
        log.info(f"Driver path: {driver_path}")

        # Исправляем путь (на Linux путь может быть к папке, а не к файлу)
        if driver_path.endswith('/') or driver_path.endswith('\\'):
            driver_path = driver_path + 'chromedriver'
        elif not driver_path.endswith('chromedriver'):
            import os
            driver_path = os.path.join(driver_path, 'chromedriver')

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)

    return driver