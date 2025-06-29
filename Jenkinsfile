// Ez a fájl a Jenkinsfile. Groovy nyelven íródott.
pipeline {
    agent any

    stages {
        stage('Setup Environment') {
            steps {
                // A virtuális környezet létrehozása és aktiválása.
                // A 'sh' parancsokat most már a venv kontextusában futtatjuk.
                sh 'python3 -m venv venv'
                sh 'source venv/bin/activate && pip install -r requirements.txt'
                sh 'source venv/bin/activate && pip install build flake8 pytest-cov'
            }
        }

        stage('Build, Test & Analyze') {
            steps {
                // Mivel a pip install már lefutott, most futtatjuk az eszközöket.
                // Minden parancs előtt aktiváljuk a venv-et!
                sh 'source venv/bin/activate && flake8 --output-file=flake8-results.txt'
                sh 'source venv/bin/activate && pytest --junitxml=test-results.xml --cov=. --cov-report=xml'
            }
        }

        stage('Package') {
            steps {
                // Aktiváljuk a venv-et a build előtt is.
                sh 'source venv/bin/activate && python3 -m build'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    # Aktiváljuk a venv-et a deploy előtt is.
                    source venv/bin/activate
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
        // A 'post' blokkban a környezet már nem feltétlenül aktív,
        // így a riportok közzététele működik anélkül,
        // hogy a venv-et újra aktiválnánk,
        // mivel ezek a Jenkins pluginok beépített step-jei.
        always {
            junit testResults: 'test-results.xml', allowEmptyResults: true
            
            // A 'cobertura' paraméternév `coberturaReportFile`, nem csak 'cobertura'.
            // javítottam a szintaxist.
            cobertura coberturaReportFile: 'coverage.xml'
            
            // Javítottam a 'recordIssues' szintaxist a Flake8-hez,
            // a 'pyLint' helyett a 'flake8' beépített step-et kell használni.
            // A 'reportFile' paraméter a 'flake8' step-hez tartozik.
            recordIssues(
                tools: [
                    flake8(reportFile: 'flake8-results.txt')
                ]
            )
        }
        
        success {
            archiveArtifacts artifacts: 'dist/*.whl, dist/*.tar.gz', fingerprint: true, onlyIfSuccessful: true
            slackSend(color: 'good', message: "A ${env.JOB_NAME} build #${env.BUILD_NUMBER} SIKERESEN BEFEJEZŐDÖTT! :tada: <${env.BUILD_URL}|Build megtekintése>")
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