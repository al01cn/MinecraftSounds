from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QDesktopServices, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame

from gui.ui import MinecraftFrame, MinecraftTitleLabel, MinecraftLabel, apply_minecraft_style
from gui.ui.button import MinecraftPixelButton
from utils import GetLogoIcon

class AboutPage(QWidget):
    """关于页面"""
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
        
        # 创建关于内容区域
        self.aboutFrame = MinecraftFrame(frame_type="stone")
        self.aboutLayout = QVBoxLayout(self.aboutFrame)
        self.aboutLayout.setContentsMargins(15, 15, 15, 15)
        self.aboutLayout.setSpacing(20)
        self.aboutLayout.setAlignment(Qt.AlignCenter)
        
        # 创建关于标题
        self.aboutTitle = MinecraftTitleLabel("关于")
        self.aboutTitle.setAlignment(Qt.AlignCenter)
        self.aboutLayout.addWidget(self.aboutTitle)
        
        # 创建logo
        self.logoLabel = QLabel()
        logo_path = GetLogoIcon(False)
        self.logoLabel.setPixmap(QPixmap(logo_path))
        self.logoLabel.setAlignment(Qt.AlignCenter)
        self.aboutLayout.addWidget(self.logoLabel)
        
        # 创建应用名称
        self.appNameLabel = MinecraftTitleLabel("我的世界音乐包生成器")
        self.appNameLabel.setAlignment(Qt.AlignCenter)
        self.aboutLayout.addWidget(self.appNameLabel)
        
        # 创建版本信息
        self.versionLabel = MinecraftLabel("版本: 1.0.0")
        self.versionLabel.setAlignment(Qt.AlignCenter)
        self.aboutLayout.addWidget(self.versionLabel)
        
        # 创建作者信息
        self.authorLabel = MinecraftLabel("作者: MinecraftSounds团队")
        self.authorLabel.setAlignment(Qt.AlignCenter)
        self.aboutLayout.addWidget(self.authorLabel)
        
        # 创建描述信息
        self.descriptionLabel = MinecraftLabel("这是一个用于创建我的世界音乐包的工具，可以帮助你轻松地将音频文件转换为我的世界可用的音乐包格式。")
        self.descriptionLabel.setAlignment(Qt.AlignCenter)
        self.descriptionLabel.setWordWrap(True)
        self.aboutLayout.addWidget(self.descriptionLabel)
        
        # 创建GitHub链接按钮
        self.githubButton = MinecraftPixelButton("访问GitHub", button_type="blue")
        self.githubButton.setMinimumSize(150, 40)
        self.githubButton.clicked.connect(self.onGithub)
        self.aboutLayout.addWidget(self.githubButton, 0, Qt.AlignCenter)
        
        # 添加关于框架到主布局
        self.mainLayout.addWidget(self.aboutFrame)
    
    def onBack(self):
        """返回主页按钮点击事件"""
        self.backToMainPage.emit()
    
    def onGithub(self):
        """访问GitHub按钮点击事件"""
        # 这里可以替换为实际的GitHub仓库地址
        QDesktopServices.openUrl(QUrl("https://github.com/your-username/MinecraftSounds"))