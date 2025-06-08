import os
import shutil

# 定义源文件夹和目标文件夹
images_source_folder = 'D:/YOLOv5/盲人检测数据集/images'  # 图片的源文件夹
labels_source_folder = 'D:/YOLOv5/盲人检测数据集/labels'  # 标签的源文件夹
train_images_folder = 'D:/YOLOv5/盲人检测数据集/images/train'  # 训练集图片文件夹
train_labels_folder = 'D:/YOLOv5/盲人检测数据集/labels/train'  # 训练集标签文件夹
val_images_folder = 'D:/YOLOv5/盲人检测数据集/images/val'      # 验证集图片文件夹
val_labels_folder = 'D:/YOLOv5/盲人检测数据集/labels/val'      # 验证集标签文件夹

# 创建目标文件夹（如果不存在）
os.makedirs(train_images_folder, exist_ok=True)
os.makedirs(train_labels_folder, exist_ok=True)
os.makedirs(val_images_folder, exist_ok=True)
os.makedirs(val_labels_folder, exist_ok=True)

# 遍历每个文件，根据文件名进行划分
for i in range(1, 1201):
    # 格式化文件名
    img_filename = f"{i:04d}.jpg"
    label_filename = f"{i:04d}.txt"
    
    # 确定当前文件的路径
    img_path = os.path.join(images_source_folder, img_filename)
    label_path = os.path.join(labels_source_folder, label_filename)
    
    # 确保文件存在
    if os.path.exists(img_path) and os.path.exists(label_path):
        # 计算当前文件在100个文件中的位置
        position_in_group = (i - 1) % 100
        
        # 进行划分
        if position_in_group < 80:  # 前80个放入train
            shutil.copy(img_path, train_images_folder)
            shutil.copy(label_path, train_labels_folder)
        else:  # 后20个放入val
            shutil.copy(img_path, val_images_folder)
            shutil.copy(label_path, val_labels_folder)
    else:
        print(f"Warning: {img_filename} or {label_filename} does not exist.")

print("数据集划分完成！")
