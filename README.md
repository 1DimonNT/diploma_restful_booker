# Diploma Project: Restful-booker Automation

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Pytest](https://img.shields.io/badge/Pytest-8.3-green)
![Selene](https://img.shields.io/badge/Selene-2.1-orange)
![Allure](https://img.shields.io/badge/Allure-2.13-red)
![Ruff](https://img.shields.io/badge/Ruff-0.8-purple)

</div>

## 📋 О проекте

Дипломный проект по автоматизации тестирования сервиса [Restful-booker](https://restful-booker.herokuapp.com/), включающий:

- **API тесты** (7+ тестов) с использованием Pydantic моделей
- **UI тесты** (7+ тестов) с использованием Selene и PageObject
- **Mobile тесты** (5+ тестов) с использованием Appium (Wikipedia)

## 🛠 Технологии и инструменты


| Технология | Назначение |
|------------|------------|
| Python 3.12 | Основной язык программирования |
| Pytest | Тестовый фреймворк |
| Selene | Обертка над Selenium для UI тестов |
| Requests | HTTP клиент для API тестов |
| Pydantic | Валидация данных и модели |
| Allure | Отчетность и логирование |
| Ruff | Линтер и форматтер |
| Appium | Mobile тестирование |
| BrowserStack | Облачное устройство для mobile тестов |

## 📁 Структура проекта
```text
diploma_restful_booker/
├── api/                   # API тесты
│   ├── client.py          # HTTP клиент
│   ├── models/            # Pydantic модели
│   └── tests/             # API тесты (7+)
├── ui/                    # UI тесты
│   ├── pages/             # PageObject
│   ├── tests/             # UI тесты (7+)
│   └── conftest.py        # UI фикстуры
├── mobile/                # Mobile тесты
│   ├── tests/             # Mobile тесты (5+)
│   └── conftest.py        # Mobile фикстуры
├── utils/                 # Утилиты
│   ├── allure_helper.py   # Allure вложения
│   └── logger.py          # Логирование
├── config.py              # Pydantic конфигурация
├── conftest.py            # Глобальные фикстуры
├── pytest.ini             # Настройки pytest
├── pyproject.toml         # Ruff настройки
└── requirements.txt       # Зависимости
```

## 🚀 Запуск тестов

### Установка зависимостей

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### API тесты
```bash
pytest api/tests -m api
```

### UI тестов
```bash
pytest ui/tests -m ui
```

### Mobile тесты (локально)
```bash
set CONTEXT=local_emulator
pytest mobile/tests -m mobile
```

### Mobile тесты (BrowserStack)
```bash
set CONTEXT=bstack
set BROWSERSTACK_USERNAME=your_username
set BROWSERSTACK_ACCESS_KEY=your_key
pytest mobile/tests -m mobile
```

### Все тесты с Allure отчетом
```bash
pytest --alluredir=allure-results
allure serve allure-results
```

## 📊 Allure отчет
Отчет содержит:
- Скриншоты при падении UI тестов
- Видео для mobile тестов (BrowserStack)
- API request/response вложения
- Логи выполнения

## 🏷 Маркеры тестов


| Маркер | Описание |
|--------|----------|
| `@pytest.mark.api` | API тесты |
| `@pytest.mark.ui` | UI тесты |
| `@pytest.mark.mobile` | Mobile тесты |
| `@pytest.mark.smoke` | Дымовые тесты |
| `@pytest.mark.critical` | Критическая важность |

## 📝 Требования к диплому
- [x] 7+ API тестов
- [x] 7+ UI тестов
- [x] 3+ Mobile тестов (сделано 5)
- [x] PageObject (Selene, Fluent style)
- [x] Pydantic модели для request/response
- [x] Allure отчетность с вложениями
- [x] Pytest конфигурация и маркеры
- [x] Ruff линтинг
- [x] Поддержка BrowserStack для mobile

## 👤 Автор
Дипломный проект студента QA.GURU Дмитрия Михайловича Иванцова

## 📄 Лицензия
MIT
