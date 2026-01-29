pipeline {
    agent any

    stages {

        stage('Test credentials') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-creds',
                        usernameVariable: 'USER',
                        passwordVariable: 'PASS'
                    )
                ]) {
                    sh '''
                      echo "Le username est $USER"
                      echo "Le password est cache"
                    '''
                }
            }
        }

    }
}

