FROM python:3.12-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Allure командной строки
RUN wget https://github.com/allure-framework/allure2/releases/download/2.24.1/allure-2.24.1.tgz && \
    tar -xzf allure-2.24.1.tgz -C /opt/ && \
    ln -s /opt/allure-2.24.1/bin/allure /usr/local/bin/allure && \
    rm allure-2.24.1.tgz

# Копирование зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего проекта
COPY . .

# Команда по умолчанию
CMD ["pytest", "api/tests/", "ui/tests/", "mobile/tests/", "-v", "--alluredir=allure-results"]