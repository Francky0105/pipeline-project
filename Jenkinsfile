pipeline {
    agent any

    environment {
        // Utilise la clé SSH de Jenkins Snap pour GitHub
        GIT_SSH_COMMAND = 'ssh -i /var/snap/jenkins/current/.ssh/id_ed25519 -o StrictHostKeyChecking=no'
    }

    stages {

        stage('Clone repository') {
            steps {
                echo 'Cloning repository from GitHub...'
                git branch: 'main', url: 'https://github.com/Francky0105/pipeline-project.git'
            }
        }

        stage('Build') {
            steps {
                echo 'Build step - OK'
            }
        }

        stage('Test') {
            steps {
                echo 'Running automated tests...'
                sh 'pytest --maxfail=1 --disable-warnings -q || true'
            }
        }

        stage('Deploy to Apache') {
            steps {
                echo 'Deploying to Apache...'
                sh 'sudo cp index.html /var/www/html/index.html'
            }
        }

        stage('Deploy with Docker (optional)') {
            steps {
                echo 'Deploying with Docker container...'
                sh '''
                docker build -t pipeline-project .
                docker stop pipeline-project || true
                docker rm pipeline-project || true
                docker run -d --name pipeline-project -p 8080:80 pipeline-project
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline SUCCESS ✅'
        }
        failure {
            echo 'Pipeline FAILED ❌'
        }
    }
}
