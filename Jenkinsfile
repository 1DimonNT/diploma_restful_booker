pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.12'
    }

    stages {
        stage('Setup') {
            steps {
                script {
                    // Проверяем переменные окружения
                    if (env.SELENOID_URL == null) {
                        env.SELENOID_URL = 'https://ru.selenoid.autotests.cloud'
                    }
                    if (env.CONTEXT == null) {
                        env.CONTEXT = 'bstack'
                    }
                }
                sh '''
                    python -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    . .venv/bin/activate
                    ruff check . || true
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest api/tests/ ui/tests/ -v --alluredir=allure-results || true
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh '''
                    . .venv/bin/activate
                    allure generate allure-results -o allure-report --clean || true
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}