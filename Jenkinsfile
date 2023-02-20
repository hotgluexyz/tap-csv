pipeline {
    agent {label 'linux'}
    stages {
        stage('Hello') {
            steps {
                sh('cd /var/lib/jenkins/ && ./deploy-connector.sh')
            }
        }
    }
}