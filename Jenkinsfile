pipeline {
    agent any

    environment {
        // Основные настройки
        API_BASE_URL = 'https://api.demoblaze.com'
        UI_BASE_URL = 'https://demoblaze.com'

        // Selenoid настройки (типовые для QA.GURU)
        SELENOID_URL = 'https://selenoid.autotests.cloud/wd/hub'

        // BrowserStack настройки (введите свои)
        BROWSERSTACK_USERNAME = credentials('browserstack-username')
        BROWSERSTACK_ACCESS_KEY = credentials('browserstack-access-key')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "===== Установка зависимостей ====="
                    pip3 install --upgrade pip
                    pip3 install -r requirements.txt
                '''
            }
        }

        stage('Run API Tests') {
            steps {
                sh '''
                    echo "===== Запуск API тестов ====="
                    pytest api/tests/ -v -m api --alluredir=allure-results/api
                '''
            }
            post {
                always {
                    stash name: 'api-results', path: 'allure-results/api'
                }
            }
        }

        stage('Run UI Tests') {
            steps {
                sh '''
                    echo "===== Запуск UI тестов на Selenoid ====="
                    pytest ui/tests/ -v -m ui --alluredir=allure-results/ui
                '''
            }
            post {
                always {
                    stash name: 'ui-results', path: 'allure-results/ui'
                }
            }
        }

        stage('Run Mobile Tests') {
            steps {
                sh '''
                    echo "===== Запуск мобильных тестов на BrowserStack ====="
                    pytest mobile/tests/ -v -m mobile --alluredir=allure-results/mobile
                '''
            }
            post {
                always {
                    stash name: 'mobile-results', path: 'allure-results/mobile'
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh '''
                    echo "===== Генерация Allure отчета ====="
                    mkdir -p allure-results/all
                    cp -r allure-results/*/* allure-results/all/ 2>/dev/null || true
                '''
            }
            post {
                always {
                    allure includeProperties: false, jdk: '', results: [[path: 'allure-results/all']]
                }
            }
        }
    }

    post {
        success {
            sh '''
                echo "✅ Все тесты успешно пройдены!"
            '''
        }
        failure {
            sh '''
                echo "❌ Некоторые тесты упали!"
            '''
        }
    }
}