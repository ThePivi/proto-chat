// Ez a fájl a Jenkinsfile. Groovy nyelven íródott.
pipeline {
    agent any

    environment {
        // A 'PATH' környezeti változó kibővítése a virtuális környezet 'bin' mappájával.
        // Ez biztosítja, hogy a Jenkins megtalálja a venv-ben telepített eszközöket.
        PATH = "${WORKSPACE}/venv/bin:${PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
            }
        }
        stage('Setup Environment') {
            steps {
                // A virtuális környezet létrehozása és a függőségek telepítése.
                // Mivel a PATH be van állítva, nem kell aktiválni a venv-et.
                sh 'python3 -m venv venv'
                sh 'pip install --upgrade pip' // Frissítjük a pip-et
                sh 'pip install -r requirements.txt'
                sh 'pip install build flake8 pytest-cov'
            }
        }

        stage('Build, Test & Analyze') {
            steps {
                // Mivel a PATH be van állítva, a pip, pytest, flake8 parancsok
                // automatikusan a venv-ben lévő verziókra hivatkoznak.
                sh 'flake8 --output-file=flake8-results.txt || true'
                sh 'cat flake8-results.txt'
                sh 'pytest --junitxml=test-results.xml --cov=. --cov-report=xml'
            }
        }

        stage('Package') {
            steps {
                // A `python3` is a venv-ből fut, mivel a PATH be van állítva.
                sh 'python3 -m build'
            }
        }

        stage('Deploy') {
            steps {
                // Itt is a venv-ből futnak a parancsok, ha szükséges.
                sh '''
                    if ls dist/*.whl 1> /dev/null 2>&1; then
                        echo "Virtuális deploy elindult..."
                        echo "A buildelt csomagok: "
                        ls dist/
                        echo "A csomag sikeresen elmentve a Jenkinsben! A telepítés befejeződött."
                    else
                        echo "HIBA: Nem találok buildelt fájlokat a 'dist/' mappában. A deploy megszakad."
                        exit 1
                    fi
                '''
            }
        }
    }

    post {
        // A post blokkban lévő step-ek továbbra is működnek,
        // nem kell aktiválni a venv-et nekik.
        always {
            junit testResults: 'test-results.xml', allowEmptyResults: true
            cobertura coberturaReportFile: 'coverage.xml'
            recordIssues(
                tools: [
                    flake8(pattern: 'flake8-results.txt') // A 'reportFile' paramétert a 'pattern' váltotta fel
                ]
            )
        }
        
        success {
            archiveArtifacts artifacts: 'dist/*.whl, dist/*.tar.gz', fingerprint: true, onlyIfSuccessful: true
            slackSend(color: 'good', message: "A ${env.JOB_NAME} build #${env.BUILD_NUMBER} SIKERESEN BEFEJEZŐDÖTT! :tada: <${env.BUILD_URL}|Build megtekintése>")
            emailext(
                subject: '$PROJECT_NAME - Build #$BUILD_NUMBER - $BUILD_STATUS!',
                body: '$PROJECT_NAME - Build #$BUILD_NUMBER ($BUILD_URL) - Státusz: $BUILD_STATUS\n\n' +
                      'A build log:\n\n' +
                      '${BUILD_LOG}',
                to: 'peter.pivarcsik@yahoo.com'
            )
        }

        failure {
            emailext(
                subject: '$PROJECT_NAME - Build #$BUILD_NUMBER - $BUILD_STATUS!',
                body: '$PROJECT_NAME - Build #$BUILD_NUMBER ($BUILD_URL) - Státusz: $BUILD_STATUS\n\n' +
                      'A build log:\n\n' +
                      '${BUILD_LOG}',
                to: 'peter.pivarcsik@yahoo.com'
            )
            slackSend(color: 'danger', message: "A ${env.JOB_NAME} build #${env.BUILD_NUMBER} HIBÁVAL VÉGZŐDÖTT! <${env.BUILD_URL}|Build megtekintése>")
        }

        aborted {
            slackSend(color: 'warning', message: "A ${env.JOB_NAME} build #${env.BUILD_NUMBER} MEGSZAKÍTVA! :warning: <${env.BUILD_URL}|Build megtekintése>")
        }
    }
}