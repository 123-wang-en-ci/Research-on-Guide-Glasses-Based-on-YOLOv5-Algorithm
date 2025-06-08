import os

def rename_and_modify_txt_files(folder_path):
    # 获取文件夹中所有的txt文件
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    # 初始化计数器
    counter = 801

    for file_name in txt_files:
        # 构造原文件的完整路径
        old_file_path = os.path.join(folder_path, file_name)
        
        # 读取文件内容
        with open(old_file_path, 'r') as file:
            lines = file.readlines()
        
        # 修改每一行的第一个数字（或单词）为4
        modified_lines = []
        for line in lines:
            parts = line.strip().split()  # 先strip去掉行尾的换行符，再split成单词列表
            if parts:  # 确保parts不是空列表
                parts[0] = '8'  
            modified_line = ' '.join(parts) + '\n'  # 重新组合成一行，并添加换行符
            modified_lines.append(modified_line)
        
        # 构造新文件名和路径
        new_file_name = f'{counter:04d}.txt'
        new_file_path = os.path.join(folder_path, new_file_name)
        
        # 写入修改后的内容到新文件
        with open(new_file_path, 'w') as file:
            file.writelines(modified_lines)
        
        # 删除原文件
        os.remove(old_file_path)
        
        # 更新计数器
        counter += 1

# 示例使用
folder_path = 'D:/YOLOv5/Bus.v1i.yolov5pytorch/Bus.v1i.yolov5pytorch/train/labels'  # 替换为你的文件夹路径
rename_and_modify_txt_files(folder_path)