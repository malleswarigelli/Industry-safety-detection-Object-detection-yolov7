# Industry-Safety-Detection-using-YOLOv7

ISD: industry safety detection, 
Purpose is creating a detection system using Computer vision and Machine Learning to monitor, track and enforce employees/workers to wear necessary safety gears. ISD is designed and modelled to take a real-time image of the personnel as input and determining if five segments - helmet, gloves, jacket, goggles and footwear are worn before entering the workplace, and record the procedure as well. If ISD doesn't find any of the five safety gears, the worker will not be allowed to proceed and prohibition alarm in the system will alert the security authorities.

Since real time image used for object detection, inference time is higher, so use YOLO series (since its state of the art model and, model size is also less)

- [Data link](https://drive.google.com/file/d/1ab3Qu8t14YyoNTFszfe1xVDOf92wip05/view?usp=drive_link)
- [Yolov7 Github repo link](https://github.com/WongKinYiu/yolov7)
- [Yolov7 Tutorial](https://youtube.com/playlist?list=PLkz_y24mlSJagh6O2MIrgI-Ki-t1rhjLI&si=6eMTgSe1-cbWVPGX)

# Flow of End to End robust automatic pipeline:
![ISD_End to End_Architexture](https://github.com/malleswarigelli/Industry-safety-detection-Object-detection-yolov7/assets/84688050/532c9a14-8893-42f7-bdad-4b9cd8bca508)

- Data Ingestion: We annotated, labelled images using Roboflow. Annotated data is downloaded as .zip file from AWS s3 bucket, unzip images
- Data Validation: We added data validation component in this project since it relies on multiple folders, files that would be generated from data_ingestion component. This component would check if all 
      the needed files exist or not, captured in validation status.   
- No data transformation needed in this case because we directly sending the image to model_training. No image preprocessing required.
- Model Training: This component triggers if validation_status from data validation component is true. We trained with a pre-trained model, YOLOv7 to
        perform real-time object detection inference on images.
        - YOLOv7 performs faster with higher accuracy than previous models due to less number of parameters and higher computational efficiency
- Model Pusher: Trained model is pushed to AWS s3

- Deployed the pipeline to AWS EC2 using containers Docker, AWS ECR, CI/CD tool GitHub Actions
- Built user application with Flask
  
# Git commands
```bash
- git add .
- git commit -m "Updated"
- git push origin main
```

# How to run?
- conda create -n isd python=3.8 -y
- conda activate isd
- pip install -r requirements.txt
- python app.py

# AWS Configurations
#aws cli download link: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

```bash
aws configure
```

# AWS-CICD-Deployment-with-Github-Actions
## 1. Login to AWS console.
## 2. Create IAM user for deployment

#with specific access
- EC2 access : It is virtual machine
- ECR: Elastic Container registry to save your docker image in aws

#Description: About the deployment
- Build docker image of the source code
- Push your docker image to ECR
- Launch Your EC2 
- Pull Your image from ECR in EC2
- Lauch your docker image in EC2

#Policy:
- AmazonEC2ContainerRegistryFullAccess
- AmazonEC2FullAccess

## 3. Create ECR repo to store/save docker image
- Save the URI: 637423357032.dkr.ecr.us-east-2.amazonaws.com/yolov7ecr
## 4. Create EC2 machine (Ubuntu)

## 5. Open EC2 and Install docker in EC2 Machine:

#optinal
- sudo apt-get update -y
- sudo apt-get upgrade

#required
- curl -fsSL https://get.docker.com -o get-docker.sh
- sudo sh get-docker.sh
- sudo usermod -aG docker ubuntu
- newgrp docker

## 6. Configure EC2 as self-hosted runner:
- setting>actions>runner>new self hosted runner> choose os> then run command one by one

## 7. Setup github secrets:

- AWS_ACCESS_KEY_ID=
- AWS_SECRET_ACCESS_KEY=
- AWS_REGION = us-east-2
- AWS_ECR_LOGIN_URI = demo>>  637423357032.dkr.ecr.us-east-2.amazonaws.com
- ECR_REPOSITORY_NAME = yolov7ecr
