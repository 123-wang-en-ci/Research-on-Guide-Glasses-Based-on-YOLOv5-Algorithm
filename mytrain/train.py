from ultralytics import YOLO
import os
import torch
print(os.getcwd())
model = YOLO("yolov5.yaml")
model = YOLO("yolov5n.pt", task="detect")

model.predict("D:/ultralytics-main/ultralytics-main/mytrain/zidane.jpeg",save=True,imgsz=640,conf=0.5)