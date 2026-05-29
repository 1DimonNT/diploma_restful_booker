pipeline {
    agent { label 'python3-jenkins-agent-1' }

    parameters {
        choice(name: 'TEST_TYPE', choices: ['all', 'api', 'ui', 'mobile'], description: 'Тип запускаемых тестов')
        choice(name: 'CONTEXT', choices: ['bstack', 'local_emulator', 'local_real'], description: 'Контекст для мобильных тестов')
        choice(name: 'PLATFORM', choices: ['android', 'ios'], description: 'Платформа для мобильных тестов')
        string(name: 'BROWSERSTACK_USERNAME', defaultValue: '', description: 'BrowserStack Username')
        string(name: 'BROWSERSTACK_ACCESS_KEY', defaultValue: '', description: 'BrowserStack Access Key')
    }

    stages {
        stage('Setup') {
            steps {
                echo '===== Установка зависимостей ====='
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('API Tests') {
            when { expression { params.TEST_TYPE == 'all' || params.TEST_TYPE == 'api' } }
            steps {
                echo '===== Запуск API тестов ====='
                sh '''
                    . venv/bin/activate
                    export API_BASE_URL="https://api.demoblaze.com"
                    pytest api/tests/ -v --alluredir=allure-results
                '''
            }
        }

        stage('UI Tests') {
            when { expression { params.TEST_TYPE == 'all' || params.TEST_TYPE == 'ui' } }
            steps {
                echo '===== Запуск UI тестов ====='
                sh '''
                    . venv/bin/activate
                    export UI_BASE_URL="https://demoblaze.com"
                    pytest ui/tests/ -v --alluredir=allure-results
                '''
            }
        }

        stage('Mobile Tests') {
            when { expression { params.TEST_TYPE == 'all' || params.TEST_TYPE == 'mobile' } }
            steps {
                echo '===== Запуск мобильных тестов ====='
                sh '''
                    . venv/bin/activate
                    export CONTEXT="${CONTEXT:-bstack}"
                    export BROWSERSTACK_USERNAME="${BROWSERSTACK_USERNAME}"
                    export BROWSERSTACK_ACCESS_KEY="${BROWSERSTACK_ACCESS_KEY}"
                    pytest mobile/tests/ -v --context=$CONTEXT --platform=android --alluredir=allure-results
                '''
            }
        }
    }

    post {
        always {
            allure results: [[path: 'allure-results']]
        }
        success {
            echo '✅ Все тесты прошли успешно!'
        }
        failure {
            echo '❌ Некоторые тесты упали. Проверьте Allure отчёт.'
        }
    }
}