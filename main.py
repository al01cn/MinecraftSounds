import os
import sys
import ctypes
import winreg

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QFontDatabase

from gui.windows import App
from gui.ui.minecraft_style import init_minecraft_fonts
from utils.pydub_patch import apply_pydub_patch
from utils.main import exeSuffixName

def is_admin():
    """检查程序是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_as_admin():
    """以管理员权限重新启动程序"""
    script = sys.argv[0]
    params = ' '.join(sys.argv[1:])
    
    # 使用ShellExecute以管理员权限启动程序
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)

def check_file_association():
    """检查.mcsd文件关联是否有效"""
    try:
        # 检查文件类型关联是否存在
        try:
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, exeSuffixName) as key:
                file_type = winreg.QueryValue(key, "")
                if file_type != "MinecraftSounds.Project":
                    return False
        except FileNotFoundError:
            return False
        
        # 检查打开命令是否正确
        try:
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "MinecraftSounds.Project\\shell\\open\\command") as key:
                command = winreg.QueryValue(key, "")
                app_exe = sys.executable
                expected_command = f'"{app_exe}" "%1"'
                if command != expected_command:
                    return False
        except FileNotFoundError:
            return False
            
        return True
    except Exception as e:
        print(f"检查.mcsd文件关联失败: {str(e)}")
        return False

def associate_mcsd_file():
    """自动关联.mcsd文件，仅在关联失效时执行"""
    # 如果文件关联已经有效，则不需要重新关联
    if check_file_association():
        return True
        
    try:
        # 获取应用程序路径
        app_exe = sys.executable
        
        # 创建文件类型关联
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, exeSuffixName) as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "MinecraftSounds.Project")
        
        # 创建文件类型描述
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "MinecraftSounds.Project") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "Minecraft音乐包项目文件")
        
        # 创建图标关联
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "MinecraftSounds.Project\\DefaultIcon") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, f"{app_exe},0")
        
        # 创建打开命令
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "MinecraftSounds.Project\\shell\\open\\command") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, f'"{app_exe}" "%1"')
        
        # 通知系统文件关联已更改
        ctypes.windll.shell32.SHChangeNotify(0x08000000, 0, None, None)
        
        return True
    except Exception as e:
        print(f"自动关联.mcsd文件失败: {str(e)}")
        return False

# 预加载模块和资源的函数
def preload_resources():
    """预加载常用模块和资源，减少启动时的加载时间"""
    # 预先导入可能会在启动后才用到的模块
    import threading
    
    # 在后台线程中预加载字体
    def load_fonts_async():
        init_minecraft_fonts()
    
    # 在后台线程中应用pydub补丁
    def apply_patch_async():
        apply_pydub_patch()
    
    # 创建并启动字体加载线程
    font_thread = threading.Thread(target=load_fonts_async)
    font_thread.daemon = True
    font_thread.start()
    
    # 创建并启动补丁应用线程
    patch_thread = threading.Thread(target=apply_patch_async)
    patch_thread.daemon = True
    patch_thread.start()
    
    return font_thread, patch_thread

if __name__ == '__main__':
    # 检查是否以管理员权限运行，如果不是则重新启动
    if len(sys.argv) > 1 and sys.argv[1] == "--admin-required" and not is_admin():
        run_as_admin()
        sys.exit(0)
    
    # 设置高DPI支持
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # 创建应用程序实例
    app = QApplication(sys.argv)
    
    # 在后台线程中预加载资源
    font_thread, patch_thread = preload_resources()
    
    # 创建主窗口
    main = App()
    
    # 延迟处理文件关联，避免启动时阻塞
    def handle_file_association():
        try:
            # 尝试关联文件
            if not associate_mcsd_file() and not is_admin():
                # 如果关联失败且不是管理员权限，则以管理员权限重启
                if QMessageBox.question(None, "需要管理员权限", 
                                      "关联.mcsd文件需要管理员权限，是否以管理员权限重新启动程序？",
                                      QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                    # 添加标记参数，避免重复提示
                    if "--admin-required" not in sys.argv:
                        sys.argv.append("--admin-required")
                    run_as_admin()
                    sys.exit(0)
        except Exception as e:
            print(f"尝试关联文件时出错: {str(e)}")
    
    # 显示主窗口
    main.show()
    
    # 处理命令行参数，如果有文件路径参数，则打开该文件
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        file_path = sys.argv[1]
        # 检查文件后缀是否为.mcsd
        if file_path != "" and file_path.lower().endswith('.mcsd'):
            # 延迟一小段时间后打开文件，确保UI已完全加载
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(100, lambda: main.openProjectFile(file_path))
    
    # 在UI显示后延迟处理文件关联
    from PyQt5.QtCore import QTimer
    QTimer.singleShot(500, handle_file_association)
    
    # 等待预加载线程完成
    font_thread.join(0.1)  # 等待字体加载，但最多等待0.1秒
    patch_thread.join(0.1)  # 等待补丁应用，但最多等待0.1秒
    
    sys.exit(app.exec_())