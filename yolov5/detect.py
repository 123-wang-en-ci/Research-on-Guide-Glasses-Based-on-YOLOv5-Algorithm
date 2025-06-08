import torch
import sys
import utils
sys.path.append(r"./yolov5-6.1")
from models.common import DetectMultiBackend
from utils.datasets import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import (LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
from utils.torch_utils import select_device, time_sync
 
 
class predict:
    def __init__(self):
        self.weights = "./best.pt"  # model.pt path(s)
        self.data = "./yolov5-6.1/Clean_data/my_coco128.yaml"  # dataset.yaml path
        self.imgsz = (640, 640)  # inference size (height, width)
        self.conf_thres = 0.5  # confidence threshold
        self.iou_thres = 0.45  # NMS IOU threshold
        self.max_det = 1000  # maximum detections per image
        self.classes = None # filter by class: --class 0, or --class 0 2 3
        self.agnostic_nms = False  # class-agnostic NMS
        self.augment = False  # augmented inference
        self.visualize = False  # visualize features
        self.half = False
        self.dnn = True  # use OpenCV DNN for ONNX inference
 
        # Load model
        self.device = select_device('cpu')
        self.model = DetectMultiBackend(self.weights, device=self.device, dnn=self.dnn, data=self.data)
        self.stride, self.names, self.pt, self.jit, self.onnx, self.engine = self.model.stride, self.model.names, self.model.pt, self.model.jit, self.model.onnx, self.model.engine
        self.imgsz = check_img_size(self.imgsz, s=self.stride)  # check image size
        # Half
        self.half = False  # FP16 supported on limited backends with CUDA
 
 
    def detect_image(self, image_path):
        det_list = []
        # Dataloader
        dataset = LoadImages(image_path, img_size=self.imgsz, stride=self.stride, auto=self.pt)
        # Run inference
        for path, im, im0s, vid_cap, s in dataset:
            im0 = im0s.copy()
            im = torch.from_numpy(im).to(self.device)
            im = im.float()  # uint8 to fp16/32
            im /= 255  # 0 - 255 to 0.0 - 1.0
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim
           # Inference
            pred = self.model(im, augment=self.augment, visualize=self.visualize)
            # NMS
            pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, self.classes, self.agnostic_nms, max_det=self.max_det)
            # Process predictions
            for i, det in enumerate(pred):  # per image
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()
                # 转换为[[ymin, xmin, ymax, xmax, conf, class_pred],[ymin, xmin, ymax, xmax, conf, class_pred]]
                det_list = [[box[1].item(), box[0].item(),
                             box[3].item(), box[2].item(), box[4].item()
                                , int(box[5].item())] for box in det]
        return det_list