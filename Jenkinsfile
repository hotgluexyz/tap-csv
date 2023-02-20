pipeline {
    agent {label 'linux'}
    stages {
        stage('Hello') {
            steps {
                sh('/home/ec2-user/deploy-connector.sh')
            }
        }
    }
}