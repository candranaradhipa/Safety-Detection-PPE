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




