pipeline {
    agent {label "linux"}
    stages {
        stage('Hello') {
            steps {
                echo sh(script: 'env|sort', returnStdout: true)
            }
        }
    }
}