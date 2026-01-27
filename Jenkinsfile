pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Francky0105/pipeline-project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t pipeline-project .'
            }
        }

        stage('Stop old container') {
            steps {
                sh '''
                docker stop pipeline-container || true
                docker rm pipeline-container || true
                '''
            }
        }

        stage('Deploy with Docker') {
            steps {
                sh '''
                docker run -d \
                --name pipeline-container \
                -p 8081:80 \
                pipeline-project
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline SUCCESS ✅ Docker deployed'
        }
        failure {
            echo 'Pipeline FAILED ❌'
        }
    }
}

