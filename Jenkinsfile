pipeline {
    agent {label 'linux'}
    stages {
        stage('Hello') {
            steps {
                sh('cd /home/ec2-user/ && chmod +x deploy-connector.sh && ./deploy-connector.sh')
            }
        }
    }
}