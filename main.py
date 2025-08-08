import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from gui.windows import App

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    # w = StickerFactoryApp()  # 直接创建类的实例
    # w.show()
    main = App()
    main.show()
    sys.exit(app.exec_())