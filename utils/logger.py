"""
Логирование операций в тестах с использованием Loguru.
Обеспечивает форматированный вывод в консоль и файл.
"""

import sys
from loguru import logger
from datetime import datetime


def setup_logger():
    """Настройка логгера с форматированием"""

    # Удаляем стандартный логгер
    logger.remove()

    # Добавляем вывод в консоль с цветами
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True,
    )

    # Добавляем вывод в файл
    logger.add(
        f"logs/test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
        compression="zip",
    )

    return logger


# Создаем экземпляр логгера
log = setup_logger()


def log_request(method: str, url: str, headers: dict = None, body: dict = None):
    """Логирование API запроса"""
    log.info(f"📤 REQUEST: {method} {url}")
    if headers:
        log.debug(f"Headers: {headers}")
    if body:
        log.debug(f"Body: {body}")


def log_response(status_code: int, body: dict = None):
    """Логирование API ответа"""
    log.info(f"📥 RESPONSE: {status_code}")
    if body:
        log.debug(f"Body: {body}")


def log_step(step_name: str):
    """Логирование шага теста"""
    log.info(f"🔹 STEP: {step_name}")
