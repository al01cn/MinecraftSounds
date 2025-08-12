import os
import time
from uu import Error
from PyQt5.QtCore import Qt, QUrl, QSize, QEventLoop, QTimer
from PyQt5.QtGui import QDesktopServices, QGuiApplication, QPixmap
from PyQt5.QtWidgets import (QApplication, QFrame, QHBoxLayout, QWidget, QLabel, QVBoxLayout,
                             QScrollArea, QStackedWidget, QPushButton, QFileDialog)
from utils import GetLogoIcon, GetIcon, project_path, getProjectHistory, saveProjectHistory
from gui.ui import MinecraftFrame, MinecraftTitleLabel, MinecraftLabel, MinecraftBackground, MinecraftTitle, apply_minecraft_style
from gui.ui.button import MinecraftPixelButton
from gui.components.ffmpeg_status import FFmpegStatusWidget
from gui.pages import EditorPage, SettingsPage, AboutPage
from gui.pages.export_page import ExportPage
from gui.ui.minecraft_dialog import MinecraftMessageBox
from gui.windows.project_manager_dialog import ProjectManagerDialog
from core.project import ProjectConfig, Project
import time

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
        # 连接编辑器页面的切换到导出页面信号
        self.editorPage.switchToExportPage.connect(self.switchToExportPage)
        
        # 创建导出页面
        self.exportPage = ExportPage(self)
        # 连接导出页面的返回编辑器页面信号
        self.exportPage.backToEditorPage.connect(self.backToEditorPage)
        
        # 创建设置页面
        self.settingsPage = SettingsPage(self)
        # 连接设置页面的返回主页信号
        self.settingsPage.backToMainPage.connect(self.backToMainPage)
        
        # 创建关于页面
        self.aboutPage = AboutPage(self)
        # 连接关于页面的返回主页信号
        self.aboutPage.backToMainPage.connect(self.backToMainPage)
        
        # 将页面添加到堆叠小部件
        self.stackedWidget.addWidget(self.mainPage)  # 索引0 - 主页面
        self.stackedWidget.addWidget(self.editorPage)  # 索引1 - 编辑器页面
        self.stackedWidget.addWidget(self.exportPage)  # 索引2 - 导出页面
        self.stackedWidget.addWidget(self.settingsPage)  # 索引3 - 设置页面
        self.stackedWidget.addWidget(self.aboutPage)  # 索引4 - 关于页面
        
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
        self.background = MinecraftBackground(self.mainPage, pattern="planks")
        self.background.setGeometry(0, 0, self.width(), self.height())
        
        # 创建主页面布局
        self.mainPageLayout = QVBoxLayout(self.mainPage)
        self.mainPageLayout.setContentsMargins(20, 20, 20, 20)
        self.mainPageLayout.setSpacing(30)
        self.mainPageLayout.setAlignment(Qt.AlignCenter)
        
        # 创建右下角设置按钮区域
        self.settingsButtonFrame = QFrame(self.mainPage)
        self.settingsButtonFrame.setStyleSheet("background: transparent;")
        self.settingsButtonLayout = QHBoxLayout(self.settingsButtonFrame)
        self.settingsButtonLayout.setContentsMargins(0, 0, 0, 0)
        
        # 创建设置按钮
        self.settingsButton = MinecraftPixelButton("设置", button_type="gray")
        self.settingsButton.setFixedSize(80, 30)
        self.settingsButton.clicked.connect(self.onSettings)
        self.settingsButton.setStyleSheet("background-color: transparent;")
        
        # 添加设置按钮到右下角布局
        self.settingsButtonLayout.addWidget(self.settingsButton)
        
        # 创建左下角关于按钮区域
        self.aboutButtonFrame = QFrame(self.mainPage)
        self.aboutButtonFrame.setStyleSheet("background: transparent;")
        self.aboutButtonLayout = QHBoxLayout(self.aboutButtonFrame)
        self.aboutButtonLayout.setContentsMargins(0, 0, 0, 0)
        
        # 创建关于按钮
        self.aboutButton = MinecraftPixelButton("关于", button_type="gray")
        self.aboutButton.setFixedSize(80, 30)
        self.aboutButton.clicked.connect(self.onAbout)
        self.aboutButton.setStyleSheet("background-color: transparent;")
        
        # 添加关于按钮到左下角布局
        self.aboutButtonLayout.addWidget(self.aboutButton)
        
        # 将按钮区域放在窗口左下角和右下角
        self.settingsButtonFrame.setParent(self.mainPage)
        self.aboutButtonFrame.setParent(self.mainPage)
        
        # 确保组件在窗口初始化后正确定位
        def updateButtonsPosition():
            # 设置按钮放在窗口右下角
            self.settingsButtonFrame.move(
                self.mainPage.width() - self.settingsButtonFrame.width() - 20,
                self.mainPage.height() - self.settingsButtonFrame.height() - 20
            )
            # 关于按钮放在窗口左下角
            self.aboutButtonFrame.move(
                20,
                self.mainPage.height() - self.aboutButtonFrame.height() - 20
            )
        
        # 在窗口显示后调用一次以正确定位
        QTimer.singleShot(100, updateButtonsPosition)
        
        # 创建标题
        self.titleLabel = MinecraftTitle("Minecraft\n我的世界音乐包生成器")
        self.titleLabel.setMinimumHeight(60)
        
        # 添加标题到主页面布局
        self.mainPageLayout.addWidget(self.titleLabel, 0, Qt.AlignCenter)
        
        # 创建FFmpeg状态组件
        self.ffmpegStatus = FFmpegStatusWidget()
        self.ffmpegStatus.ffmpeg_downloaded.connect(self.onFFmpegDownloaded)
        
        # 将FFmpeg状态组件放在窗口顶部
        self.ffmpegStatus.setParent(self.mainPage)
        
        # 确保组件在窗口初始化后正确定位
        def updateFFmpegPosition():
            # 放在窗口顶部中央
            self.ffmpegStatus.move(
                (self.mainPage.width() - self.ffmpegStatus.width()) // 2,
                10
            )
        
        # 在窗口显示后调用一次以正确定位
        QTimer.singleShot(100, updateFFmpegPosition)
        QTimer.singleShot(100, updateButtonsPosition)
        
        # 窗口大小变化时更新组件位置
        def custom_resize_event(event):
            # 更新FFmpeg状态组件位置
            updateFFmpegPosition()
            # 更新左下角和右下角按钮位置
            updateButtonsPosition()
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
        
        self.manageProjectBtn = MinecraftPixelButton("项目管理", button_type="blue")
        self.manageProjectBtn.setMinimumSize(150, 40)
        self.manageProjectBtn.clicked.connect(self.onManageProject)
        
        # 添加按钮到水平布局
        self.buttonLayout.addWidget(self.createProjectBtn)
        self.buttonLayout.addWidget(self.openProjectBtn)
        self.buttonLayout.addWidget(self.manageProjectBtn)
        
        # 将按钮布局添加到框架布局
        self.buttonFrameLayout.addLayout(self.buttonLayout)
        
        # 创建历史项目区域
        self.historyLabel = MinecraftTitleLabel("历史项目")
        self.historyLabel.setAlignment(Qt.AlignCenter)
        self.buttonFrameLayout.addWidget(self.historyLabel)
        
        # 创建历史项目滚动区域
        self.historyScrollArea = QScrollArea()
        self.historyScrollArea.setWidgetResizable(True)
        self.historyScrollArea.setFrameShape(QFrame.NoFrame)
        self.historyScrollArea.setMinimumHeight(100)
        self.historyScrollArea.setMaximumHeight(150)
        
        # 创建历史项目容器
        self.historyContainer = QWidget()
        self.historyLayout = QVBoxLayout(self.historyContainer)
        self.historyLayout.setContentsMargins(0, 0, 0, 0)
        self.historyLayout.setSpacing(5)
        self.historyLayout.setAlignment(Qt.AlignTop)
        
        # 设置滚动区域的小部件
        self.historyScrollArea.setWidget(self.historyContainer)
        
        # 添加历史项目滚动区域到按钮框架
        self.buttonFrameLayout.addWidget(self.historyScrollArea)
        
        # 加载历史项目
        self.loadHistoryProjects()
        
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
            project_name = project_info["name"]
            project_description = project_info["description"]
            project_icon = project_info["icon_path"]
            pack_format = project_info["pack_format"]
            sound_main_key = project_info["sound_main_key"]
            
            project = Project(project_name, project_description, project_icon, pack_format, sound_main_key)
            try:
                project.create()
            except Error as e:
                MinecraftMessageBox.show_error(
                    self,
                    "项目创建失败",
                    str(e)
                )
                return

            # 保存到历史记录
            saveProjectHistory(project_name)
            
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
            
            # 刷新历史项目列表
            self.loadHistoryProjects()

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
    
    def onManageProject(self):
        """项目管理按钮点击事件"""
        # 创建项目管理弹窗
        dialog = ProjectManagerDialog(self)
        
        # 连接项目删除信号
        dialog.projectDeleted.connect(self.onProjectDeleted)
        
        # 连接项目列表更新信号
        dialog.projectListUpdated.connect(self.loadHistoryProjects)
        
        # 显示弹窗
        dialog.exec_()
    
    def onProjectDeleted(self, project_name):
        """项目删除回调"""
        # 如果当前打开的项目被删除，返回主页面
        if self.editorPage.project_name == project_name:
            self.backToMainPage()
            MinecraftMessageBox.show_message(
                self,
                "提示",
                f"当前打开的项目 {project_name} 已被删除"
            )
    
    
    def loadHistoryProjects(self):
        """加载历史项目"""
        # 清空历史项目布局
        while self.historyLayout.count():
            item = self.historyLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # 获取历史项目记录
        history = getProjectHistory()
        
        if not history:
            # 如果没有历史项目，显示提示信息
            noHistoryLabel = MinecraftLabel("暂无历史项目")
            noHistoryLabel.setAlignment(Qt.AlignCenter)
            self.historyLayout.addWidget(noHistoryLabel)
            return
        
        # 添加历史项目按钮
        for item in history:
            project_name = item.get("name")
            last_access = item.get("last_access", 0)
            
            # 创建项目按钮
            projectBtn = MinecraftPixelButton(project_name, button_type="blue")
            projectBtn.setMinimumHeight(30)
            
            # 设置工具提示（显示最后访问时间）
            last_access_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_access))
            projectBtn.setToolTip(f"最后访问时间: {last_access_time}")
            
            # 连接点击事件
            projectBtn.clicked.connect(lambda checked, name=project_name: self.openHistoryProject(name))
            
            # 添加到布局
            self.historyLayout.addWidget(projectBtn)
    
    def openHistoryProject(self, project_name):
        """打开历史项目"""
        try:
            # 保存到历史记录
            saveProjectHistory(project_name)
            
            # 加载项目到编辑器页面
            self.editorPage.loadProject(project_name)
            
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
            
            # 保存到历史记录
            saveProjectHistory(self.current_project_path.project_name)
            
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
    
    def backToEditorPage(self):
        """返回编辑器页面"""
        self.stackedWidget.setCurrentIndex(1)
        self.setWindowTitle(self.editorPage.title_text)
    
    def switchToExportPage(self, project_path, audio_files):
        """切换到导出页面"""
        # 加载项目到导出页面
        self.exportPage.loadProject(project_path, audio_files)
        # 切换到导出页面
        self.stackedWidget.setCurrentIndex(2)
    
    def onSettings(self):
        """设置按钮点击事件"""
        # 切换到设置页面
        self.stackedWidget.setCurrentIndex(3)
        # 设置窗口标题
        self.setWindowTitle("设置 - 我的世界音乐包生成器")
    
    def onAbout(self):
        """关于按钮点击事件"""
        # 切换到关于页面
        self.stackedWidget.setCurrentIndex(4)
        # 设置窗口标题
        self.setWindowTitle("关于 - 我的世界音乐包生成器")
        
    def onManageProject(self):
        """打开项目管理弹窗"""
        dialog = ProjectManagerDialog(self)
        # 连接项目删除信号
        dialog.projectDeleted.connect(self.onProjectDeleted)
        # 连接项目列表更新信号
        dialog.projectListUpdated.connect(self.loadHistoryProjects)
        dialog.exec_()
    
    def onProjectDeleted(self, project_name):
        """项目删除回调"""
        # 如果当前打开的项目被删除，则返回主页面
        if self.stackedWidget.currentIndex() == 1 and self.editorPage.current_project_path and \
           self.editorPage.current_project_path.project_name == project_name:
            # 返回主页面
            self.backToMainPage()
            # 提示用户
            MinecraftMessageBox.show_info(
                self,
                "项目已删除",
                f"当前打开的项目 {project_name} 已被删除。"
            )

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
            
        # 设置固定窗口大小，不允许用户调整
        self.setFixedSize(width, height)
        self.setWindowIcon(GetLogoIcon())
        self.setWindowTitle('MinecraftSounds - 我的世界音乐包生成器')
        
        # 设置窗口标志，禁用最大化按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

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