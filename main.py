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
        
        # 命令映射字典
        command_map = {
            "wx.exe-win-x64": ('x64', 'WeChatSetup.exe'),
            "wx.exe-win-x32": ('x32', 'WeChatSetup_x86.exe'),
            "wx-input.exe-win": ('input', 'WeChatInput.exe'),
            "qq.exe-win-x32": ('qq_x32', 'QQ_9.9.19_250429_x86_01.exe'),
            "qq.exe-win-arm": ('qq_arm', 'QQ_9.9.19_250429_arm64_01.exe'),
            "qq.exe-win-old": ('qq_old', 'QQ9.7.23.29406.exe'),
            "everything_setup.exe-win-x86": ('everything_x86', 'Everything-1.4.1.1026.x86-Setup.exe'),
            "everything_setup.exe-win-x64": ('everything_x64', 'Everything-1.4.1.1026.x64-Setup.exe'),
            "everything_Lite_setup.exe-win-x86": ('everything_lite_x86', 'Everything-1.4.1.1026.x86.Lite-Setup.exe'),
            "everything_Lite_setup.exe-win-x64": ('everything_lite_x64', 'Everything-1.4.1.1026.x64.Lite-Setup.exe'),
            "everything_setup.msi-win-x86": ('everything_msi_x86', 'Everything-1.4.1.1026.x86.msi'),
            "everything_setup.msi-win-x64": ('everything_msi_x64', 'Everything-1.4.1.1026.x64.msi'),
            "everything_Lite_setup.msi-win-x86": ('everything_lite_msi_x86', 'Everything-1.4.1.1026.x86.Lite.msi'),
            "everything_Lite_setup.msi-win-x64": ('everything_lite_msi_x64', 'Everything-1.4.1.1026.x64.Lite.msi'),
            "pan.baidu.exe-win": ('baidu_netdisk', 'BaiduNetdisk_7.55.1.101.exe'),
            "kuake.pan.exe-win": ('quark_pan', 'QuarkPC_V4.0.0.316.exe'),
            "kuake.exe-win": ('quark_browser', 'QuarkPC_V2.6.5.320.exe'),
            "thunder.pan.exe-win": ('thunder', 'XunLeiWebSetup12.1.6.2780gw.exe'),
            "thunder.video.new.exe-win-x64": ('thunder_video_new', 'XMPSetup7.0.3.92xmpgw.exe'),
            "thunder.video.old.exe-win-x86": ('thunder_video_old', 'XMPSetup6.2.6.622xmpgw.exe'),
            "ali.pan.exe-win": ('ali_pan', 'aDrive-6.8.6.exe'),
            "baidu.pan.enterprise.exe-win": ('baidu_pan_enterprise', 'BaiduNetdisk_7.55.1.101.exe'),
            "baidu.fanyi.exe-win": ('baidu_fanyi', '百度翻译_Setup_2.0.0.exe'),
            "baidu.input.exe-win": ('baidu_input', 'BaiduPinyinSetup_2.0.0.exe'),
            "baidu.input.f five.exe-win": ('baidu_input_five', 'BaiduWubiSetup_1.2.0.67.exe'),
            "360safe.exe-win": ('360safe', 'inst.exe'),
            "360safe.fast.exe-win": ('360safe_fast', 'setupbeta_jisu.exe'),
            "360.shadu.exe-win": ('360_shadu', '360sd_x64_std_7.0.0.1060C.exe'),
            "360.docprot.exe-win": ('360_docprot', 'dpsetup.exe'),
            "360se.exe-win": ('360_se', '360se_setup.exe'),
            "360pic.exe-win": ('360_pic', 'pic360Setup.exe'),
            "360zip.exe-win": ('360_zip', '360zip_setup.exe'),
            "360DrvMgrInstaller.exe-win": ('360_drvmgr', '360DrvMgrInstaller_beta.exe'),
            "360DesktopLite.exe-win": ('360_desktop_lite', '360DesktopLite_zm000001.exe'),
            "360suda.exe-win": ('360_suda', 'SudaSetup.exe'),
            "360game.exe-win": ('360_game', '360game_setup.exe'),
            "360safebox.exe-win": ('360_safebox', 'Safebox_setup_6.0.0.1090.exe'),
            "360suda.caplayer.exe-win": ('360_suda_caplayer', 'SudaCaplayerSetup_360gw.exe'),
            "360c0mpkill.exe-win": ('360_compkill', '360c0mpkill_5.1.64.1284-0423.zip'),
            "360DiskPart.exe-win": ('360_diskpart', 'DiskPartSetup_360gwxz.exe'),
            "360CleanPro.exe-win": ('360_cleanpro', 'SysCleanProSetup_swzs.exe'),
            "360yun.exe-win": ('360_yun', '360eyun_setup_4.0.1.1370.exe'),
            "QuickMediaEditor.exe-win": ('360_quickmedia', 'QuickMediaEditor_domain.exe'),
            "360hb.exe-win": ('360_hb', '360hb4.0.414.0__1003__.exe'),
            "7-zip.exe-win-x64": ('7-zip_x64', '7-zip_setup_x64.exe'),
            "7-zip.exe-win-x86": ('7-zip_x86', '7-zip_setup_x86.exe'),
            "7-zip.exe-win-arm64": ('7-zip_arm64', '7z2409_arm64.exe'),
            "geek.exe.zip-win": ('geek_zip', 'geek.zip'),
            "geek.exe.7z-win": ('geek_7z', 'geek.7z'),
        }
        
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
                
                # 处理帮助命令
                if cmd == "-h" or cmd == "--help":
                    print("\n可用下载命令:")
                    
                    # 自动从command_map生成分类帮助
                    categories = {}
                    for cmd_name in command_map.keys():
                        # 从命令名提取软件名作为分类
                        software = cmd_name.split('.')[0]
                        if software not in categories:
                            categories[software] = []
                        categories[software].append(cmd_name)
                    
                    # 显示分类命令
                    for software, cmds in categories.items():
                        print(f"\n{software}相关:")
                        for cmd_name in cmds:
                            print(f"  dl {cmd_name}")
                    
                    print("\n输入'exit'退出程序")
                    continue
                


                if cmd in command_map:
                    url_key, filename = command_map[cmd]
                    url = DOWNLOAD_URLS[url_key]
                    output = os.path.join(os.path.expanduser('~'), 'Downloads', filename)
                else:
                    available_commands = ", ".join(f"dl {cmd}" for cmd in command_map.keys())
                    print(f"无效命令，可用命令: {available_commands}, exit")
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
