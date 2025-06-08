import random
import os
import glob
from PIL import Image

def convert_and_rename_images(folder_path):
    # 获取指定文件夹中的所有图片文件
    # 这里使用 glob 获取所有常见的图片格式
    image_files = glob.glob(os.path.join(folder_path, '*.*'))
    
    # 设定重命名的起始编号
    start_index = 1101
    
    for i, image_file in enumerate(image_files):
        # 确保文件是图片格式
        try:
            img = Image.open(image_file)
            # 构造新的文件名
            new_index = start_index + i
            new_filename = f"{new_index:04}.jpg"
            new_file_path = os.path.join(folder_path, new_filename)
            
            # 将图片保存为 JPG 格式
            img.convert('RGB').save(new_file_path, 'JPEG')
            #print(f"Converted and renamed: {image_file} to {new_file_path}")
            
            # 删除原文件
            os.remove(image_file)

        except Exception as e:
            print(f"Error processing {image_file}: {e}")

# 使用示例
folder_path = 'D:/YOLOv5/自行车'  # 替换为你的文件夹路径
convert_and_rename_images(folder_path)
