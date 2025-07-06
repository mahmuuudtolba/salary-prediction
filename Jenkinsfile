pipeline {
    agent any

    environment {
        GCP_PROJECT = "ecstatic-seeker-464205-c0"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        // Define the image name as a variable to avoid typos
        IMAGE_NAME = "gcr.io/${GCP_PROJECT}/salary-prediction-project:latest"
    }

    stages {
        stage('Cloning Github Repo') {
            steps {
                echo 'Cloning github repo to jenkins............'
                checkout scmGit(branches: [[name: '*/main']], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/mahmuuudtolba/salary-prediction']])
            }u
        }

        // This stage is not necessary for the Docker build, but kept if you have other uses for it.
        // The Docker build will handle its own dependencies inside the container.
        stage('Setting up Local Virtual Environment') {
            steps {
                script {
                    echo 'Setting up our virtual environment and installing dependencies............'
                    sh '''
                        python -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    '''
                }
            }
        }

        stage('Build and Push Docker Image to GCR') {
            steps {
                // Use a single, consistent credential ID and variable name
                withCredentials([file(credentialsId: 'GCP-key', variable: 'GCP_KEY_FILE')]) {
                    script {
                        echo 'Building and Pushing Docker Image to GCR............'
                        sh '''
                            # Set the path for gcloud CLI
                            export PATH=$PATH:${GCLOUD_PATH}

                            # Authenticate with GCP and configure Docker
                            gcloud auth activate-service-account --key-file=${GCP_KEY_FILE}
                            gcloud config set project ${GCP_PROJECT}
                            gcloud auth configure-docker --quiet

                            # Enable Docker BuildKit and build the image with the secret
                            echo "Building image: ${IMAGE_NAME}"
                            export DOCKER_BUILDKIT=1
                            docker build --secret id=gcp-credentials,src=${GCP_KEY_FILE} -t ${IMAGE_NAME} .

                            # Push the image to GCR
                            docker push ${IMAGE_NAME}
                        '''
                    }
                }
            }
        }

        stage('Deploy to Google Cloud Run') {
            steps {
                // Use the same credential ID for consistency
                withCredentials([file(credentialsId: 'GCP-key', variable: 'GCP_KEY_FILE')]) {
                    script {
                        echo 'Deploying to Google Cloud Run............'
                        sh '''
                            # Set the path for gcloud CLI
                            export PATH=$PATH:${GCLOUD_PATH}

                            # Re-authentication is good practice if running on different agents, but can be optional
                            gcloud auth activate-service-account --key-file=${GCP_KEY_FILE}
                            gcloud config set project ${GCP_PROJECT}

                            # Deploy the correct image that was just built
                            gcloud run deploy hotel-reservation \
                                --image=${IMAGE_NAME} \
                                --platform=managed \
                                --region=us-central1 \
                                --allow-unauthenticated
                        '''
                    }
                }
            }
        }
    }
}