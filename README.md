# Safety Detection PPE with YOLO

## Overview
Safety Detection PPE with YOLO is a safety monitoring system designed to detect and verify whether individuals comply with the mandatory use of complete Personal Protective Equipment (PPE) in designated work areas. This project was developed as an application of Artificial Intelligence (AI), particularly computer vision, to perform object detection and assess PPE completeness from CCTV footage installed in specific monitoring locations.

The system employs the You Only Look Once (YOLO) algorithm, a pre-trained object detection model developed by Ultralytics. YOLO was selected because of its high detection accuracy, real-time processing capability, and widespread adoption in object detection research and industrial applications.

In addition, a Graphical User Interface (GUI) was developed to provide an interactive platform that integrates the detection system with end users. CCTV footage is uploaded through the GUI and subsequently processed by the YOLO algorithm to identify each type of PPE worn by individuals. The detection results are displayed using colored bounding boxes and class labels for each detected object. Properly worn PPE, including helmet, mask, gloves, safety boots, and coveralls, is indicated by green bounding boxes. Conversely, missing PPE is identified with the labels no-helmet, no-mask, no-gloves, no-safety boots, and no-coveralls, which are displayed using red bounding boxes.

Based on the detection results, the system determines the overall safety status of the monitored area. A "Safe" status is displayed when all detected individuals are wearing the required PPE completely, while a "Not Safe" status is issued when one or more required PPE items are missing for any detected individual.

## Tools
- Python 3 Environments
- Visual Studio Code (optional)
- Python libraries (Tkinter, cv2, threading, time, YOLO, sys, PIL)

## Video Demo
The system is capable of processing videos in various file formats and resolution levels. Higher-resolution videos generally provide sharper visual details, enabling the system to detect objects more accurately and reliably.

### Video demo details :
- Length : 02:59
- Frame width : 1280
- Frame height : 720
- Frame rate : 30.00 frames/second

https://github.com/user-attachments/assets/18b872fe-2cb3-4511-a333-cddbdd7a0dce


> ### Graphical User Interface <a name = 'gui'></a>

The GUI consists of several main components that support the operation of the application, including:

* **Video preview area**, which displays the selected video before the detection process begins.
* **"Select Video"** feature, which allows users to browse and upload the video to be processed by the system.
* **"Start Detection"** feature, which initiates the detection process after a video has been successfully uploaded.
* **"Exit"** feature, which closes the application and terminates the system.

<img width="1037" height="895" alt="image" src="https://github.com/user-attachments/assets/9b9890df-9ace-4654-84b2-6d69e019adc4" />

> ### Previewing The Uploaded Video <a name = 'preview'></a>

After the video has been successfully uploaded into the system, it will first be displayed in a preview format to allow the user to ensure that the selected file is correct and corresponds to the video intended for detection. This preview feature enables users to verify the video content before the detection process begins, thereby reducing the possibility of selecting an incorrect video.

<img width="1097" height="756" alt="image" src="https://github.com/user-attachments/assets/ad318d98-9951-499d-b9e4-68b821aad327" />

> ### Detection System Workflow <a name = 'Workflow'></a>

Technically, this code works by capturing the video stream from a camera or CCTV system through `cv2.VideoCapture`, then loading a trained YOLO model from the `best.pt` file to perform inference on each frame repeatedly within the main loop. Each frame that is successfully read is sent to the model using `model(img, stream=True)`, after which the detection results are processed one by one to extract the bounding box coordinates, confidence score, and class index. The class index is then matched with the previously defined list of class names. After that, the system applies a confidence threshold, assigns green color to safe PPE classes, red color to violation classes such as `No-Helmet` or `No-Mask`, and plays an alarm through `pygame` using `threading` so that the sound can run without interrupting the detection process, while the alarm delay is controlled to prevent it from sounding continuously. The final results are displayed directly in the video window with labels and bounding boxes, and the program stops when the user presses the `q` key, after which the camera is released and all windows are closed.

> ### Application Simulation Video <a name = 'Apps'></a>

Simulation Video of the System with an Integrated GUI Application


https://github.com/user-attachments/assets/b9c156a9-0ebc-4b07-9c49-3d5cec5d1a65

## Contributor
[**Candra Naradhipa Cahyakusuma**](https://github.com/candranaradhipa)
[Robotics and AI Engineering](https://ftmm.unair.ac.id/teknik-robotika-dan-kecerdasan-buatan-program-studi/), [Universitas Airlangga](https://unair.ac.id/)
<candradhipa16@gmail.com>

