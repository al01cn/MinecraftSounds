from PyQt5.QtCore import Qt, QSize, QUrl, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QPixmap
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QListWidget, QListWidgetItem, QFileDialog, QMessageBox)
import os

from gui.ui import MinecraftFrame, MinecraftTitleLabel, MinecraftLabel, MinecraftBackground, apply_minecraft_style
from gui.ui.button import MinecraftPixelButton
from gui.ui.minecraft_dialog import MinecraftMessageBox, MinecraftMessageBoxResult

class AudioDropZone(MinecraftFrame):
    """音频文件拖放区域"""
    fileDropped = pyqtSignal(list)  # 文件拖放信号，传递文件路径列表
    
    def __init__(self, parent=None):
        super().__init__(parent, frame_type="stone")
        self.setAcceptDrops(True)
        self.setMinimumHeight(150)
        
        # 创建布局
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignCenter)
        
        # 创建提示标签
        self.iconLabel = QLabel()
        self.iconLabel.setPixmap(QPixmap("app/assets/icons/music_note.svg").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.iconLabel.setAlignment(Qt.AlignCenter)
        
        self.textLabel = MinecraftLabel("拖放音频文件到这里或点击选择文件（支持多选）")
        self.textLabel.setAlignment(Qt.AlignCenter)
        
        # 创建选择文件按钮
        self.selectButton = MinecraftPixelButton("选择文件", button_type="brown")
        self.selectButton.clicked.connect(self.selectFile)
        
        # 添加组件到布局
        self.layout.addWidget(self.iconLabel)
        self.layout.addWidget(self.textLabel)
        self.layout.addWidget(self.selectButton, 0, Qt.AlignCenter)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """拖拽进入事件"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """拖拽放下事件"""
        if event.mimeData().hasUrls():
            valid_files = []
            invalid_files = []
            
            # 处理所有拖放的文件
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                # 检查是否为音频文件
                if self.isAudioFile(file_path):
                    valid_files.append(file_path)
                else:
                    invalid_files.append(os.path.basename(file_path))
            
            # 如果有有效文件，发送信号
            if valid_files:
                self.fileDropped.emit(valid_files)
            
            # 如果有无效文件，显示警告
            if invalid_files:
                MinecraftMessageBox.show_warning(
                    self,
                    "文件类型错误",
                    f"以下文件不是有效的音频文件 (.ogg, .wav, .mp3):\n{', '.join(invalid_files)}"
                )
    
    def selectFile(self):
        """选择文件按钮点击事件"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "选择音频文件", "", "音频文件 (*.ogg *.wav *.mp3)"
        )
        if file_paths:
            self.fileDropped.emit(file_paths)
    
    def isAudioFile(self, file_path):
        """检查是否为音频文件"""
        valid_extensions = [".ogg", ".wav", ".mp3"]
        _, ext = os.path.splitext(file_path)
        return ext.lower() in valid_extensions

class AudioListItem(QWidget):
    """音频列表项"""
    deleteRequested = pyqtSignal(str)  # 删除请求信号
    
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        
        # 创建布局
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(10)
        
        # 文件名标签
        self.nameLabel = MinecraftLabel(os.path.basename(file_path))
        
        # 删除按钮
        self.deleteButton = MinecraftPixelButton("删除", button_type="red")
        self.deleteButton.setFixedSize(60, 30)
        self.deleteButton.clicked.connect(self.onDelete)
        
        # 添加组件到布局
        self.layout.addWidget(self.nameLabel)
        self.layout.addWidget(self.deleteButton)
    
    def onDelete(self):
        """删除按钮点击事件"""
        self.deleteRequested.emit(self.file_path)

