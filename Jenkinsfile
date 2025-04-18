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
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker stop $CONTAINER_NAME || true'
            }
        }

        stage('Remove Old Container') {
            steps {
                sh 'docker rm $CONTAINER_NAME || true'
            }
        }

        stage('Run New Container') {
            steps {
                sh 'docker run -d -p $PORT:$PORT --name $CONTAINER_NAME $IMAGE_NAME'
            }
        }

        stage('List Running Containers') {
            steps {
                sh 'docker ps'
            }
        }
    }

    post {
        always {
            echo 'Pipeline run finished.'
        }
    }
}
