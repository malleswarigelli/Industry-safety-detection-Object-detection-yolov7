# DL-ISD-yolov7

# Industry-Safety-Detection-using-YOLOv7

ISD: industry safety detection, 
Purpose is creating a detection system using Computer vision and Machine Learning to monitor, track and enforce employees/workers to wear necessary safety gears. ISD is designed and modelled to take a real-time image of the personnel as input and determining if five segments - helmet, gloves, jacket, goggles and footwear are worn before entering the workplace, and record the procedure as well. If ISD doesn't find any of the five safety gears, the worker will not be allowed to proceed and prohibition alarm in the system will alert the security authorities.

Since real time image used for object detection, inference time is higher, so use YOLO series (since its state of the art model and, model size is also less)

- [Data link](https://drive.google.com/file/d/1ab3Qu8t14YyoNTFszfe1xVDOf92wip05/view?usp=drive_link)
- [Yolov7 Github repo link](https://github.com/WongKinYiu/yolov7)
- [Yolov7 Tutorial](https://youtube.com/playlist?list=PLkz_y24mlSJagh6O2MIrgI-Ki-t1rhjLI&si=6eMTgSe1-cbWVPGX)


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