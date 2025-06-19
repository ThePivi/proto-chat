// Jenkinsfile
pipeline {
    agent any // A build bármely elérhető agenten futhat (lokálisan a masteren)

    tools {
        // Biztosítja, hogy a Jenkins megtalálja a Python telepítést
        // Ezt a nevet (pl. 'Python_3_9') előzetesen be kell állítanod a Jenkinsben (Manage Jenkins -> Tools -> Python installations)
        python 'Python_3_9' // Cseréld ki a Python verziódnak megfelelő névre, amit beállítottál
    }

    stages {
        stage('Checkout Source Code') {
            steps {
                echo 'Source code checked out successfully from Git.'
                // A 'checkout scm' parancsot a Jenkins automatikusan futtatja,
                // ha a pipeline forrása "Pipeline script from SCM"
            }
        }

        stage('Install Python Dependencies') {
            steps {
                echo 'Installing Python dependencies from requirements.txt...'
                // A 'sh' parancs Linux shell parancsot futtat
                // Fontos: a Python környezet aktiválása a Jenkins számára
                sh 'python -m pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Running unit and integration tests with pytest...'
                // A 'pytest' futtatása, és a teszteredmények JUnit XML formátumba mentése
                sh 'pytest --junitxml=test-results.xml tests/'
            }
        }

        stage('Code Linting') {
            steps {
                echo 'Running code linter (flake8)...'
                // A flake8 futtatása a forráskódon
                // Az "|| true" gondoskodik róla, hogy a build ne bukjon el, ha vannak linter hibák/figyelmeztetések,
                // de a Warning Next Generation Plugin mégis gyűjteni tudja őket.
                sh 'flake8 src/ || true'
            }
        }

        stage('Archive Artifacts') {
            steps {
                echo 'Archiving test results and logs...'
                // Archiválja a teszteredmény XML fájlt. Ez később elemzésre kerül a 'post' blokkban.
                archiveArtifacts artifacts: 'test-results.xml', fingerprint: true
                // Ha szeretnéd archiválni a teljes Python forráskódot zip-ben:
                // sh 'zip -r project_source.zip src/ tests/ requirements.txt Jenkinsfile'
                // archiveArtifacts artifacts: 'project_source.zip', fingerprint: true
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished, checking overall status.'
        }
        success {
            echo 'Pipeline completed successfully! Publishing test results.'
            // Publikálja a JUnit teszteredményeket a Jenkins felületén
            junit 'test-results.xml'
            // Ide jöhetnek értesítések sikeres build esetén (pl. email)
        }
        failure {
            echo 'Pipeline failed! Please check console output for details.'
            // Ide jöhetnek értesítések sikertelen build esetén
        }
    }
}