# Salary Prediction With GCP
 
This is a implementation of the classification model for salary prediction.

## Requirements
- python 3.10 or later


#### install python using Anaconda

## Installation 

```bash
conda create --prefix ./venv python=3.10 -y
```

### Install the required packages
```bash
$ pip install -r requirements.txt
```

### Run application locally
Run the pipeline
```bash
$ python pipeline/training_pipeline.py
```

Lanuch the flask app
```bash
$ python application.py
```

## Docker

#### Build docker image
- go incide custom_jenkins 
```bash
docker build -t jenkins-mlops
```

#### Run docker container

```bash
docker run -d --name jenkins-mlops-container --privileged -p 8080:8080 -p 50000:50000 -v /var/run/docker.sock:/var/run/docker.sock -v jenkins_home:/var/jenkins_home -v jenkins_dind:/var/lib/docker  jenkins-mlops
```
#### Setup jenkins container
- get inside the container bash
```bash
docker exec -u root -it jenkins-mlops-container bash
```
- Install Python Inside Jenkins Container
```bash
apt update -y
apt install -y python3
python3 --version
ln -s /usr/bin/python3 /usr/bin/python
python --version
apt install -y python3-pip
apt install -y python3-venv
exit
```

- Restart the jenkins contianer
 ```bash
docker restart jenkins-mlops-container
 ```

- Installing GCP CLI
```bash
docker exec -u root -it jenkins-mlops-container bash
apt-get update
apt-get install -y curl apt-transport-https ca-certificates gnupg
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
apt-get update && apt-get install -y google-cloud-sdk
gcloud --version
exit
```

- Grant Docker Permissions
```bash
docker exec -u root -it jenkins-mlops-container bash
groupadd docker
usermod -aG docker jenkins
usermod -aG root jenkins
exit
```
- Restart the jenkins contianer
 ```bash
docker restart jenkins-mlops-container
 ```



