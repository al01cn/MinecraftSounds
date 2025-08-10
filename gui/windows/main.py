import os
from PyQt5.QtCore import Qt, QUrl, QSize, QEventLoop, QTimer
from PyQt5.QtGui import QDesktopServices, QGuiApplication, QPixmap
from PyQt5.QtWidgets import (QApplication, QFrame, QHBoxLayout, QWidget, QLabel, QVBoxLayout,
                             QScrollArea, QStackedWidget, QPushButton, QFileDialog)
from utils import GetLogoIcon, GetIcon, project_path
from gui.ui import MinecraftFrame, MinecraftTitleLabel, MinecraftLabel, MinecraftBackground, MinecraftTitle, apply_minecraft_style
from gui.ui.button import MinecraftPixelButton
from gui.ui.button.minecraft_settings_button import MinecraftSettingsButton
from gui.components.ffmpeg_status import FFmpegStatusWidget
from gui.pages import EditorPage
from gui.ui.minecraft_dialog import MinecraftMessageBox
from core.project import ProjectConfig, Project

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initWindow()
        self.nclose = True
        
        # 应用我的世界风格
        apply_minecraft_style(self)

        # 创建堆叠小部件来管理不同页面
        self.stackedWidget = QStackedWidget(self)
        
        # 创建主页面
        self.mainPage = QWidget()
        self.createMainPage()
        
        # 创建编辑器页面
        self.editorPage = EditorPage(self)
        # 连接编辑器页面的返回主页信号
        self.editorPage.backToMainPage.connect(self.backToMainPage)
        
        # 将页面添加到堆叠小部件
        self.stackedWidget.addWidget(self.mainPage)  # 索引0 - 主页面
        self.stackedWidget.addWidget(self.editorPage)  # 索引1 - 编辑器页面
        
        # 创建主布局
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.addWidget(self.stackedWidget)
        
        # 默认显示主页面
        self.stackedWidget.setCurrentIndex(0)
        
        # 当前项目路径
        self.current_project_path = None
    
    def createMainPage(self):
        """创建主页面"""
        # 创建背景
        self.background = MinecraftBackground(self.mainPage, pattern="dirt")
        self.background.setGeometry(0, 0, self.width(), self.height())
        
        # 创建主页面布局
        self.mainPageLayout = QVBoxLayout(self.mainPage)
        self.mainPageLayout.setContentsMargins(20, 20, 20, 20)
        self.mainPageLayout.setSpacing(30)
        self.mainPageLayout.setAlignment(Qt.AlignCenter)
        
        # 创建标题
        self.titleLabel = MinecraftTitle("Minecraft\n我的世界音乐包生成器")
        self.titleLabel.setMinimumHeight(60)
        
        # 添加标题到主页面布局
        self.mainPageLayout.addWidget(self.titleLabel, 0, Qt.AlignCenter)
        
        # 创建FFmpeg状态组件
        self.ffmpegStatus = FFmpegStatusWidget()
        self.ffmpegStatus.ffmpeg_downloaded.connect(self.onFFmpegDownloaded)
        
        # 将FFmpeg状态组件放在窗口底部
        self.ffmpegStatus.setParent(self.mainPage)
        
        # 确保组件在窗口初始化后正确定位
        def updateFFmpegPosition():
            # 放在窗口底部中央
            self.ffmpegStatus.move(
                (self.mainPage.width() - self.ffmpegStatus.width()) // 2,
                self.mainPage.height() - self.ffmpegStatus.height() - 10
            )
        
        # 在窗口显示后调用一次以正确定位
        QTimer.singleShot(100, updateFFmpegPosition)
        
        # 窗口大小变化时更新FFmpeg状态组件位置
        original_resize_event = self.mainPage.resizeEvent
        def custom_resize_event(event):
            if original_resize_event:
                original_resize_event(event)
            updateFFmpegPosition()
        self.mainPage.resizeEvent = custom_resize_event
        
        # 创建logo
        self.logoLabel = QLabel()
        logo_path = GetLogoIcon(False)
        self.logoLabel.setPixmap(QPixmap(logo_path))
        self.logoLabel.setAlignment(Qt.AlignCenter)
        
        # 添加logo到主页面布局
        self.mainPageLayout.addWidget(self.logoLabel, 0, Qt.AlignCenter)
        
        # 创建一个框架来容纳按钮
        self.buttonFrame = MinecraftFrame(frame_type="stone")
        self.buttonFrame.setMinimumSize(400, 150)
        self.buttonFrameLayout = QVBoxLayout(self.buttonFrame)
        self.buttonFrameLayout.setContentsMargins(20, 20, 20, 20)
        self.buttonFrameLayout.setSpacing(20)
        self.buttonFrameLayout.setAlignment(Qt.AlignCenter)
        
        # 创建按钮的水平布局
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setSpacing(20)
        self.buttonLayout.setAlignment(Qt.AlignCenter)
        
        # 创建按钮
        self.createProjectBtn = MinecraftPixelButton("创建项目", button_type="green")
        self.createProjectBtn.setMinimumSize(150, 40)
        self.createProjectBtn.clicked.connect(self.onCreateProject)
        
        self.openProjectBtn = MinecraftPixelButton("打开项目", button_type="brown")
        self.openProjectBtn.setMinimumSize(150, 40)
        self.openProjectBtn.clicked.connect(self.onOpenProject)
        
        self.testEditorBtn = MinecraftPixelButton("测试编辑器", button_type="purple")
        self.testEditorBtn.setMinimumSize(150, 40)
        self.testEditorBtn.clicked.connect(self.onTestEditor)
        
        # 添加按钮到水平布局
        self.buttonLayout.addWidget(self.createProjectBtn)
        self.buttonLayout.addWidget(self.openProjectBtn)
        self.buttonLayout.addWidget(self.testEditorBtn)
        
        # 将按钮布局添加到框架布局
        self.buttonFrameLayout.addLayout(self.buttonLayout)
        
        # 创建设置按钮
        self.settingsBtn = MinecraftSettingsButton()
        # 不需要设置最小尺寸，因为MinecraftSettingsButton已经设置了固定大小
        self.settingsBtn.clicked.connect(self.onSettings)
        self.buttonFrameLayout.addWidget(self.settingsBtn, 0, Qt.AlignCenter)
        
        # 将按钮框架添加到主页面布局
        self.mainPageLayout.addWidget(self.buttonFrame, 0, Qt.AlignCenter)

        # 3. 创建子界面

        # 4. 隐藏启动页面

        # create sub interface

    def onCreateProject(self):
        """创建项目按钮点击事件"""
        from gui.windows.create_project_dialog import CreateProjectDialog
        
        dialog = CreateProjectDialog(self)
        result = dialog.exec_()
        
        if result == dialog.Accepted:
            project_info = dialog.getProjectInfo()
            print("创建项目信息:", project_info)
            project_name = project_info["name"]
            project_description = project_info["description"]
            project_icon = project_info["icon_path"]
            pack_format = project_info["pack_format"]
            sound_main_key = project_info["sound_main_key"]
            
            project = Project(project_name, project_description, project_icon, pack_format, sound_main_key)
            project.create()
            
            # 切换到编辑器页面
            self.editorPage.loadProject(project_name)

            self.stackedWidget.setCurrentIndex(1)
            # 设置窗口标题
            self.setWindowTitle(self.editorPage.title_text)
            # 显示提示信息
            MinecraftMessageBox.show_message(
                self,
                "项目创建成功",
                f"项目 {project_name} 已成功创建。"
            )

            # TODO: 使用项目信息创建实际的项目
            # self.createNewProject(project_info)
        
    def onOpenProject(self):
        """打开项目按钮点击事件"""
        # 打开文件对话框，选择.mcsd文件
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开项目", "", "音乐包项目文件 (*.mcsd)"
        )
        
        if file_path:
            self.openProjectFile(file_path)
        
    def onSettings(self):
        """设置按钮点击事件"""
        print("设置")
        # 这里添加设置的逻辑
        
    def onTestEditor(self):
        """测试编辑器按钮点击事件"""
        # 创建一个测试项目路径
        # 加载测试项目到编辑器页面
        self.editorPage.loadProject("qwq")
        
        # 切换到编辑器页面
        self.stackedWidget.setCurrentIndex(1)
        
        # 设置窗口标题
        self.setWindowTitle(self.editorPage.title_text)
        
        # 显示提示信息
        MinecraftMessageBox.show_message(
            self,
            "测试模式",
            "已进入编辑器测试模式，您可以测试编辑器的各项功能。"
        )
    
    def openProjectFile(self, file_path):
        """打开项目文件"""
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                MinecraftMessageBox.show_error(
                    self,
                    "文件错误",
                    f"文件不存在: {file_path}"
                )
                return
            
            # 检查文件扩展名
            if not file_path.lower().endswith('.mcsd'):
                MinecraftMessageBox.show_error(
                    self,
                    "文件类型错误",
                    "请选择有效的音乐包项目文件 (.mcsd)"
                )
                return
            
            # 设置当前项目路径
            self.current_project_path = ProjectConfig.load_config(file_path)
            
            # 加载项目到编辑器页面
            self.editorPage.loadProject(self.current_project_path.project_name)
            
            # 切换到编辑器页面
            self.stackedWidget.setCurrentIndex(1)
            
            # 设置窗口标题
            self.setWindowTitle(self.editorPage.title_text)
            
        except Exception as e:
            MinecraftMessageBox.show_error(
                self,
                "打开项目失败",
                f"错误信息: {str(e)}"
            )
        
    def onFFmpegDownloaded(self, success):
        """FFmpeg下载完成回调"""
        if success:
            print("FFmpeg下载成功，UI已更新")
        else:
            print("FFmpeg下载失败")
            
    def backToMainPage(self):
        """返回主页面"""
        self.stackedWidget.setCurrentIndex(0)
        # 恢复窗口标题
        self.setWindowTitle('MinecraftSounds - 我的世界音乐包生成器')

    def initWindow(self):
        # 获取屏幕信息
        screen = QGuiApplication.primaryScreen()
        screen_size = screen.availableSize()
        dpi_scale = screen.devicePixelRatio()
        
        # 根据屏幕大小和DPI缩放调整窗口大小
        base_width, base_height = 900, 700
        min_width, min_height = 800, 600
        
        # 如果屏幕尺寸较小，适当缩小窗口
        if screen_size.width() < 1200 or screen_size.height() < 800:
            width = min(base_width, int(screen_size.width() * 0.8))
            height = min(base_height, int(screen_size.height() * 0.8))
        else:
            width = base_width
            height = base_height
            
        self.resize(width, height)
        self.setMinimumSize(min_width, min_height)
        self.setWindowIcon(GetLogoIcon())
        self.setWindowTitle('MinecraftSounds - 我的世界音乐包生成器')

        # 居中显示窗口
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        
        # 设置窗口样式
        self.setStyleSheet("""
            QWidget#mainWindow {
                background-color: #373737;
            }
        """)
        self.setObjectName("mainWindow")

        # set the minimum window width that allows the navigation panel to be expanded
        # self.navigationInterface.setMinimumExpandWidth(900)
        # self.navigationInterface.expand(useAni=False)