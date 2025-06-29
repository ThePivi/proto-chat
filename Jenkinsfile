// Ez a fájl a Jenkinsfile. Groovy nyelven íródott.
pipeline {
    agent any

    stages {
        stage('Build & Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pip install build flake8 pytest-cov'

                sh 'flake8 --output-file=flake8-results.txt'
                sh 'pytest --junitxml=test-results.xml --cov=. --cov-report=xml'
            }
        }

        stage('Package') {
            steps {
                sh 'python3 -m build'
            }
        }

        stage('Deploy') {
            steps {
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

    // A 'post' blokk a build befejezése után fut le.
    post {
        // --- Teszt riportok, Kódlefedettség, Kódminőség (mindig lefut) ---
        always {
            // Teszt riportok - JUnit
            junit testResults: 'test-results.xml', allowEmptyResults: true

            // Kódlefedettség (Coverage) - Cobertura
            // Az "autoUpdateSource" és "enableSourceFileRetention" paraméterek helytelenek voltak,
            // a sourceFileDepth elavult, a sourceEncoding pedig objektumot vár.
            // A legegyszerűbb, ha a Cobertura DSL-jét használjuk, ami a plugin dokumentációjában van.
            // A paraméternevek függnek a plugin verziójától!
            // Próbáljuk ki a legújabb szintaxissal.
            script {
                try {
                    cobertura coberturaReportFile: 'coverage.xml'
                } catch(e) {
                    echo "Cobertura riport készítése sikertelen: ${e}"
                }
            }

            // Kódminőség (Warnings) - Record Issues
            recordIssues(
                tools: [
                    flake8(reportFile: 'flake8-results.txt')
                ],
                aggregatingResults: true,
                skipBlames: true
            )
        }
        
        // --- Artifact Archiválás (csak sikeres build esetén) ---
        success {
            archiveArtifacts artifacts: 'dist/*.whl, dist/*.tar.gz', fingerprint: true, onlyIfSuccessful: true

            // Slack értesítés sikeres build esetén
            slackSend(color: 'good', message: "A ${env.JOB_NAME} build #${env.BUILD_NUMBER} SIKERESEN BEFEJEZŐDÖTT! :tada: <${env.BUILD_URL}|Build megtekintése>")
        }

        // --- E-mail és Slack értesítés (csak sikertelen build esetén) ---
        failure {
            emailext(
                subject: '$PROJECT_NAME - Build #$BUILD_NUMBER - $BUILD_STATUS!',
                body: '$PROJECT_NAME - Build #$BUILD_NUMBER ($BUILD_URL) - Státusz: $BUILD_STATUS\n\n' +
                      'A build log:\n\n' +
                      '${BUILD_LOG}',
                to: 'peter.pivarcsik@yahoo.com'
            )
            // Slack értesítés hibás build esetén
            slackSend(color: 'danger', message: "A ${env.JOB_NAME} build #${env.BUILD_NUMBER} HIBÁVAL VÉGZŐDÖTT! <${env.BUILD_URL}|Build megtekintése>")
        }

        // --- Slack értesítés megszakított build esetén ---
        aborted {
            slackSend(color: 'warning', message: "A ${env.JOB_NAME} build #${env.BUILD_NUMBER} MEGSZAKÍTVA! :warning: <${env.BUILD_URL}|Build megtekintése>")
        }
    }
}