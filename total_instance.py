import os

def count_lines_in_txt_files_by_batch(folder_path, batch_size=100):
    current_batch_lines = 0  # 当前批次的行数
    file_count = 0  # 已处理文件数量

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 判断是否为txt文件
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r') as f:
                    # 读取文件并计算行数
                    lines = f.readlines()
                    current_batch_lines += len(lines)  # 累加当前批次的行数
                    file_count += 1  # 累加文件数

                    # 每处理 batch_size 个文件时输出一次当前批次的行数统计
                    if file_count % batch_size == 0:
                        print(f"已处理 {file_count} 个文件，本批次的行数总和为: {current_batch_lines}")
                        current_batch_lines = 0  # 重置当前批次行数

            except Exception as e:
                print(f"无法读取文件 {filename}: {e}")
    
    # 如果最后一批文件没有达到 batch_size，输出它们的行数
    if current_batch_lines > 0:
        print(f"最后一批文件的行数总和为: {current_batch_lines}")

# 设置文件夹路径
folder_path = r"D:\YOLOv5\盲人检测数据集备份\盲人检测数据集\labels"  # 请替换为你的文件夹路径

# 计算并输出每 100 个文件的总行数
count_lines_in_txt_files_by_batch(folder_path, batch_size=100)
