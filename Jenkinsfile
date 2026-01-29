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
           1️⃣ CLONE DU CODE
        =============================== */
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        /* ===============================
           2️⃣ TEST DES CREDENTIALS JENKINS
        =============================== */
        stage('Test credentials') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                      echo "Le username est $DOCKER_USER"
                      echo "Le password est caché ✅"
                    '''
                }
            }
        }

        /* ===============================
           3️⃣ CONTRÔLE DE SÉCURITÉ DU CODE
        =============================== */
        stage('Security - Code Check') {
            steps {
                sh '''
                  echo "Analyse de sécurité du code..."
                  if grep -R --exclude=Jenkinsfile --exclude-dir=.git "password" .; then
                    echo "❌ Mot de passe trouvé dans le code"
                    exit 1
                  else
                    echo "✅ Aucun secret détecté"
                  fi
                '''
            }
        }



               /* ===============================
                     🔐 DOCKER LOGIN SÉCURISÉ
                  =============================== */
         stage('Docker Login (Secure)') {
             steps {
                  withCredentials([
                             usernamePassword(
                                    credentialsId: 'docker-creds',
                                    usernameVariable: 'DOCKER_USER',
                                    passwordVariable: 'DOCKER_PASS'
                                  )
                            ]) {
                               sh '''
                                 echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                               '''
                               }
                     }
          }



        /* ===============================
           4️⃣ BUILD DOCKER
        =============================== */
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        /* ===============================
           5️⃣ SCAN DE SÉCURITÉ DOCKER
        =============================== */
        stage('Security - Docker Image Scan') {
            steps {
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
           6️⃣ ARRÊT ANCIEN CONTENEUR
        =============================== */
        stage('Stop old container') {
            steps {
                sh '''
                  docker stop $CONTAINER_NAME || true
                  docker rm $CONTAINER_NAME || true
                '''
            }
        }

        /* ===============================
           7️⃣ DÉPLOIEMENT SÉCURISÉ
        =============================== */
        stage('Deploy with Docker') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                  docker run -d \
                    --name $CONTAINER_NAME \
                    --read-only \
                    --restart unless-stopped \
                    -p $APP_PORT:80 \
                    $IMAGE_NAME
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline exécuté avec succès"
        }
        failure {
            echo "❌ Pipeline bloqué (sécurité ou erreur)"
        }
    }
}

