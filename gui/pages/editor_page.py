from PyQt5.QtCore import Qt, QSize, QUrl, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QListWidget, QListWidgetItem, QFileDialog, QMessageBox)
import os
import shutil

from gui.ui import MinecraftFrame, MinecraftTitleLabel, MinecraftLabel, MinecraftBackground, apply_minecraft_style
from gui.ui.button import MinecraftPixelButton
from gui.ui.minecraft_dialog import MinecraftMessageBox, MinecraftMessageBoxResult
from core.minecraft import *
from utils.main import copyFile

class AudioFileSelector(MinecraftFrame):
    """音频文件选择器"""
    fileSelected = pyqtSignal(list)  # 文件选择信号，传递文件路径列表
    
    def __init__(self, parent=None):
        super().__init__(parent, frame_type="stone")
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
        
        self.textLabel = MinecraftLabel("点击下方按钮添加音频文件（支持多选）")
        self.textLabel.setAlignment(Qt.AlignCenter)
        
        # 创建选择文件按钮
        self.selectButton = MinecraftPixelButton("选择文件", button_type="brown")
        self.selectButton.clicked.connect(self.selectFile)
        
        # 添加组件到布局
        self.layout.addWidget(self.iconLabel)
        self.layout.addWidget(self.textLabel)
        self.layout.addWidget(self.selectButton, 0, Qt.AlignCenter)
    
    def selectFile(self):
        """选择文件按钮点击事件"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "选择音频文件", "", "音频文件 (*.ogg *.wav *.mp3 *.flac)"
        )
        if file_paths:
            valid_files = []
            invalid_files = []
            
            # 检查文件类型
            for file_path in file_paths:
                if self.isAudioFile(file_path):
                    valid_files.append(file_path)
                else:
                    invalid_files.append(os.path.basename(file_path))
            
            # 如果有有效文件，发送信号
            if valid_files:
                self.fileSelected.emit(valid_files)
            
            # 如果有无效文件，显示警告
            if invalid_files:
                MinecraftMessageBox.show_warning(
                    self,
                    "文件类型错误",
                    f"以下文件不是有效的音频文件 (.ogg, .wav, .mp3, .flac):\n{', '.join(invalid_files)}"
                )
    
    def isAudioFile(self, file_path):
        """检查是否为音频文件"""
        valid_extensions = [".ogg", ".wav", ".mp3", ".flac"]
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

class EditorPage(QWidget):
    """音乐包编辑器页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 应用我的世界风格
        apply_minecraft_style(self)

        # 当前项目路径
        self.current_project_path = None
        
        # 创建主布局
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(20)
        
        # 标题已移除，改为设置窗口标题
        self.title_text = "音乐包编辑器"
        
        # 创建顶部按钮区域
        self.topButtonLayout = QHBoxLayout()
        self.topButtonLayout.setContentsMargins(0, 0, 0, 0)
        self.topButtonLayout.setSpacing(20)
        
        # 创建返回按钮
        self.backButton = MinecraftPixelButton("返回主页", button_type="brown")
        self.backButton.setMinimumSize(120, 40)
        self.backButton.clicked.connect(self.onBack)
        
        # 创建重构和导出按钮
        self.rebuildButton = MinecraftPixelButton("重构", button_type="green")
        self.rebuildButton.setMinimumSize(120, 40)
        self.rebuildButton.clicked.connect(self.onRebuild)
        
        self.exportButton = MinecraftPixelButton("导出", button_type="blue")
        self.exportButton.setMinimumSize(120, 40)
        self.exportButton.clicked.connect(self.onExport)
        
        # 添加按钮到顶部布局
        self.topButtonLayout.addWidget(self.backButton)
        self.topButtonLayout.addWidget(self.rebuildButton)
        self.topButtonLayout.addStretch(1)
        self.topButtonLayout.addWidget(self.exportButton)
        
        # 添加顶部按钮布局到主布局
        self.mainLayout.addLayout(self.topButtonLayout)
        
        # 创建音频文件选择器
        self.fileSelector = AudioFileSelector(self)
        self.fileSelector.fileSelected.connect(self.onFileSelected)
        self.mainLayout.addWidget(self.fileSelector)
        
        # 创建音频列表区域
        self.listFrame = MinecraftFrame(frame_type="stone")
        self.listLayout = QVBoxLayout(self.listFrame)
        self.listLayout.setContentsMargins(10, 10, 10, 10)
        self.listLayout.setSpacing(5)
        
        # 创建列表标题区域（标题和添加分类按钮）
        self.listTitleLayout = QHBoxLayout()
        self.listTitleLayout.setContentsMargins(0, 0, 0, 0)
        self.listTitleLayout.setSpacing(10)
        
        # 创建列表标题
        self.listTitleLabel = MinecraftLabel("已添加的音频文件")
        self.listTitleLayout.addWidget(self.listTitleLabel)
        
        # 添加弹性空间
        self.listTitleLayout.addStretch(1)
        
        # 创建添加分类按钮
        self.addCategoryButton = MinecraftPixelButton("添加分类", button_type="green")
        self.addCategoryButton.setFixedSize(100, 30)
        self.addCategoryButton.clicked.connect(self.onAddCategory)
        self.listTitleLayout.addWidget(self.addCategoryButton)
        
        # 创建删除分类按钮
        self.deleteCategoryButton = MinecraftPixelButton("删除分类", button_type="red")
        self.deleteCategoryButton.setFixedSize(100, 30)
        self.deleteCategoryButton.clicked.connect(self.onDeleteCategory)
        self.deleteCategoryButton.setEnabled(False)  # 初始状态为禁用
        self.listTitleLayout.addWidget(self.deleteCategoryButton)
        
        # 将标题布局添加到列表布局
        self.listLayout.addLayout(self.listTitleLayout)
        
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
        
        # 初始化音频文件列表和分类列表
        self.audioFiles = []
        self.categories = []
        
    
    # 返回主页信号
    backToMainPage = pyqtSignal()
    
    def onBack(self):
        """返回主页按钮点击事件"""
        # 尝试多种方式返回主页
        
        # 1. 尝试通过信号
        self.backToMainPage.emit()
        
        # 2. 尝试通过父窗口
        parent = self.parent()
        while parent:
            if hasattr(parent, 'stackedWidget'):
                parent.stackedWidget.setCurrentIndex(0)
                return
            parent = parent.parent()
        
        # 3. 尝试通过活动窗口
        from PyQt5.QtWidgets import QApplication
        mainWindow = QApplication.instance().activeWindow()
        if mainWindow and hasattr(mainWindow, 'stackedWidget'):
            mainWindow.stackedWidget.setCurrentIndex(0)
    
    def loadProject(self, project_name):
        """加载项目"""
        # 加载项目配置
        pj_path = ProjectPath(project_name)

        self.current_project_path = pj_path

        # 更新窗口标题
        self.title_text = f"音乐包编辑器 - {pj_path.project_name}"
        
        # 设置窗口标题
        window = self.window()
        if window:
            window.setWindowTitle(self.title_text)
        
        # 清空当前列表
        self.audioFiles = []
        self.audioList.clear()
        
        # 加载项目文件
        # TODO: 实现项目文件加载逻辑
    
    def onFileSelected(self, file_paths):
        """文件选择事件处理"""
        # 处理多个文件
        added_count = 0
        duplicate_files = []
        copy_failed_files = []
        
        # 确保项目路径已设置
        if not self.current_project_path:
            MinecraftMessageBox.show_warning(
                self,
                "项目未加载",
                "无法添加音频文件，请先加载项目"
            )
            return
        
        # 获取缓存文件夹路径
        cache_dir = self.current_project_path.cache()
        
        # 确保缓存文件夹存在
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        
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
            
            # 复制文件到缓存文件夹
            try:
                copyFile(file_path, cache_dir)
            except Exception as e:
                copy_failed_files.append(f"{os.path.basename(file_path)} (错误: {str(e)})")
        
        # 显示添加结果
        if added_count > 0:
            success_message = f"成功添加了 {added_count} 个音频文件"
            if not copy_failed_files:
                success_message += "，并已复制到缓存文件夹"
            MinecraftMessageBox.show_message(
                self,
                "添加成功",
                success_message
            )
        
        # 如果有复制失败的文件，显示警告
        if copy_failed_files:
            MinecraftMessageBox.show_warning(
                self,
                "文件复制失败",
                f"以下文件复制到缓存文件夹失败:\n{', '.join(copy_failed_files)}"
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
            try:
                # 只删除缓存目录中的对应文件
                if self.current_project_path:
                    cache_dir = self.current_project_path.cache()
                    cache_file_path = os.path.join(cache_dir, os.path.basename(file_path))
                    if os.path.exists(cache_file_path):
                        delFile(cache_file_path)
                
                self.audioFiles.remove(file_path)
                self.audioList.takeItem(index)
                MinecraftMessageBox.show_message(
                    self,
                    "删除成功",
                    f"已成功从列表中移除 {os.path.basename(file_path)}"
                )
            except Error as e:
                MinecraftMessageBox.show_warning(
                    self,
                    "删除失败",
                    f"删除文件失败: {str(e)}"
                )
                return

    
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
    
    def onAddCategory(self):
        """添加分类按钮点击事件"""
        from gui.ui.minecraft_dialog import MinecraftInputDialog
        
        # 创建输入对话框
        dialog = MinecraftInputDialog(
            self,
            "创建分类",
            "请输入分类名称：",
            ""
        )
        
        # 显示对话框并获取结果
        result = dialog.exec_()
        
        # 如果用户点击了确定按钮
        if result == MinecraftMessageBoxResult.ok:
            category_name = dialog.get_input_text()
            if category_name:
                # 检查分类是否已存在
                if category_name in self.categories:
                    MinecraftMessageBox.show_warning(
                        self,
                        "创建失败",
                        f"分类 \"{category_name}\" 已存在"
                    )
                    return
                
                # 添加分类到列表
                self.categories.append(category_name)

                createFolder(self.current_project_path.soundf(category_name))
                
                # 更新删除分类按钮状态
                self.updateDeleteCategoryButtonState()
                
                MinecraftMessageBox.show_message(
                    self,
                    "创建成功",
                    f"已成功创建分类 \"{category_name}\""
                )
            else:
                MinecraftMessageBox.show_warning(
                    self,
                    "创建失败",
                    "分类名称不能为空"
                )
    
    def updateDeleteCategoryButtonState(self):
        """更新删除分类按钮状态"""
        self.deleteCategoryButton.setEnabled(len(self.categories) > 0)
    
    def onDeleteCategory(self):
        """删除分类按钮点击事件"""
        if not self.categories:
            MinecraftMessageBox.show_warning(
                self,
                "无法删除",
                "没有可删除的分类"
            )
            return
        
        from gui.ui.minecraft_dialog import MinecraftCheckboxDialog
        
        # 创建多选对话框
        dialog = MinecraftCheckboxDialog(
            self,
            "删除分类",
            "请选择要删除的分类：",
            self.categories
        )
        
        # 显示对话框并获取结果
        result = dialog.exec_()
        
        # 如果用户点击了确定按钮
        if result == MinecraftMessageBoxResult.ok:
            selected_categories = dialog.get_selected_items()
            if selected_categories:
                # 从列表中移除选中的分类
                for category in selected_categories:
                    if category in self.categories:
                        delFolder(self.current_project_path.soundf(category))
                        self.categories.remove(category)
                
                # 更新删除分类按钮状态
                self.updateDeleteCategoryButtonState()
                
                # 显示删除成功消息
                if len(selected_categories) == 1:
                    message = f"已成功删除分类 \"{selected_categories[0]}\""
                else:
                    message = f"已成功删除 {len(selected_categories)} 个分类"
                
                MinecraftMessageBox.show_message(
                    self,
                    "删除成功",
                    message
                )
            else:
                MinecraftMessageBox.show_warning(
                    self,
                    "删除失败",
                    "未选择任何分类"
                )