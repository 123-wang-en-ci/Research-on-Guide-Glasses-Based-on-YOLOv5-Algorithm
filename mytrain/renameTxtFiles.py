import os

def rename_txt_files(directory):
    # 确保目录是存在的
    if not os.path.isdir(directory):
        print(f"指定的目录不存在: {directory}")
        return

    # 获取所有的txt文件
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    
    # 创建一个映射关系，从0401到0500映射到0301到0400
    rename_map = {}
    for i in range(701, 801):  # 0401 到 0500
        old_name = f"{i:04d}.txt"  # 原文件名
        new_name = f"{i - 100:04d}.txt"  # 新文件名，减去100
        rename_map[old_name] = new_name

    # 遍历文件并重命名
    for old_name, new_name in rename_map.items():
        old_path = os.path.join(directory, old_name)
        new_path = os.path.join(directory, new_name)

        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            print(f"已重命名: {old_path} -> {new_path}")
        else:
            print(f"文件不存在: {old_path}")

if __name__ == "__main__":
    # 指定要处理的文件夹路径
    folder_path = r'D:/YOLOv5/盲人检测数据集/labels - 副本/7  栅栏'  # 请替换为你的文件夹路径
    rename_txt_files(folder_path)
