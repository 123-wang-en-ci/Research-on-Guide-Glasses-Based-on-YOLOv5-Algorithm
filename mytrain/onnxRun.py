#coding:utf-8
import argparse
import cv2
import numpy as np
import onnxruntime as ort
from ultralytics.utils import ASSETS, yaml_load
from ultralytics.utils.checks import check_requirements, check_yaml
from ultralytics import YOLO
import time
import torch
 
# 导出onnx模型
# model = YOLO("yolov8n.pt")
# model.export(format="onnx")
 
class YOLOv8:
    """YOLOv8目标检测模型类，用于处理推理和可视化操作。"""
    def __init__(self, onnx_model, confidence_thres, iou_thres):
        """
        初始化YOLOv8类的实例。
        参数:
            onnx_model: ONNX模型的路径。
            confidence_thres: 过滤检测的置信度阈值。
            iou_thres: 非极大抑制的IoU（交并比）阈值。
        """
        self.input_height = None
        self.input_width = None
        self.img = None
        self.img_width = None
        self.img_height = None
        self.onnx_model = onnx_model
        self.confidence_thres = confidence_thres
        self.iou_thres = iou_thres
 
        # 从COCO数据集的配置文件加载类别名称
        self.classes = yaml_load(check_yaml("coco8.yaml"))["names"]
        # 字典存储类别名称
        # print(self.classes)
        # {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane'...}
 
        # 为类别生成颜色调色板
        self.color_palette = np.random.uniform(0, 255, size=(len(self.classes), 3))
 
        # 初始化ONNX会话
        self.initialize_session(self.onnx_model)
 
    def draw_detections(self, img, box, score, class_id):
        """
        根据检测到的对象在输入图像上绘制边界框和标签。
        参数:
            img: 要绘制检测的输入图像。
            box: 检测到的边界框。
            score: 对应的检测得分。
            class_id: 检测到的对象的类别ID。
        返回:
            None
        """
 
        # 提取边界框的坐标
        x1, y1, w, h = box
 
        # 获取类别ID对应的颜色
        color = self.color_palette[class_id]
 
        # 在图像上绘制边界框
        cv2.rectangle(img, (int(x1), int(y1)), (int(x1 + w), int(y1 + h)), color, 2)
 
        # 创建包含类名和得分的标签文本
        label = f"{self.classes[class_id]}: {score:.2f}"
 
        # 计算标签文本的尺寸
        (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
 
        # 计算标签文本的位置
        label_x = x1
        label_y = y1 - 10 if y1 - 10 > label_height else y1 + 10
 
        # 绘制填充的矩形作为标签文本的背景
        cv2.rectangle(
            img, (label_x, label_y - label_height), (label_x + label_width, label_y + label_height), color, cv2.FILLED
        )
 
        # 在图像上绘制标签文本
        cv2.putText(img, label, (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
 
    def preprocess(self,frame):
        """
        在进行推理之前，对输入图像进行预处理。
        返回:
            image_data: 预处理后的图像数据，准备好进行推理。
        """
        # 使用OpenCV读取输入图像(h,w,c)(1 c h w)
        self.img = frame
 
        # 获取输入图像的高度和宽度
        self.img_height, self.img_width = self.img.shape[:2]
 
        # 将图像颜色空间从BGR转换为RGB
        img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
 
        # 将图像调整为匹配输入形状(640,640,3)
        img = cv2.resize(img, (self.input_width, self.input_height))
 
        # 将图像数据除以255.0进行归一化
        image_data = np.array(img) / 255.0
 
        # 转置图像，使通道维度成为第一个维度(3,640,640)
        image_data = np.transpose(image_data, (2, 0, 1))  # 通道优先
 
        # 扩展图像数据的维度以匹配期望的输入形状(1,3,640,640)
        image_data = np.expand_dims(image_data, axis=0).astype(np.float32)
 
        # 返回预处理后的图像数据
        return image_data
 
    def postprocess(self, input_image, output):
        """
        对模型的输出进行后处理，以提取边界框、分数和类别ID。
        参数:
            input_image (numpy.ndarray): 输入图像。
            output (numpy.ndarray): 模型的输出。
        返回:
            numpy.ndarray: 输入图像，上面绘制了检测结果。
        """
        # 转置并压缩输出以匹配期望的形状：(8400, 84)
        outputs = np.transpose(np.squeeze(output[0]))
        # 获取输出数组的行数
        rows = outputs.shape[0]
        # 存储检测到的边界框、分数和类别ID的列表
        boxes = []
        scores = []
        class_ids = []
        # 计算边界框坐标的比例因子
        x_factor = self.img_width / self.input_width
        y_factor = self.img_height / self.input_height
# NMS(非极大值抑制)
        # 遍历输出数组的每一行
        for i in range(rows):
            # 从当前行提取类别的得分
            classes_scores = outputs[i][4:]
            # 找到类别得分中的最大值
            max_score = np.amax(classes_scores)
 
            # 如果最大得分大于或等于置信度阈值
            if max_score >= self.confidence_thres:
                # 获取得分最高的类别ID
                class_id = np.argmax(classes_scores)
 
                # 从当前行提取边界框坐标
                x, y, w, h = outputs[i][0], outputs[i][1], outputs[i][2], outputs[i][3]
                # 计算边界框的缩放坐标
                left = int((x - w / 2) * x_factor)
                top = int((y - h / 2) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
 
                # 将类别ID、得分和边界框坐标添加到相应的列表中
                class_ids.append(class_id)
                scores.append(max_score)
                boxes.append([left, top, width, height])
 
        # 应用非极大抑制以过滤重叠的边界框
        indices = cv2.dnn.NMSBoxes(boxes, scores, self.confidence_thres, self.iou_thres)
 
        # 遍历非极大抑制后选择的索引
        for i in indices:
            # 获取与索引对应的边界框、得分和类别ID
            box = boxes[i]
            score = scores[i]
            class_id = class_ids[i]
            # 在输入图像上绘制检测结果
            self.draw_detections(input_image, box, score, class_id)
        # 返回修改后的输入图像
        return input_image
 
    def initialize_session(self, onnx_model):
        """
        初始化ONNX模型会话。
        :return:
        """
        # if torch.cuda.is_available():
        #     print("Using CUDA")
        #     providers = ["CUDAExecutionProvider"]
        # else:
        #     print("Using CPU")
        #     providers = ["CPUExecutionProvider"]
        providers = ["CPUExecutionProvider"]
        session_options = ort.SessionOptions()
        session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        # 使用ONNX模型创建推理会话，并指定执行提供者
        self.session = ort.InferenceSession(onnx_model,
                                            session_options=session_options,
                                            providers=providers)
        return self.session
 
    def main(self,frame):
        """
        使用ONNX模型进行推理，并返回带有检测结果的输出图像。
        返回:
            output_img: 带有检测结果的输出图像。
        """
        # 获取模型的输入
        model_inputs = self.session.get_inputs()
        # 保存输入的形状，稍后使用
        # input_shape：(1,3,640,640)
        # self.input_width:640,self.input_height:640
        input_shape = model_inputs[0].shape
        self.input_width = input_shape[2]
        self.input_height = input_shape[3]
        # 对图像数据进行预处理
        img_data = self.preprocess(frame)
        # 使用预处理后的图像数据运行推理,outputs:(1,84,8400)  8400 = 80*80 + 40*40 + 20*20
        outputs = self.session.run(None, {model_inputs[0].name: img_data})
        # print(len(outputs))
        # 对输出进行后处理以获取输出图像
        return self.postprocess(frame, outputs)  # 输出图像
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="onnx_weights/yolov8n.onnx", help="ONNX模型路径")
    parser.add_argument("--video", type=str, default="2.mp4", help="视频文件路径或摄像头索引")
    parser.add_argument("--conf-thres", type=float, default=0.3, help="置信度阈值")
    parser.add_argument("--iou-thres", type=float, default=0.5, help="IoU阈值")
    args = parser.parse_args()
 
    # 创建YOLOv8实例
    detection = YOLOv8(args.model, args.conf_thres, args.iou_thres)
 
    # 使用 OpenCV 打开视频
    cap = cv2.VideoCapture(args.video)
 
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()
 
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        start_time = time.time()
        output_frame = detection.main(frame)  # 对视频帧进行推理
        end_time = time.time()
        # print(f"{(end_time - start_time)*1000} ms")
        fps = 1 / (end_time - start_time)
        cv2.putText(output_frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Output", output_frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
 
    cap.release()
    cv2.destroyAllWindows()