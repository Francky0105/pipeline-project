pipeline {
    agent any

    environment {
        IMAGE_NAME = "pipeline-project"
        CONTAINER_NAME = "pipeline-container"
        APP_PORT = "8081"
    }

    triggers {
        githubPush()
    }

    stages {

        /* ===============================
           1️⃣ CLONE SÉCURISÉ
        =============================== */
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        /* ===============================
           2️⃣ CONTRÔLE D’INTÉGRITÉ DU CODE
        =============================== */
        stage('Security - Code Check') {
            steps {
                echo "Basic security checks on source code..."
                sh '''
                  if grep -R "password" .; then
                    echo "❌ Mot de passe trouvé dans le code"
                    exit 1
                  fi
                '''
            }
        }

        /* ===============================
           3️⃣ BUILD DOCKER SÉCURISÉ
        =============================== */
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        /* ===============================
           4️⃣ SCAN DE SÉCURITÉ DOCKER
        =============================== */
        stage('Security - Docker Image Scan') {
            steps {
                echo "Docker image security scan..."
                sh '''
                  if command -v trivy >/dev/null 2>&1; then
                    trivy image --severity HIGH,CRITICAL $IMAGE_NAME
                  else
                    echo "⚠️ Trivy non installé, scan ignoré"
                  fi
                '''
            }
        }

        /* ===============================
           5️⃣ ARRÊT SÉCURISÉ DES ANCIENS CONTENEURS
        =============================== */

        stage('Stop old container') {
            steps {
                sh '''
                   docker stop pipeline-container || true
                   docker rm pipeline-container || true
                '''
            }
        }

        /* ===============================
           6️⃣ DÉPLOIEMENT CONTRÔLÉ
        =============================== */

        stage('Deploy with Docker') {
             when {
                 branch 'main'
             }
            steps {
                 sh '''
                   docker run -d \
                    --name pipeline-container \
                    --read-only \
                    --restart unless-stopped \
                     -p 8081:80 \
                    pipeline-project
                 '''
            }
        }

      
    post {
        success {
            echo "✅ Pipeline sécurisé exécuté avec succès"
        }
        failure {
            echo "❌ Pipeline bloqué pour raisons de sécurité"
        }
    }
}


