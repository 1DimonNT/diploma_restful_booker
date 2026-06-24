pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.12'
        SELENOID_URL = 'https://ru.selenoid.autotests.cloud'
    }

    parameters {
        choice(
            name: 'CONTEXT',
            choices: ['bstack', 'local_emulator', 'local_real'],
            description: 'Контекст запуска мобильных тестов'
        )
        choice(
            name: 'PLATFORM',
            choices: ['android', 'ios'],
            description: 'Платформа для тестирования'
        )
        string(
            name: 'DEVICE',
            defaultValue: 'Google Pixel 7',
            description: 'Устройство для тестирования'
        )
        booleanParam(
            name: 'RUN_MOBILE_TESTS',
            defaultValue: false,
            description: 'Запускать ли мобильные тесты (требуется BrowserStack)'
        )
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    . venv/bin/activate
                    ruff check . || true
                '''
            }
        }

        stage('API Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest api/tests/ -v --alluredir=allure-results/api
                '''
            }
        }

        stage('UI Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest ui/tests/ -v --alluredir=allure-results/ui
                '''
            }
        }

        stage('Mobile Tests') {
            when {
                expression { params.RUN_MOBILE_TESTS == true }
            }
            steps {
                sh '''
                    . venv/bin/activate
                    export CONTEXT=${CONTEXT}
                    export PLATFORM=${PLATFORM}
                    pytest mobile/tests/ -v --alluredir=allure-results/mobile
                '''
            }
        }

        stage('Generate Report') {
            steps {
                sh '''
                    . venv/bin/activate
                    mkdir -p allure-results/all
                    cp -r allure-results/api/* allure-results/all/ 2>/dev/null || true
                    cp -r allure-results/ui/* allure-results/all/ 2>/dev/null || true
                    cp -r allure-results/mobile/* allure-results/all/ 2>/dev/null || true
                    allure generate allure-results/all -o allure-report --clean || true
                '''
            }
        }

        stage('Publish Report') {
            steps {
                allure publish allure-report
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}