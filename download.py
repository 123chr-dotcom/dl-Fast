#!/usr/bin/env python3
"""
文件下载模块
"""

import requests
from tqdm import tqdm
import os

def download_file(url, output_path):
    """
    下载文件并显示进度条
    
    参数:
        url (str): 下载URL
        output_path (str): 保存路径
        
    异常:
        requests.exceptions.RequestException: 下载失败时抛出
    """
    try:
        # 发起HTTP GET请求，开启流式下载
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # 获取文件总大小
        total_size = int(response.headers.get('content-length', 0))
        
        # 创建进度条
        progress_bar = tqdm(
            total=total_size,
            unit='B',
            unit_scale=True,
            desc=f"下载 {os.path.basename(output_path)}"
        )
        
        # 写入文件
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # 过滤掉保持连接的新块
                    f.write(chunk)
                    progress_bar.update(len(chunk))
        
        progress_bar.close()
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"下载失败: {str(e)}")
