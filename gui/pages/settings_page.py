from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame, QFileDialog, QLineEdit
import os
import sys
import winreg
import ctypes

from gui.ui import MinecraftFrame, MinecraftTitleLabel, MinecraftLabel, apply_minecraft_style
from gui.ui.button import MinecraftPixelButton
from utils.main import ffmpeg_path, app_path, exeSuffixName

class SettingsPage(QWidget):
    """设置页面"""
    # 返回主页信号
    backToMainPage = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 应用我的世界风格
        apply_minecraft_style(self)
        
        # 创建主布局
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(20)
        
        # 创建顶部按钮区域
        self.topButtonLayout = QHBoxLayout()
        self.topButtonLayout.setContentsMargins(0, 0, 0, 0)
        self.topButtonLayout.setSpacing(20)
        
        # 创建返回按钮
        self.backButton = MinecraftPixelButton("返回主页", button_type="brown")
        self.backButton.setMinimumSize(120, 40)
        self.backButton.clicked.connect(self.onBack)
        
        # 添加按钮到顶部布局
        self.topButtonLayout.addWidget(self.backButton)
        self.topButtonLayout.addStretch(1)
        
        # 添加顶部按钮布局到主布局
        self.mainLayout.addLayout(self.topButtonLayout)
        
        # 创建设置内容区域
        self.settingsFrame = MinecraftFrame(frame_type="stone")
        self.settingsLayout = QVBoxLayout(self.settingsFrame)
        self.settingsLayout.setContentsMargins(15, 15, 15, 15)
        self.settingsLayout.setSpacing(10)
        
        # 创建设置标题
        self.settingsTitle = MinecraftTitleLabel("设置")
        self.settingsTitle.setAlignment(Qt.AlignCenter)
        self.settingsLayout.addWidget(self.settingsTitle)
        
        # 创建设置内容滚动区域
        self.settingsScrollArea = QScrollArea()
        self.settingsScrollArea.setWidgetResizable(True)
        self.settingsScrollArea.setFrameShape(QFrame.NoFrame)
        
        # 创建设置内容容器
        self.settingsContainer = QWidget()
        self.settingsContainerLayout = QVBoxLayout(self.settingsContainer)
        self.settingsContainerLayout.setContentsMargins(0, 0, 0, 0)
        self.settingsContainerLayout.setSpacing(15)
        self.settingsContainerLayout.setAlignment(Qt.AlignTop)
        
        # 添加设置项
        self.addSettingItems()
        
        # 设置滚动区域的小部件
        self.settingsScrollArea.setWidget(self.settingsContainer)
        
        # 添加滚动区域到设置布局
        self.settingsLayout.addWidget(self.settingsScrollArea)
        
        # 添加设置框架到主布局
        self.mainLayout.addWidget(self.settingsFrame)
    
    def addSettingItems(self):
        """添加设置项"""
        # 添加FFmpeg路径设置
        self.addFFmpegPathSetting()
        
        # 文件关联设置已移除，现在在应用启动时自动关联
    
    def addFFmpegPathSetting(self):
        """添加FFmpeg路径设置"""
        # 创建FFmpeg路径设置容器
        ffmpegContainer = QWidget()
        ffmpegLayout = QVBoxLayout(ffmpegContainer)
        ffmpegLayout.setContentsMargins(0, 0, 0, 0)
        ffmpegLayout.setSpacing(5)
        
        # 添加标题
        ffmpegTitle = MinecraftLabel("FFmpeg路径设置")
        ffmpegTitle.setStyleSheet("font-weight: bold;")
        ffmpegLayout.addWidget(ffmpegTitle)
        
        # 创建路径输入区域
        pathContainer = QWidget()
        pathLayout = QHBoxLayout(pathContainer)
        pathLayout.setContentsMargins(0, 0, 0, 0)
        pathLayout.setSpacing(5)
        
        # 创建路径输入框
        self.ffmpegPathInput = QLineEdit()
        self.ffmpegPathInput.setStyleSheet("""
            QLineEdit {
                background-color: #373737;
                color: #FFFFFF;
                border: 2px solid #1F1F1F;
                border-radius: 2px;
                padding: 4px;
                font-family: 'Courier New';
            }
            QLineEdit:focus {
                border: 2px solid #5A5A5A;
            }
        """)
        
        # 设置默认路径
        default_ffmpeg_dir = os.path.join(app_path, 'ffmpeg')
        default_ffmpeg_path = os.path.join(default_ffmpeg_dir, 'ffmpeg.exe')
        
        # 检查当前ffmpeg路径
        if os.path.exists(ffmpeg_path):
            self.ffmpegPathInput.setText(os.path.dirname(ffmpeg_path))
        else:
            self.ffmpegPathInput.setText(default_ffmpeg_dir)
        
        # 创建浏览按钮
        browseButton = MinecraftPixelButton("浏览", button_type="gray")
        browseButton.setMinimumSize(60, 30)
        browseButton.clicked.connect(self.onBrowseFFmpegPath)
        
        # 创建重置按钮
        resetButton = MinecraftPixelButton("重置", button_type="gray")
        resetButton.setMinimumSize(60, 30)
        resetButton.clicked.connect(self.onResetFFmpegPath)
        
        # 创建帮助按钮
        helpButton = MinecraftPixelButton("帮助", button_type="blue")
        helpButton.setMinimumSize(60, 30)
        helpButton.clicked.connect(self.onFFmpegHelp)
        
        # 添加组件到路径布局
        pathLayout.addWidget(self.ffmpegPathInput, 1)  # 1表示拉伸因子
        pathLayout.addWidget(browseButton)
        pathLayout.addWidget(resetButton)
        pathLayout.addWidget(helpButton)
        
        # 添加路径容器到FFmpeg布局
        ffmpegLayout.addWidget(pathContainer)
        
        # 添加说明文本
        helpText = MinecraftLabel("注意：修改路径后需要重启应用才能生效。默认路径为app/ffmpeg目录。如果没有检测到FFmpeg，请自行下载并设置路径。")
        helpText.setStyleSheet("color: #AAAAAA; font-size: 9pt;")
        helpText.setWordWrap(True)
        ffmpegLayout.addWidget(helpText)
        
        # 添加FFmpeg容器到设置布局
        self.settingsContainerLayout.addWidget(ffmpegContainer)
        
        # 添加分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #555555;")
        separator.setMaximumHeight(1)
        self.settingsContainerLayout.addWidget(separator)
    
    def onBrowseFFmpegPath(self):
        """浏览FFmpeg路径按钮点击事件"""
        # 打开文件对话框选择目录
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "选择FFmpeg目录",
            self.ffmpegPathInput.text()
        )
        
        if dir_path:
            # 检查选择的目录中是否有ffmpeg.exe
            ffmpeg_exe_path = os.path.join(dir_path, "ffmpeg.exe")
            if os.path.exists(ffmpeg_exe_path):
                self.ffmpegPathInput.setText(dir_path)
                self.saveFFmpegPath(dir_path)
            else:
                from gui.ui.minecraft_dialog import MinecraftMessageBox
                MinecraftMessageBox.show_warning(
                    self,
                    "无效的FFmpeg目录",
                    "所选目录中未找到ffmpeg.exe文件。请选择包含ffmpeg.exe的有效目录。"
                )
    
    def onResetFFmpegPath(self):
        """重置FFmpeg路径按钮点击事件"""
        # 重置为默认路径
        default_ffmpeg_dir = os.path.join(app_path, 'ffmpeg')
        self.ffmpegPathInput.setText(default_ffmpeg_dir)
        self.saveFFmpegPath(default_ffmpeg_dir)
    
    def saveFFmpegPath(self, dir_path):
        """保存FFmpeg路径到配置文件"""
        try:
            from utils.main import config_path
            import json
            
            # 读取现有配置或创建新配置
            config = {}
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                except:
                    pass
            
            # 更新配置
            config['ffmpeg_path'] = dir_path
            
            # 保存配置
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
                
            from gui.ui.minecraft_dialog import MinecraftMessageBox
            MinecraftMessageBox.show_message(
                self,
                "设置已保存",
                "FFmpeg路径已更新，重启应用后生效。"
            )
        except Exception as e:
            from gui.ui.minecraft_dialog import MinecraftMessageBox
            MinecraftMessageBox.show_error(
                self,
                "保存设置失败",
                f"无法保存FFmpeg路径设置: {str(e)}"
            )
    
    def onFFmpegHelp(self):
        """FFmpeg帮助按钮点击事件"""
        from gui.ui.minecraft_dialog import MinecraftMessageBox
        
        MinecraftMessageBox.show_message(
            self,
            "FFmpeg设置帮助",
            """FFmpeg是一个用于处理音视频的开源软件，本应用需要使用它来处理音频文件。

如果您还没有安装FFmpeg，请按照以下步骤操作：
1. 访问FFmpeg官方网站 https://ffmpeg.org/download.html 下载适合您系统的版本
2. 解压下载的文件到您选择的目录
3. 在本应用的设置页面中，点击"浏览"按钮选择FFmpeg所在的目录
4. 确保选择的目录中包含ffmpeg.exe文件
5. 点击"确定"保存设置，然后重启应用

您也可以将FFmpeg添加到系统环境变量中，这样应用将自动检测并使用它。"""
        )
    
    # FFmpeg相关方法已移除
    
    # 文件关联设置已移除，现在在应用启动时自动关联
    
    # 文件关联相关方法已移除
    
    # 文件关联方法已移除，现在在应用启动时自动关联
    
    # 取消关联方法已移除，现在在应用启动时自动关联
    
    def onBack(self):
        """返回主页按钮点击事件"""
        self.backToMainPage.emit()