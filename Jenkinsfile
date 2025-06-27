// Ez a fájl a Jenkinsfile. Groovy nyelven íródott.

// A 'pipeline' blokk a teljes folyamatot definiálja.
pipeline {
    // 'agent any' azt jelenti, hogy a Jenkins bármelyik elérhető node-on futtathatja a pipeline-t.
    agent any

    // 'stages' blokk, ami a build folyamat fázisait tartalmazza.
    stages {
        // -- Stage 1: Checkout --
        // Ez a stage automatikusan lefut, amikor a pipeline elindul,
        // klónozza a repositoryt. Ezt nem kell expliciten definiálni.

        // -- Stage 2: Build & Test --
        stage('Build & Test') {
            // A 'steps' blokk tartalmazza a stage-en belüli parancsokat.
            steps {
                // Itt futnak a shell parancsok, amik korábban a Build Steps-ben voltak.
                // A Jenkins Pipeline automatikusan aktiválja a venv-et, ha a pip install-t meghívod
                // és a python parancsokat a venv/bin/activate kontextusában futtatod.

                // Pip install build és egyéb függőségek
                sh 'pip install -r requirements.txt'
                sh 'pip install build flake8 pytest-cov'

                // Futtatjuk a statikus elemzést, a teszteket és a coverage-t.
                // Az 'sh' parancs futtatja a shell szkriptet.
                sh 'flake8 --output-file=flake8-results.txt'
                sh 'pytest --junitxml=test-results.xml --cov=. --cov-report=xml'
            }
        }

        // -- Stage 3: Package --
        stage('Package') {
            steps {
                sh 'python3 -m build'
            }
        }

        // -- Stage 4: Deploy --
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
        // --- Teszt riportok ---
        // A 'junit' step a Publish JUnit test result report funkciója.
        always {
            // A 'test-results.xml' fájlt dolgozza fel.
            // A 'testResults' opcióval is lehet hivatkozni rá.
            junit testResults: 'test-results.xml', allowEmptyResults: true, keepLongStdio: true
        }

        // --- Kódlefedettség (Coverage) ---
        // A 'cobertura' step a Publish Cobertura Coverage Report funkciója.
        always {
            // A Cobertura XML riportot dolgozza fel.
            cobertura autoUpdateHealth: false, autoUpdateSource: false, branchCoverageTargets: '70, 0, 0', conditionalCoverageTargets: '70, 0, 0', lineCoverageTargets: '70, 0, 0', failUnhealthy: false, failUnstable: false, sourceFileDepth: 0, enableSourceFileRetention: false, sourceEncoding: 'UTF-8', coberturaReportFile: 'coverage.xml'
        }

        // --- Kódminőség (Warnings) ---
        // A 'recordIssues' step a Record compiler warnings and static analysis results funkciója.
        always {
            recordIssues(
                tools: [
                    pyLint(pattern: 'flake8-results.txt', name: 'Flake8')
                ],
                aggregatingResults: true,
                skipBlames: true,
                skipChecks: true
            )
        }

        // --- Artifact Archiválás ---
        // Az 'archiveArtifacts' step az Archive the artifacts funkciója.
        success {
            archiveArtifacts artifacts: 'dist/*.whl, dist/*.tar.gz', fingerprint: true, onlyIfSuccessful: true
        }

        // --- E-mail értesítés ---
        // Az 'emailext' step az Editable Email Notification funkciója.
        failure {
            emailext(
                subject: '$PROJECT_NAME - Build #$BUILD_NUMBER - $BUILD_STATUS!',
                body: '$PROJECT_NAME - Build #$BUILD_NUMBER ($BUILD_URL) - Státusz: $BUILD_STATUS\n\n' +
                      'A build log:\n\n' +
                      '${BUILD_LOG}',
                to: 'peter.pivarcsik@yahoo.com'
            )
        }
        
        // --- Slack értesítés ---
        // A 'slackSend' step a Slack Notifications funkciója.
        failure {
            slackSend(color: 'danger', message: "A ${env.JOB_NAME} build #${env.BUILD_NUMBER} HIBÁVAL VÉGZŐDÖTT! <${env.BUILD_URL}|Build megtekintése>")
        }
        success {
            slackSend(color: 'good', message: "A ${env.JOB_NAME} build #${env.BUILD_NUMBER} SIKERESEN BEFEJEZŐDÖTT! :tada: <${env.BUILD_URL}|Build megtekintése>")
        }
        aborted {
            slackSend(color: 'warning', message: "A ${env.JOB_NAME} build #${env.BUILD_NUMBER} MEGSZAKÍTVA! :warning: <${env.BUILD_URL}|Build megtekintése>")
        }
    }
}