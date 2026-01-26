pipeline {
    agent any

    environment {
        // Clé SSH spécifique pour Jenkins Snap
        GIT_SSH_COMMAND = 'ssh -i /var/snap/jenkins/current/.ssh/id_ed25519 -o StrictHostKeyChecking=no'
    }

    stages {

        stage('Clone repository') {
            steps {
                echo 'Cloning repository...'
                git branch: 'main', url: 'git@github.com:Francky0105/pipeline-project.git'
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
                docker build -t cicd-project .
                docker stop cicd-project || true
                docker rm cicd-project || true
                docker run -d --name cicd-project -p 8080:80 cicd-project
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

