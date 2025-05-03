#!/usr/bin/env python3
"""
dlFast - 交互式命令行下载工具
"""

import sys
import os
import traceback
from download import download_file
from config import DOWNLOAD_URLS

def main():
    """主程序入口"""
    try:
        print("dlFast 下载工具 (输入exit退出)")
        
        while True:
            try:
                command = input("> ").strip().lower()
                
                if command == "exit":
                    break
                    
                if not command.startswith("dl "):
                    print("无效命令格式，请使用'dl 命令'，如: dl wx.exe-win-x64")
                    continue
                    
                cmd = command[3:]  # 去掉'dl '前缀
                
                if cmd == "wx.exe-win-x64":
                    url = DOWNLOAD_URLS['x64']
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', 'WeChatSetup.exe')
                elif cmd == "wx.exe-win-x32":
                    url = DOWNLOAD_URLS['x32']
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', 'WeChatSetup_x86.exe')
                else:
                    print("无效命令，可用命令: dl wx.exe-win-x64, dl wx.exe-win-x32, exit")
                    continue
                    
                try:
                    download_file(url, output)
                    print("下载完成")
                except Exception as e:
                    print(f"下载失败: {str(e)}")
                    
            except EOFError:
                print("\n使用exit命令退出程序")
            except KeyboardInterrupt:
                print("\n使用exit命令退出程序")
            except Exception as e:
                print(f"发生错误: {str(e)}")
                traceback.print_exc()
                
    except Exception as e:
        print(f"程序启动失败: {str(e)}")
        traceback.print_exc()
        input("按Enter键退出...")

if __name__ == "__main__":
    main()
