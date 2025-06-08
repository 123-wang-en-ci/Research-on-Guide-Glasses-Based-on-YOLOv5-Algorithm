from ultralytics import YOLO
 
# 加载预训练的YOLOv11n模型
model = YOLO(r"D:\ultralytics-main\ultralytics-main\yolov11\runs\runs\train\exp2\weights\best.pt")
 
# 对'bus.jpg'图像进行推理，并获取结果
results = model.predict(r"D:\ultralytics-main\ultralytics-main\datasets\images\pre\2.jpg", save=True, imgsz=640, conf=0.5)
 
# 处理返回的结果
for result in results:
    boxes = result.boxes       # 获取边界框信息
    result.show()              # 显示结果