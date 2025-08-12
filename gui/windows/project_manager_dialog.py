import os
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import QUrl

from utils import project_path, projectExists, deleteFolder, getProjectHistory, saveProjectHistory
from gui.ui import MinecraftFrame, MinecraftTitleLabel, MinecraftLabel, apply_minecraft_style
from gui.ui.button import MinecraftPixelButton
from gui.ui.minecraft_dialog import MinecraftMessageBox

class ProjectManagerDialog(QDialog):
    """项目管理弹窗"""
    projectDeleted = pyqtSignal(str)  # 项目删除信号
    projectListUpdated = pyqtSignal()  # 项目列表更新信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("项目管理")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumSize(600, 400)
        
        # 应用我的世界风格
        apply_minecraft_style(self)
        
        # 创建主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        # 创建标题
        self.title_label = MinecraftTitleLabel("项目管理")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)
        
        # 创建项目列表框架
        self.project_frame = MinecraftFrame(frame_type="stone")
        self.project_frame_layout = QVBoxLayout(self.project_frame)
        self.project_frame_layout.setContentsMargins(15, 15, 15, 15)
        self.project_frame_layout.setSpacing(10)
        
        # 创建项目列表标题
        self.list_title = MinecraftLabel("项目列表")
        self.list_title.setAlignment(Qt.AlignCenter)
        self.project_frame_layout.addWidget(self.list_title)
        
        # 创建项目列表
        self.project_list = QListWidget()
        self.project_list.setStyleSheet("""
            QListWidget {
                background-color: rgba(0, 0, 0, 100);
                border: 2px solid #555555;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #555555;
            }
            QListWidget::item:selected {
                background-color: rgba(60, 60, 180, 150);
            }
        """)
        self.project_frame_layout.addWidget(self.project_list)
        
        # 创建操作按钮布局
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(10)
        
        # 创建打开文件夹按钮
        self.open_folder_btn = MinecraftPixelButton("打开项目文件夹", button_type="blue")
        self.open_folder_btn.clicked.connect(self.openProjectFolder)
        self.button_layout.addWidget(self.open_folder_btn)
        
        # 创建删除项目按钮
        self.delete_btn = MinecraftPixelButton("删除项目", button_type="red")
        self.delete_btn.clicked.connect(self.deleteProject)
        self.button_layout.addWidget(self.delete_btn)
        
        # 添加按钮布局到项目框架
        self.project_frame_layout.addLayout(self.button_layout)
        
        # 添加项目框架到主布局
        self.main_layout.addWidget(self.project_frame)
        
        # 创建关闭按钮
        self.close_btn = MinecraftPixelButton("关闭", button_type="brown")
        self.close_btn.clicked.connect(self.close)
        self.main_layout.addWidget(self.close_btn, 0, Qt.AlignCenter)
        
        # 加载项目列表
        self.loadProjects()
    
    def loadProjects(self):
        """加载项目列表"""
        # 清空列表
        self.project_list.clear()
        
        # 获取项目历史记录
        history = getProjectHistory()
        
        # 添加项目到列表
        for item in history:
            project_name = item.get("name")
            if project_name and projectExists(project_name):
                list_item = QListWidgetItem(project_name)
                self.project_list.addItem(list_item)
    
    def openProjectFolder(self):
        """打开项目文件夹"""
        # 获取选中的项目
        selected_items = self.project_list.selectedItems()
        if not selected_items:
            MinecraftMessageBox.show_message(
                self,
                "提示",
                "请先选择一个项目"
            )
            return
        
        # 获取项目名称
        project_name = selected_items[0].text()
        
        # 获取项目路径
        project_folder = os.path.join(project_path, project_name)
        
        # 检查项目文件夹是否存在
        if not os.path.exists(project_folder):
            MinecraftMessageBox.show_message(
                self,
                "错误",
                f"项目文件夹不存在: {project_folder}"
            )
            return
        
        # 打开项目文件夹
        QDesktopServices.openUrl(QUrl.fromLocalFile(project_folder))
    
    def deleteProject(self):
        """删除项目"""
        # 获取选中的项目
        selected_items = self.project_list.selectedItems()
        if not selected_items:
            MinecraftMessageBox.show_message(
                self,
                "提示",
                "请先选择一个项目"
            )
            return
        
        # 获取项目名称
        project_name = selected_items[0].text()
        
        # 确认删除
        confirm_dialog = MinecraftMessageBox(
            self,
            "确认删除",
            f"确定要删除项目 {project_name} 吗？\n此操作不可恢复！",
            buttons=["确定", "取消"]
        )
        
        if confirm_dialog.exec_() == QDialog.Accepted and confirm_dialog.result_button == "确定":
            try:
                # 获取项目路径
                project_folder = os.path.join(project_path, project_name)
                
                # 删除项目文件夹
                deleteFolder(project_folder)
                
                # 刷新项目列表
                self.loadProjects()
                
                # 发送项目删除信号
                self.projectDeleted.emit(project_name)
                
                # 发送项目列表更新信号
                self.projectListUpdated.emit()
                
                # 显示删除成功消息
                MinecraftMessageBox.show_message(
                    self,
                    "成功",
                    f"项目 {project_name} 已成功删除"
                )
            except Exception as e:
                # 显示删除失败消息
                MinecraftMessageBox.show_message(
                    self,
                    "删除失败",
                    f"删除项目时发生错误: {str(e)}"
                )