class EditorWindow(QWidget):
    """音乐包编辑器窗口"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initWindow()
        
        # 应用我的世界风格
        apply_minecraft_style(self)
        
        # 创建主布局
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(20)
        
        # 创建标题
        self.titleLabel = MinecraftTitleLabel("音乐包编辑器")
        self.mainLayout.addWidget(self.titleLabel, 0, Qt.AlignCenter)
        
        # 创建顶部按钮区域
        self.topButtonLayout = QHBoxLayout()
        self.topButtonLayout.setContentsMargins(0, 0, 0, 0)
        self.topButtonLayout.setSpacing(20)
        
        # 创建重构和导出按钮
        self.rebuildButton = MinecraftPixelButton("重构", button_type="green")
        self.rebuildButton.setMinimumSize(120, 40)
        self.rebuildButton.clicked.connect(self.onRebuild)
        
        self.exportButton = MinecraftPixelButton("导出", button_type="blue")
        self.exportButton.setMinimumSize(120, 40)
        self.exportButton.clicked.connect(self.onExport)
        
        # 添加按钮到顶部布局
        self.topButtonLayout.addWidget(self.rebuildButton)
        self.topButtonLayout.addWidget(self.exportButton)
        self.topButtonLayout.addStretch(1)
        
        # 添加顶部按钮布局到主布局
        self.mainLayout.addLayout(self.topButtonLayout)
        
        # 创建音频拖放区域
        self.dropZone = AudioDropZone(self)
        self.dropZone.fileDropped.connect(self.onFileDropped)
        self.mainLayout.addWidget(self.dropZone)
        
        # 创建音频列表区域
        self.listFrame = MinecraftFrame(frame_type="stone")
        self.listLayout = QVBoxLayout(self.listFrame)
        self.listLayout.setContentsMargins(10, 10, 10, 10)
        self.listLayout.setSpacing(5)
        
        # 创建列表标题
        self.listTitleLabel = MinecraftLabel("已添加的音频文件")
        self.listLayout.addWidget(self.listTitleLabel)
        
        # 创建音频列表
        self.audioList = QListWidget()
        self.audioList.setStyleSheet("""
            QListWidget {
                background-color: #373737;
                border: 2px solid #1F1F1F;
                color: #FFFFFF;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #1F1F1F;
            }
            QListWidget::item:selected {
                background-color: #4A4A4A;
            }
        """)
        self.listLayout.addWidget(self.audioList)
        
        # 添加列表框架到主布局
        self.mainLayout.addWidget(self.listFrame)
        
        # 初始化音频文件列表
        self.audioFiles = []
    
    def initWindow(self):
        """初始化窗口"""
        # 设置窗口尺寸（与主窗口相同）
        self.resize(900, 700)
        self.setMinimumSize(800, 600)
        self.setWindowTitle('音乐包编辑器')
        
        # 设置窗口样式
        self.setStyleSheet("""
            QWidget {
                background-color: #373737;
            }
        """)
    
    def onFileDropped(self, file_paths):
        """文件拖放事件处理"""
        # 处理多个文件
        added_count = 0
        duplicate_files = []
        
        for file_path in file_paths:
            # 检查文件是否已存在
            if file_path in self.audioFiles:
                duplicate_files.append(os.path.basename(file_path))
                continue
            
            # 添加文件到列表
            self.audioFiles.append(file_path)
            added_count += 1
            
            # 创建列表项
            item = QListWidgetItem()
            self.audioList.addItem(item)
            
            # 创建自定义小部件
            widget = AudioListItem(file_path)
            widget.deleteRequested.connect(self.onDeleteAudio)
            
            # 设置列表项大小和小部件
            item.setSizeHint(widget.sizeHint())
            self.audioList.setItemWidget(item, widget)
        
        # 显示添加结果
        if added_count > 0:
            MinecraftMessageBox.show_message(
                self,
                "添加成功",
                f"成功添加了 {added_count} 个音频文件"
            )
        
        # 如果有重复文件，显示警告
        if duplicate_files:
            MinecraftMessageBox.show_warning(
                self,
                "文件已存在",
                f"以下文件已经添加过了:\n{', '.join(duplicate_files)}"
            )
    
    def onDeleteAudio(self, file_path):
        """删除音频文件"""
        # 从列表中移除文件
        if file_path in self.audioFiles:
            index = self.audioFiles.index(file_path)
            self.audioFiles.remove(file_path)
            self.audioList.takeItem(index)
    
    def onRebuild(self):
        """重构按钮点击事件"""
        if not self.audioFiles:
            MinecraftMessageBox.show_warning(
                self,
                "无法重构",
                "请先添加音频文件"
            )
            return
        
        # 这里添加重构逻辑
        MinecraftMessageBox.show_message(
            self,
            "重构成功",
            f"已成功重构 {len(self.audioFiles)} 个音频文件"
        )
    
    def onExport(self):
        """导出按钮点击事件"""
        if not self.audioFiles:
            MinecraftMessageBox.show_warning(
                self,
                "无法导出",
                "请先添加音频文件"
            )
            return
        
        # 选择导出目录
        export_dir = QFileDialog.getExistingDirectory(
            self, "选择导出目录", ""
        )
        
        if export_dir:
            # 这里添加导出逻辑
            MinecraftMessageBox.show_message(
                self,
                "导出成功",
                f"已成功导出到 {export_dir}"
            )