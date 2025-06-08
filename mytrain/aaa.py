
import requests

def download_file(url, destination):
    """
    下载文件的函数。
    
    :param url: 文件的URL
    :param destination: 文件保存的本地路径
    """
    try:
        # 发起GET请求
        response = requests.get(url, stream=True)
        
        # 检查请求是否成功
        if response.status_code == 200:
            # 打开文件以写入二进制模式
            with open(destination, 'wb') as file:
                # 循环写入数据
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"文件已下载到：{destination}")
        else:
            print(f"下载失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"下载过程中出现错误：{e}")

# 使用示例
url = 'https://a530943-bf87-f60ed9eb.nmb1.seetacloud.com:8443/jupyter/lab/tree/yolov5-master/runs.tar.gz'  # 替换为你要下载的文件的URL
destination = 'runs.tar.gz'  # 替换为你想保存文件的本地路径

download_file(url, destination)