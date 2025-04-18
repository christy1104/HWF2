pipeline {
    agent any

    environment {
        IMAGE_NAME = 'devops2-hwf'
        CONTAINER_NAME = 'devops2-hwf-container'
        PORT = '5000'
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Repository is automatically cloned by Jenkins (SCM configured)'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        stage('Stop Old Container') {
            steps {
                bat 'docker stop %CONTAINER_NAME% || true'
            }
        }

        stage('Remove Old Container') {
            steps {
                bat 'docker rm %CONTAINER_NAME% || true'
            }
        }

        stage('Run New Container') {
            steps {
                bat 'docker run -d -p %PORT%:%PORT% --name %CONTAINER_NAME% %IMAGE_NAME%'
            }
        }

        stage('List Running Containers') {
            steps {
                bat 'docker ps'
            }
        }
    }

    post {
        always {
            echo 'Pipeline run finished.'
        }
    }
}
