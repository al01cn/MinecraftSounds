import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from gui.components.ffmpeg_status import FFmpegStatusWidget
from utils.main import check_ffmpeg

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FFmpeg状态测试")
        self.setGeometry(100, 100, 400, 100)
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 添加FFmpeg状态组件
        self.ffmpeg_status = FFmpegStatusWidget()
        self.ffmpeg_status.ffmpeg_downloaded.connect(self.on_ffmpeg_downloaded)
        layout.addWidget(self.ffmpeg_status)
        
        # 打印当前FFmpeg状态
        exists, path = check_ffmpeg()
        print(f"FFmpeg状态: {'存在' if exists else '不存在'}")
        if exists:
            print(f"FFmpeg路径: {path}")
    
    def on_ffmpeg_downloaded(self, success):
        print(f"FFmpeg下载{'成功' if success else '失败'}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())