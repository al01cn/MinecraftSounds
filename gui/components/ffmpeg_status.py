from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QColor, QPainter, QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QMessageBox
from utils.main import check_ffmpeg, download_ffmpeg
import os

class FFmpegStatusWidget(QWidget):
    """FFmpeg状态指示器和下载按钮组件"""
    
    # 定义信号
    ffmpeg_downloaded = pyqtSignal(bool)  # 下载完成信号，参数为是否成功
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
        # 初始状态设置为未知（灰色）
        self._createIndicator("#808080")  # 灰色
        self.statusLabel.setToolTip("正在检查FFmpeg状态...")
        
        # 使用QTimer延迟检查FFmpeg，避免阻塞UI
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(500, self.checkFFmpeg)  # 500毫秒后检查FFmpeg
    
    def initUI(self):
        # 创建水平布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(3)
        
        # 创建状态标签 - 使用更小的字体
        self.statusLabel = QLabel("FFmpeg:")
        self.statusLabel.setStyleSheet("color: white; font-size: 9px; background-color: transparent;")
        
        # 创建状态指示器 - 更小的指示器
        self.statusIndicator = QLabel()
        self.statusIndicator.setFixedSize(10, 10)
        
        # 创建下载按钮 - 更小的按钮
        self.downloadButton = QPushButton("下载")
        self.downloadButton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: 1px solid #388E3C;
                border-radius: 3px;
                padding: 2px 5px;
                font-size: 9px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
            QPushButton:pressed {
                background-color: #2E7D32;
            }
        """)
        self.downloadButton.clicked.connect(self.onDownloadClicked)
        self.downloadButton.hide()  # 默认隐藏
        
        # 添加组件到布局
        layout.addWidget(self.statusLabel)
        layout.addWidget(self.statusIndicator)
        layout.addWidget(self.downloadButton)
        
        # 设置布局
        self.setLayout(layout)
        
        # 设置组件的固定大小
        self.setFixedHeight(20)
        self.setMaximumWidth(120)
    
    def checkFFmpeg(self):
        """检查FFmpeg是否存在并更新UI"""
        # 使用线程执行FFmpeg检查，避免阻塞UI
        import threading
        
        def check_ffmpeg_thread():
            # 在线程中执行FFmpeg检查
            ffmpeg_exists, ffmpeg_path = check_ffmpeg()
            
            # 使用Qt的信号槽机制在主线程中更新UI
            from PyQt5.QtCore import QMetaObject, Qt, Q_ARG
            
            if ffmpeg_exists:
                # 在主线程中更新UI为绿色指示器
                QMetaObject.invokeMethod(self, "_updateFFmpegStatus",
                                        Qt.QueuedConnection,
                                        Q_ARG(bool, True),
                                        Q_ARG(str, ffmpeg_path))
            else:
                # 在主线程中更新UI为红色指示器
                QMetaObject.invokeMethod(self, "_updateFFmpegStatus",
                                        Qt.QueuedConnection,
                                        Q_ARG(bool, False),
                                        Q_ARG(str, ""))
        
        # 创建并启动线程
        thread = threading.Thread(target=check_ffmpeg_thread)
        thread.daemon = True
        thread.start()
    
    from PyQt5.QtCore import pyqtSlot, QMetaObject, Qt, Q_ARG
    
    @pyqtSlot(bool, str)
    def _updateFFmpegStatus(self, exists, path):
        """在主线程中更新FFmpeg状态UI"""
        if exists:
            # 创建绿色圆形指示器
            self._createIndicator("#4CAF50")  # 绿色
            self.downloadButton.hide()
            self.statusLabel.setToolTip(f"FFmpeg已安装: {path}")
        else:
            # 创建红色圆形指示器
            self._createIndicator("#F44336")  # 红色
            self.downloadButton.show()
            self.statusLabel.setToolTip("未检测到FFmpeg，请点击下载按钮安装")
    
    def _createIndicator(self, color):
        """创建圆形状态指示器"""
        size = 10  # 更小的尺寸
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, size, size)
        painter.end()
        
        self.statusIndicator.setPixmap(pixmap)
    
    def onDownloadClicked(self):
        """下载按钮点击事件"""
        # 禁用按钮，防止重复点击
        self.downloadButton.setEnabled(False)
        self.downloadButton.setText("正在下载...")
        
        # 显示下载进度对话框
        QMessageBox.information(self, "下载FFmpeg", "FFmpeg将在后台下载并安装，请稍候...")
        
        # 执行下载
        success = download_ffmpeg()
        
        # 更新UI
        if success:
            QMessageBox.information(self, "下载成功", "FFmpeg已成功下载并安装!")
            self.checkFFmpeg()  # 重新检查状态
        else:
            QMessageBox.warning(self, "下载失败", "FFmpeg下载失败，请检查网络连接或手动下载。")
            self.downloadButton.setEnabled(True)
            self.downloadButton.setText("重试下载")
        
        # 发送下载完成信号
        self.ffmpeg_downloaded.emit(success)