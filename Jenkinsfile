pipeline {
  agent any
  triggers {
    pollSCM('H/15 * * * *')
  }
  stages {
    stage('Build Container') {
      agent {
        label "Pi_3"
      }
      steps {
        sh "docker build -t hs110 ."
      }
    }
    stage('Tag Container') {
      agent {
        label "Pi_3"
      }
      steps {
        sh "docker tag hs110 fx8350:5000/hs110:latest"
        sh "docker tag hs110 fx8350:5000/hs110:${env.BUILD_NUMBER}"
        sh "docker tag hs110 leonhess/hs110:latest"
        sh "docker tag hs110 leonhess/hs110:${env.BUILD_NUMBER}"
      }
    }
    stage('Push Registries') {
      parallel {
        stage('Push to local Registry') {
          agent {
            label "Pi_3"
          }
          steps {
            sh "docker push fx8350:5000/hs110:${env.BUILD_NUMBER}"
            sh "docker push fx8350:5000/hs110:latest"
          }
        }
        stage('Push to DockerHub') {
          agent {
            label "Pi_3"
          }
          steps {
            withDockerRegistry([credentialsId: "dockerhub", url: ""]) {
              sh "docker push leonhess/hs110:${env.BUILD_NUMBER}"
              sh "docker push leonhess/hs110:latest"
            }
          }
        }
      }
    }
    stage('Cleanup') {
      agent {
        label "Pi_3"
      }
      steps {
        sh "docker rmi fx8350:5000/hs110:latest"
        sh "docker rmi fx8350:5000/hs110:${env.BUILD_NUMBER}"
        sh "docker rmi leonhess/hs110:latest"
        sh "docker rmi leonhess/hs110:${env.BUILD_NUMBER}"
      }
    }
    stage('Deploy to swarm') {
      agent {
        label "master"
      }
      steps {
        ansiblePlaybook(
          playbook: 'deploy_to_swarm.yml',
          credentialsId: '78c069cd-77c4-4c91-89cc-7805f3c9cfe2'
          )
        }
      }
    }
  }
