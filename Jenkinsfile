pipeline {
    agent {
        label "jenkins-python"
    }
    environment {
      ORG               = 'masterplanx'
      APP_NAME          = 'demo-mockapp'
      CHARTMUSEUM_CREDS = credentials('jenkins-x-chartmuseum')
    }
    stages {
      stage('CI Build and push snapshot') {
        when {
          branch 'PR-*'
        }
        environment {
          PREVIEW_VERSION = "0.0.0-SNAPSHOT-$BRANCH_NAME-$BUILD_NUMBER"
          PREVIEW_NAMESPACE = "$APP_NAME-$BRANCH_NAME".toLowerCase()
          HELM_RELEASE = "$PREVIEW_NAMESPACE".toLowerCase()
          PATH_APP = "/home/jenkins/workspace/masterplanx_demo-mockapp_master/"
        }
        steps {
          container('python') {
            sh 'export PYTHONPATH=:$PATH_APP'
            sh "python -m unittest"
            sh "pip install pytest coverage"
            sh "pip install pytest-runner flask redis"
            sh 'export PG_USER="username" && export PG_PASS=c2VjcmV0cGFzc3dvcmQ= && export PG_HOST=demodb-postgresql.jx.svc.cluster.local && export PG_DB=my-database && export REDIS_HOST=democache-redis-master.jx.svc.cluster.local && export RD_PASS=WFdWRjFnM3pMMA== && export REDIS_PORT2=6379 && PYTHONPATH=:/home/jenkins/workspace/masterplanx_demo-mockapp_master pytest'

            sh 'export VERSION=$PREVIEW_VERSION && skaffold build -f skaffold.yaml'


            sh "jx step post build --image $DOCKER_REGISTRY/$ORG/$APP_NAME:$PREVIEW_VERSION"
          }

          dir ('./charts/preview') {
           container('python') {
             sh "make preview"
             sh "jx preview --app $APP_NAME --dir ../.."
           }
          }
        }
      }
      stage('Build Release') {
        when {
          branch 'master'
        }
        steps {
          container('python') {
            // ensure we're not on a detached head
            sh "git checkout master"
            sh "git config --global credential.helper store"

            sh "jx step git credentials"
            // so we can retrieve the version in later steps
            sh "echo \$(jx-release-version) > VERSION"
          }
          dir ('./charts/demo-mockapp') {
            container('python') {
              sh "make tag"
            }
          }
          container('python') {
            sh "python -m unittest"
            sh "pip install pytest coverage pytest-runner"
            sh "pip install flask flask_migrate redis"
            sh 'export PG_USER="username" && export PG_PASS=c2VjcmV0cGFzc3dvcmQ= && export PG_HOST=demodb-postgresql.jx.svc.cluster.local && export PG_DB=my-database && export REDIS_HOST=democache-redis-master.jx.svc.cluster.local && export RD_PASS=WFdWRjFnM3pMMA== && export REDIS_PORT2=6379 && PYTHONPATH=:/home/jenkins/workspace/masterplanx_demo-mockapp_master pytest'

            sh 'export VERSION=`cat VERSION` && skaffold build -f skaffold.yaml'

            sh "jx step post build --image $DOCKER_REGISTRY/$ORG/$APP_NAME:\$(cat VERSION)"
          }
        }
      }
      stage('Promote to Environments') {
        when {
          branch 'master'
        }
        steps {
          dir ('./charts/demo-mockapp') {
            container('python') {
              sh 'jx step changelog --version v\$(cat ../../VERSION)'

              // release the helm chart
              sh 'jx step helm release'

              // promote through all 'Auto' promotion Environments
              sh 'jx promote -b --all-auto --timeout 1h --version \$(cat ../../VERSION)'
            }
          }
        }
      }
    }
    post {
        always {
            cleanWs()
        }
    }
  }
