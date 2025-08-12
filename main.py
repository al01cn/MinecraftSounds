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

def associate_mcsd_file():
    """自动关联.mcsd文件"""
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

if __name__ == '__main__':
    # 检查是否以管理员权限运行，如果不是则重新启动
    if len(sys.argv) > 1 and sys.argv[1] == "--admin-required" and not is_admin():
        run_as_admin()
        sys.exit(0)
    
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    
    # 初始化Minecraft字体
    init_minecraft_fonts()
    
    # 应用pydub补丁，防止ffmpeg弹出控制台窗口
    apply_pydub_patch()
    
    # 自动关联.mcsd文件
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
    
    # 创建主窗口
    main = App()
    
    # 处理命令行参数，如果有文件路径参数，则打开该文件
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        file_path = sys.argv[1]
        # 检查文件后缀是否为.mcsd
        if file_path != "" and file_path.lower().endswith('.mcsd'):
            # 延迟一小段时间后打开文件，确保UI已完全加载
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(100, lambda: main.openProjectFile(file_path))

        main.show()
        

    else:
        # 正常显示主窗口
        main.show()
    
    sys.exit(app.exec_())