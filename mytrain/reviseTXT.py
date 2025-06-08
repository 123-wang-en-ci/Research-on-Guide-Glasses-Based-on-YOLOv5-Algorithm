import os

def modify_first_column_in_txt_files(folder_path, modifier_function):
    # 遍历指定文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            new_lines = []

            # 读取文件
            with open(file_path, 'r') as file:
                for line in file:
                    # 分割行，修改第一列
                    parts = line.split()
                    if len(parts) > 0:
                        # 假设我们简单地加1作为示例修改
                        parts[0] = '8'# ----------------------->
                    new_lines.append(' '.join(parts))

            # 将修改后的内容写回文件
            with open(file_path, 'w') as file:
                for new_line in new_lines:
                    file.write(new_line + '\n')

def example_modifier(value):
    # 示例修改函数：将第一列的值加1
    return value + 1

if __name__ == "__main__":
    folder_path = 'D:/YOLOv5/8-11/8-11/9公交站'  # 请替换为您的文件夹路径
    modify_first_column_in_txt_files(folder_path, example_modifier)
