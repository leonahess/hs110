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
    stage('Deploy to leon-raspi-cluster-3') {
      agent {
        label "master"
      }
      steps {
        sshagent(credentials: ['d4eb3f5d-d0f5-4964-8bad-038f0d774551']) {
          sh "ssh -o StrictHostKeyChecking=no pi@leon-raspi-cluster-3 docker kill hs110"
          sh "ssh -o StrictHostKeyChecking=no pi@leon-raspi-cluster-3 docker rm hs110"
          sh "ssh -o StrictHostKeyChecking=no pi@leon-raspi-cluster-3 docker run --restart always -d --name=hs110 --net=host fx8350:5000/hs110:latest"
        }
      }
    }
  }
}
