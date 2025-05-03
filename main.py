#!/usr/bin/env python3
"""
dlFast - 交互式命令行下载工具
"""

import sys
import os
import traceback
from download import download_file
from config import DOWNLOAD_URLS

import logging
import os
from pathlib import Path

def setup_logging():
    """配置日志记录"""
    log_dir = Path(os.getenv('TEMP', '.')) / 'dlFast_logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'dlFast.log'
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def main():
    """主程序入口"""
    try:
        setup_logging()
        logging.info("="*50)
        logging.info("程序启动，开始初始化...")
        
        # 检查关键模块导入
        try:
            import requests
            import tqdm
            logging.info("关键模块导入成功")
        except ImportError as e:
            logging.error(f"模块导入失败: {str(e)}")
            raise
            
        logging.info("初始化完成，准备进入主循环")
        
        # 添加启动暂停
        if sys.platform == "win32":
            os.system("title dlFast 下载工具")
            
        print("dlFast 下载工具 (输入exit退出)")
        logging.info("程序界面已显示")
        
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
                elif cmd == "wx-input.exe-win":
                    url = DOWNLOAD_URLS['input']
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', 'WeChatInput.exe')
                elif cmd == "qq.exe-win-x32":
                    url = DOWNLOAD_URLS['qq_x32']
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', 'QQ_9.9.19_250429_x86_01.exe')
                elif cmd == "qq.exe-win-arm":
                    url = DOWNLOAD_URLS['qq_arm']
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', 'QQ_9.9.19_250429_arm64_01.exe')
                elif cmd == "qq.exe-win-old":
                    url = DOWNLOAD_URLS['qq_old']
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', 'QQ9.7.23.29406.exe')
                elif cmd == "everything_setup.exe-win-x86":
                    url = DOWNLOAD_URLS['everything_x86']
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', 'Everything-1.4.1.1026.x86-Setup.exe')
                elif cmd == "everything_setup.exe-win-x64":
                    url = DOWNLOAD_URLS['everything_x64']
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', 'Everything-1.4.1.1026.x64-Setup.exe')
                elif cmd == "everything_Lite_setup.exe-win-x86":
                    url = DOWNLOAD_URLS['everything_lite_x86']
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', 'Everything-1.4.1.1026.x86.Lite-Setup.exe')
                elif cmd == "everything_Lite_setup.exe-win-x64":
                    url = DOWNLOAD_URLS['everything_lite_x64']
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', 'Everything-1.4.1.1026.x64.Lite-Setup.exe')
                elif cmd == "everything_setup.msi-win-x86":
                    url = DOWNLOAD_URLS['everything_msi_x86']
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', 'Everything-1.4.1.1026.x86.msi')
                elif cmd == "everything_setup.msi-win-x64":
                    url = DOWNLOAD_URLS['everything_msi_x64']
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', 'Everything-1.4.1.1026.x64.msi')
                elif cmd == "everything_Lite_setup.msi-win-x86":
                    url = DOWNLOAD_URLS['everything_lite_msi_x86']
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', 'Everything-1.4.1.1026.x86.Lite.msi')
                elif cmd == "everything_Lite_setup.msi-win-x64":
                    url = DOWNLOAD_URLS['everything_lite_msi_x64']
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', 'Everything-1.4.1.1026.x64.Lite.msi')
                elif cmd == "pan.baidu.exe-win":
                    url = DOWNLOAD_URLS['baidu_netdisk']
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', 'BaiduNetdisk_7.55.1.101.exe')
                elif cmd == "kuake.pan.exe-win":
                    url = DOWNLOAD_URLS['quark_pan']
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', 'QuarkPC_V4.0.0.316.exe')
                elif cmd == "kuake.exe-win":
                    url = DOWNLOAD_URLS['quark_browser']
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', 'QuarkPC_V2.6.5.320.exe')
                elif cmd == "thunder.pan.exe-win":
                    url = DOWNLOAD_URLS['thunder']
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', 'XunLeiWebSetup12.1.6.2780gw.exe')
                elif cmd == "thunder.video.new.exe-win-x64":
                    url = DOWNLOAD_URLS['thunder_video_new']
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', 'XMPSetup7.0.3.92xmpgw.exe')
                elif cmd == "thunder.video.old.exe-win-x86":
                    url = DOWNLOAD_URLS['thunder_video_old']
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', 'XMPSetup6.2.6.622xmpgw.exe')
                else:
                    print("无效命令，可用命令: dl wx.exe-win-x64, dl wx.exe-win-x32, dl wx-input.exe-win, dl qq.exe-win-x32, dl qq.exe-win-arm, dl qq.exe-win-old, dl everything_setup.exe-win-x86, dl everything_setup.exe-win-x64, dl everything_Lite_setup.exe-win-x86, dl everything_Lite_setup.exe-win-x64, dl everything_setup.msi-win-x86, dl everything_setup.msi-win-x64, dl everything_Lite_setup.msi-win-x86, dl everything_Lite_setup.msi-win-x64, dl pan.baidu.exe-win, dl kuake.pan.exe-win, dl kuake.exe-win, dl thunder.pan.exe-win, dl thunder.video.new.exe-win-x64, dl thunder.video.old.exe-win-x86, exit")
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
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        if sys.platform == "win32":
            print("\n程序执行完毕，按任意键退出...")
            os.system("pause >nul")
