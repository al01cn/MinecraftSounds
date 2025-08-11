import os
import sys
import ctypes

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

from gui.windows import App
from gui.ui.minecraft_style import init_minecraft_fonts

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

if __name__ == '__main__':
    # 检查是否以管理员权限运行，如果不是则重新启动
    if not is_admin():
        run_as_admin()
        sys.exit(0)
    
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    
    # 初始化Minecraft字体
    init_minecraft_fonts()
    
    # w = StickerFactoryApp()  # 直接创建类的实例
    # w.show()
    main = App()
    main.show()
    sys.exit(app.exec_())