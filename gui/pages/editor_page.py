from PyQt5.QtCore import Qt, QSize, QUrl, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QListWidget, QListWidgetItem, QFileDialog, QMessageBox)
import os
import shutil

from gui.ui import MinecraftFrame, MinecraftTitleLabel, MinecraftLabel, MinecraftBackground, apply_minecraft_style
from gui.ui.button import MinecraftPixelButton
from gui.ui.minecraft_dialog import MinecraftMessageBox, MinecraftMessageBoxResult
from core.minecraft.projectPath import ProjectPath
from utils.main import copyFile, getFileList, getFolderList, delFile, delFolder, createFolder

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
    categoryChanged = pyqtSignal(str, str)  # 分类变更信号，传递文件路径和新分类
    soundKeyChanged = pyqtSignal(str, str)  # soundKey变更信号，传递文件路径和新soundKey
    
    def __init__(self, file_path, parent=None, categories=None):
        super().__init__(parent)
        self.file_path = file_path
        
        # 创建布局
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(15)
        
        # 获取文件名并去除后缀
        file_name = os.path.basename(file_path)
        file_name_without_ext = os.path.splitext(file_name)[0]
        
        # 文件名标签（不含后缀）
        self.nameLabel = MinecraftLabel(file_name_without_ext)
        self.nameLabel.setFixedWidth(200)
        
        # 生成并设置soundKey
        self.soundKey = self.generateSoundKey(file_name_without_ext)
        
        # soundKey输入框
        from PyQt5.QtWidgets import QLineEdit
        self.soundKeyEdit = QLineEdit(self.soundKey)
        self.soundKeyEdit.setFixedSize(150, 30)
        self.soundKeyEdit.setStyleSheet("""
            QLineEdit {
                background-color: #373737;
                border: 2px solid #1F1F1F;
                color: #FFFFFF;
                padding: 5px;
                font-family: 'Minecraft';
            }
        """)
        self.soundKeyEdit.setMaxLength(5)  # 限制最大长度为5个字符
        self.soundKeyEdit.textChanged.connect(self.onSoundKeyChanged)
        
        # 分类下拉框
        from PyQt5.QtWidgets import QComboBox
        self.categoryComboBox = QComboBox()
        self.categoryComboBox.setFixedSize(150, 30)
        self.categoryComboBox.setStyleSheet("""
            QComboBox {
                background-color: #373737;
                border: 2px solid #1F1F1F;
                color: #FFFFFF;
                padding: 5px;
                font-family: 'Minecraft';
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #1F1F1F;
            }
            QComboBox QAbstractItemView {
                background-color: #373737;
                border: 2px solid #1F1F1F;
                color: #FFFFFF;
                selection-background-color: #4A4A4A;
            }
        """)
        
        # 添加默认选项
        self.categoryComboBox.addItem("无分类")
        
        # 添加分类选项
        if categories:
            for category in categories:
                self.categoryComboBox.addItem(category)
        
        # 连接分类变更信号
        self.categoryComboBox.currentTextChanged.connect(self.onCategoryChanged)
        
        # 删除按钮
        self.deleteButton = MinecraftPixelButton("删除", button_type="red")
        self.deleteButton.setFixedSize(80, 30)
        self.deleteButton.clicked.connect(self.onDelete)
        
        # 添加组件到布局
        self.layout.addWidget(self.nameLabel, 0, Qt.AlignLeft)
        self.layout.addWidget(self.soundKeyEdit, 0, Qt.AlignLeft)
        self.layout.addStretch(1)
        self.layout.addWidget(self.categoryComboBox, 0, Qt.AlignRight)
        self.layout.addWidget(self.deleteButton, 0, Qt.AlignRight)
    
    def onDelete(self):
        """删除按钮点击事件"""
        self.deleteRequested.emit(self.file_path)
    
    def generateSoundKey(self, file_name):
        """根据文件名生成soundKey"""
        from utils.main import cnTextToPinyinFirst, enTextToFirst
        import re
        
        # 判断是否为中文（包含至少一个中文字符）
        if re.search(r'[\u4e00-\u9fa5]', file_name):
            # 中文处理
            sound_key = cnTextToPinyinFirst(file_name)
        else:
            # 英文处理
            sound_key = enTextToFirst(file_name)
        
        # 确保soundKey符合规范：最长5个字符，只包含小写英文字母和数字，数字不能在开头
        sound_key = sound_key.lower()[:5]  # 截取前5个字符并转为小写
        
        # 过滤非法字符，只保留小写字母和数字
        sound_key = ''.join(c for c in sound_key if c.islower() or c.isdigit())
        
        # 如果首字符是数字，添加字母前缀
        if sound_key and sound_key[0].isdigit():
            sound_key = 's' + sound_key[:-1]  # 添加's'前缀并保持总长度不超过5
        
        # 如果为空，使用默认值
        if not sound_key:
            sound_key = "sound"
        
        return sound_key
    
    def onSoundKeyChanged(self, text):
        """soundKey变更事件"""
        # 验证输入是否符合规范：只包含小写英文字母和数字，数字不能在开头
        valid_text = ''
        for c in text.lower():
            if c.islower() or c.isdigit():
                valid_text += c
        
        # 如果首字符是数字，不添加到有效文本中
        if valid_text and valid_text[0].isdigit():
            valid_text = valid_text[1:]
            # 如果删除数字后为空，不更新
            if not valid_text:
                self.soundKeyEdit.setText(self.soundKey)
                return
        
        # 如果有效文本与当前文本不同，更新文本框
        if valid_text != text:
            self.soundKeyEdit.setText(valid_text)
            return
        
        # 更新soundKey并发送信号
        self.soundKey = valid_text
        self.soundKeyChanged.emit(self.file_path, self.soundKey)
    
    def onCategoryChanged(self, category):
        """分类变更事件"""
        if category == "无分类":
            category = ""
        # 发送分类变更信号
        self.categoryChanged.emit(self.file_path, category)
    
    def updateCategories(self, categories):
        """更新分类列表"""
        current_category = self.categoryComboBox.currentText()
        
        # 清空并重新添加选项
        self.categoryComboBox.clear()
        self.categoryComboBox.addItem("无分类")
        
        # 添加分类选项
        if categories:
            for category in categories:
                self.categoryComboBox.addItem(category)
        
        # 尝试恢复之前的选择
        index = self.categoryComboBox.findText(current_category)
        if index >= 0:
            self.categoryComboBox.setCurrentIndex(index)
        else:
            self.categoryComboBox.setCurrentIndex(0)  # 默认选择"无分类"

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
        self.listTitleLayout.setSpacing(20)  # 增加间距
        
        # 创建列表标题
        self.listTitleLabel = MinecraftLabel("已添加的音频文件")
        self.listTitleLabel.setMinimumWidth(500)  # 设置最小宽度，使标题更宽
        self.listTitleLabel.setFixedWidth(500)  # 设置固定宽度，确保宽度生效
        self.listTitleLabel.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #FFFFFF;
                padding: 5px;
            }
        """)
        self.listTitleLayout.addWidget(self.listTitleLabel, 0, Qt.AlignLeft)
        
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
        
        # 加载分类列表
        self.loadCategories()
        
        # 检查 sounds.json 文件是否存在，如果不存在则创建
        sounds_json_path = self.current_project_path.cacheConfig()
        if not os.path.exists(sounds_json_path):
            # 只在文件不存在时才更新 sounds.json
            self.updateSoundsJsonFromCache()
        
        # 先尝试从sounds.json加载音频信息
        if not self.loadAudioInfoFromJson():
            # 如果没有sounds.json或加载失败，则从缓存目录加载音频文件
            self.loadCachedAudioFiles()
    
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
        cache_dir = self.current_project_path.cacheSrc()
        
        # 确保缓存文件夹存在
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, mode=0o755)  # 设置读写权限
        
        for file_path in file_paths:
            # 检查文件是否已存在
            if file_path in self.audioFiles:
                duplicate_files.append(os.path.basename(file_path))
                continue
            
            # 复制文件到缓存文件夹
            try:
                copyFile(file_path, cache_dir)
                
                # 获取文件名
                file_name = os.path.basename(file_path)
                # 构建缓存文件路径
                cache_file_path = os.path.join(cache_dir, file_name)
                
                # 添加缓存文件路径到列表（而不是原始文件路径）
                self.audioFiles.append(cache_file_path)
                added_count += 1
                
                # 创建列表项
                item = QListWidgetItem()
                self.audioList.addItem(item)
                
                # 创建自定义小部件（使用缓存文件路径）
                widget = AudioListItem(cache_file_path, categories=self.categories)
                widget.deleteRequested.connect(self.onDeleteAudio)
                widget.categoryChanged.connect(self.onAudioCategoryChanged)
                widget.soundKeyChanged.connect(self.onAudioSoundKeyChanged)
                
                # 设置列表项大小和小部件
                item.setSizeHint(widget.sizeHint())
                self.audioList.setItemWidget(item, widget)
            except Exception as e:
                copy_failed_files.append(f"{os.path.basename(file_path)} (错误: {str(e)})")
        
        # 如果成功添加了文件，保存音频信息到JSON
        if added_count > 0:
            self.saveAudioInfoToJson()
            
            # 显示添加结果
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
                # 删除缓存目录中的对应文件
                if self.current_project_path:
                    # 获取文件名
                    file_name = os.path.basename(file_path)
                    
                    # 检查文件是否在缓存根目录
                    cache_root = self.current_project_path.cache()
                    cache_file_path = os.path.join(cache_root, file_name)
                    if os.path.exists(cache_file_path):
                        delFile(cache_file_path)
                    
                    # 检查文件是否在缓存源文件目录
                    cache_src = self.current_project_path.cacheSrc()
                    cache_src_file_path = os.path.join(cache_src, file_name)
                    if os.path.exists(cache_src_file_path):
                        delFile(cache_src_file_path)
                    
                    # 检查文件是否在分类子文件夹中
                    for category in self.categories:
                        category_dir = self.current_project_path.cacheSrcF(category)
                        category_file_path = os.path.join(category_dir, file_name)
                        if os.path.exists(category_file_path):
                            delFile(category_file_path)
                            break
                
                self.audioFiles.remove(file_path)
                self.audioList.takeItem(index)
                
                # 保存音频信息到JSON文件
                self.saveAudioInfoToJson()
                
                MinecraftMessageBox.show_message(
                    self,
                    "删除成功",
                    f"已成功从列表中移除 {os.path.basename(file_path)}"
                )
            except Exception as e:
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
    
    # 导出页面切换信号
    switchToExportPage = pyqtSignal(object, list)
    
    def onExport(self):
        """导出按钮点击事件"""
        if not self.audioFiles:
            MinecraftMessageBox.show_warning(
                self,
                "无法导出",
                "请先添加音频文件"
            )
            return
        
        # 发送切换到导出页面的信号，传递项目路径和音频文件列表
        self.switchToExportPage.emit(self.current_project_path, self.audioFiles)
    
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

                createFolder(self.current_project_path.cacheSrcF(category_name))
                
                # 更新删除分类按钮状态
                self.updateDeleteCategoryButtonState()
                
                # 更新所有音频项的分类下拉框
                self.updateAllAudioItemCategories()
                
                # 保存音频信息到JSON文件
                self.saveAudioInfoToJson()
                
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
        
    def saveAudioInfoToJson(self):
        from utils import updateJsonFile, createJsonFile
        """保存音频信息到sounds.json文件"""
        if not self.current_project_path:
            return
        
        import json
        
        # sounds.json 文件路径
        sounds_json_path = self.current_project_path.cacheConfig()
        
        # 读取现有的 sounds.json 文件（如果存在）
        existing_audio_info = {}
        if os.path.exists(sounds_json_path):
            try:
                with open(sounds_json_path, 'r', encoding='utf-8') as f:
                    existing_audio_info = json.load(f)
            except Exception as e:
                print(f"读取 sounds.json 文件失败: {str(e)}")
        
        # 创建音频信息字典
        audio_info = {}
        
        # 获取当前列表中的所有文件名
        current_file_names = []
        
        # 遍历所有列表项，获取音频信息
        for i in range(self.audioList.count()):
            item = self.audioList.item(i)
            widget = self.audioList.itemWidget(item)
            if isinstance(widget, AudioListItem):
                file_path = widget.file_path  # 这是当前实际的文件路径
                file_name = os.path.basename(file_path)
                current_file_names.append(file_name)
                
                # 获取当前分类
                category = widget.categoryComboBox.currentText()
                if category == "无分类":
                    category = ""
                
                # 确保cache_path与实际文件路径一致
                actual_cache_path = file_path
                
                # 获取soundKey
                sound_key = widget.soundKey
                
                # 只保留名称对应的分类、soundkey和cache_path
                audio_info[file_name] = {
                    "category": category,
                    "sound_key": sound_key,
                    "cache_path": actual_cache_path
                }
        
        # 保留不在当前列表中的音频文件信息，但只保留必要字段
        for file_name, info in existing_audio_info.items():
            if file_name not in current_file_names:
                # 只保留必要字段
                audio_info[file_name] = {
                    "category": info.get("category", ""),
                    "sound_key": info.get("sound_key", ""),
                    "cache_path": info.get("cache_path", "")
                }
        
        # 保存到sounds.json文件
        try:
            # 检查文件是否存在
            if not os.path.exists(sounds_json_path):
                createJsonFile(sounds_json_path)
            updateJsonFile(sounds_json_path, audio_info)
            return True
        except Exception as e:
            print(f"保存音频信息失败: {str(e)}")
            return False
    
    def loadAudioInfoFromJson(self):
        """从sounds.json文件加载音频信息"""
        if not self.current_project_path:
            return False
        
        import json
        
        # sounds.json文件路径
        sounds_json_path = self.current_project_path.cacheConfig()
        
        # 检查文件是否存在
        if not os.path.exists(sounds_json_path):
            print(f"sounds.json文件不存在: {sounds_json_path}")
            return False
        
        try:
            # 读取sounds.json文件
            with open(sounds_json_path, 'r', encoding='utf-8') as f:
                audio_info = json.load(f)
            
            # 获取缓存文件夹路径
            cache_dir = self.current_project_path.cacheSrc()
            
            # 确保缓存文件夹存在
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir, mode=0o755)  # 设置读写权限
            
            # 加载音频文件
            for file_name, info in audio_info.items():
                # 构建缓存文件路径
                cache_file_path = os.path.join(cache_dir, file_name)
                
                # 检查缓存文件是否存在
                if not os.path.exists(cache_file_path):
                    # 检查cache_path是否存在
                    cache_path = info.get("cache_path", "")
                    if cache_path and os.path.exists(cache_path) and cache_path != cache_file_path:
                        try:
                            copyFile(cache_path, cache_dir)
                        except Exception as e:
                            print(f"复制文件失败: {str(e)}")
                            continue
                    else:
                        print(f"缓存文件不存在且无法从cache_path复制: {file_name}")
                        continue
                
                # 检查文件是否已存在于列表中
                if cache_file_path not in self.audioFiles:
                    # 添加文件到列表
                    self.audioFiles.append(cache_file_path)
                    
                    # 创建列表项
                    item = QListWidgetItem()
                    self.audioList.addItem(item)
                    
                    # 创建自定义小部件
                    widget = AudioListItem(cache_file_path, categories=self.categories)
                    widget.deleteRequested.connect(self.onDeleteAudio)
                    widget.categoryChanged.connect(self.onAudioCategoryChanged)
                    widget.soundKeyChanged.connect(self.onAudioSoundKeyChanged)
                    
                    # 设置soundKey
                    sound_key = info.get("sound_key", "")
                    if sound_key:
                        widget.soundKeyEdit.setText(sound_key)
                    
                    # 设置分类
                    category = info.get("category", "")
                    if category:
                        index = widget.categoryComboBox.findText(category)
                        if index >= 0:
                            widget.categoryComboBox.setCurrentIndex(index)
                    
                    # 设置列表项大小和小部件
                    item.setSizeHint(widget.sizeHint())
                    self.audioList.setItemWidget(item, widget)
            
            print(f"已从sounds.json加载音频信息")
            return True
        except Exception as e:
            print(f"加载音频信息失败: {str(e)}")
            return False
    
    def onAudioCategoryChanged(self, file_path, category):
        """处理音频分类变更
        
        将音频文件从原分类移动到新分类文件夹。
        如果选择"无分类"，则移动到根目录。
        
        Args:
            file_path: 音频文件路径
            category: 目标分类名称，"无分类"表示移动到根目录
        """
        from utils import copyFile, delFile
        
        try:
            # 获取文件名
            file_name = os.path.basename(file_path)
            
            # 确定目标路径
            if category == "无分类":
                # 移动到根目录
                target_dir = self.current_project_path.cacheSrc()
                target_path = os.path.join(target_dir, file_name)
                print(f"音频文件 {file_name} 已从分类中移除")
            else:
                # 移动到分类目录
                target_dir = self.current_project_path.cacheSrcF(category)
                target_path = os.path.join(target_dir, file_name)
                print(f"音频文件 {file_name} 已移动到分类 {category}")
            
            # 确保目标目录存在
            if not os.path.exists(target_dir):
                os.makedirs(target_dir, mode=0o755)  # 设置读写权限
            
            # 使用复制后删除的方式实现剪切粘贴
            copyFile(file_path, target_path)
            delFile(file_path)
            
            # 更新文件路径在列表中的引用
            for i, audio_path in enumerate(self.audioFiles):
                if audio_path == file_path:
                    self.audioFiles[i] = target_path
                    break
            
            # 更新列表项中的文件路径
            for i in range(self.audioList.count()):
                item = self.audioList.item(i)
                widget = self.audioList.itemWidget(item)
                if isinstance(widget, AudioListItem) and widget.file_path == file_path:
                    widget.file_path = target_path
                    break
                    
            print(f"音频文件 {file_name} 的分类已更改为: {category if category else '无分类'}")
            
            # 保存音频信息到JSON文件
            self.saveAudioInfoToJson()
            
            return target_path
        except Exception as e:
            print(f"分类更改失败: {str(e)}")
            return None
    
    def onAudioSoundKeyChanged(self, file_path, sound_key):
        """音频soundKey变更事件"""
        # 处理音频文件soundKey变更
        print(f"音频文件 {os.path.basename(file_path)} 的soundKey已更改为: {sound_key}")
        
        # 保存音频信息到JSON文件
        self.saveAudioInfoToJson()
    
    def updateAllAudioItemCategories(self):
        """更新所有音频项的分类下拉框"""
        # 遍历所有列表项，更新分类下拉框
        for i in range(self.audioList.count()):
            item = self.audioList.item(i)
            widget = self.audioList.itemWidget(item)
            if isinstance(widget, AudioListItem):
                widget.updateCategories(self.categories)
    
    def loadCategories(self):
        """加载项目中的分类列表"""
        if not self.current_project_path:
            return
        
        # 清空当前分类列表
        self.categories = []
        
        # 获取sounds目录下的所有文件夹作为分类
        sounds_dir = self.current_project_path.cacheSrc()
        if os.path.exists(sounds_dir):
            self.categories = getFolderList(sounds_dir)
        
        # 更新删除分类按钮状态
        self.updateDeleteCategoryButtonState()
    
    def updateSoundsJsonFromCache(self, force_update=False):
        """检查缓存目录中的音频文件，并更新 sounds.json 文件
        
        Args:
            force_update: 是否强制更新文件，即使文件已存在
        """
        if not self.current_project_path:
            return
        
        import json
        from utils import updateJsonFile, createJsonFile
        
        # 获取缓存文件夹路径
        cache_dir = self.current_project_path.cacheSrc()
        
        # 确保缓存文件夹存在
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, mode=0o755)  # 设置读写权限
            return
        
        # sounds.json 文件路径
        sounds_json_path = self.current_project_path.cacheConfig()
        
        # 如果文件已存在且不强制更新，则直接返回
        if os.path.exists(sounds_json_path) and not force_update:
            return
        
        # 读取现有的 sounds.json 文件（如果存在）
        existing_audio_info = {}
        if os.path.exists(sounds_json_path):
            try:
                with open(sounds_json_path, 'r', encoding='utf-8') as f:
                    existing_audio_info = json.load(f)
            except Exception as e:
                print(f"读取 sounds.json 文件失败: {str(e)}")
        
        # 获取缓存目录中的所有音频文件
        audio_files = getFileList(cache_dir)
        
        # 检查分类目录中的音频文件
        for category in self.categories:
            category_dir = self.current_project_path.cacheSrcF(category)
            if os.path.exists(category_dir):
                category_files = getFileList(category_dir)
                for file_name in category_files:
                    if file_name not in audio_files:
                        audio_files.append(file_name)
        
        # 创建更新后的音频信息字典
        updated_audio_info = {}
        
        # 过滤出音频文件并更新信息
        valid_extensions = [".ogg", ".wav", ".mp3", ".flac"]
        for file_name in audio_files:
            _, ext = os.path.splitext(file_name)
            if ext.lower() in valid_extensions:
                # 检查文件是否在现有的 sounds.json 中
                if file_name in existing_audio_info:
                    # 保留现有信息
                    updated_audio_info[file_name] = existing_audio_info[file_name]
                else:
                    # 为新文件创建默认信息
                    file_path = os.path.join(cache_dir, file_name)
                    updated_audio_info[file_name] = {
                        "name": file_name,
                        "sound_key": os.path.splitext(file_name)[0],  # 默认使用文件名作为 sound_key
                        "category": "",  # 默认无分类
                        "original_suffix": ext,
                        "original_path": file_path,
                        "cache_path": file_path
                    }
        
        # 保存更新后的音频信息到 sounds.json 文件
        try:
            # 检查文件是否存在
            if not os.path.exists(sounds_json_path):
                createJsonFile(sounds_json_path)
            updateJsonFile(sounds_json_path, updated_audio_info)
            print(f"已更新 sounds.json 文件")
        except Exception as e:
            print(f"更新 sounds.json 文件失败: {str(e)}")
    
    def loadCachedAudioFiles(self):
        """从缓存目录加载音频文件"""
        if not self.current_project_path:
            return
        
        # 获取缓存文件夹路径
        cache_dir = self.current_project_path.cacheSrc()
        
        # 确保缓存文件夹存在
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, mode=0o755)  # 设置读写权限
            return
        
        # 获取缓存目录中的所有音频文件
        audio_files = getFileList(cache_dir)
        
        # 过滤出音频文件
        valid_extensions = [".ogg", ".wav", ".mp3", ".flac"]
        for file_name in audio_files:
            _, ext = os.path.splitext(file_name)
            if ext.lower() in valid_extensions:
                file_path = os.path.join(cache_dir, file_name)
                
                # 检查文件是否已存在于列表中
                if file_path not in self.audioFiles:
                    # 添加文件到列表
                    self.audioFiles.append(file_path)
                    
                    # 创建列表项
                    item = QListWidgetItem()
                    self.audioList.addItem(item)
                    
                    # 创建自定义小部件
                    widget = AudioListItem(file_path, categories=self.categories)
                    widget.deleteRequested.connect(self.onDeleteAudio)
                    widget.categoryChanged.connect(self.onAudioCategoryChanged)
                    widget.soundKeyChanged.connect(self.onAudioSoundKeyChanged)
                    
                    # 设置列表项大小和小部件
                    item.setSizeHint(widget.sizeHint())
                    self.audioList.setItemWidget(item, widget)
    
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
                        delFolder(self.current_project_path.cacheSrcF(category))
                        self.categories.remove(category)
                
                # 更新删除分类按钮状态
                self.updateDeleteCategoryButtonState()
                
                # 更新所有音频项的分类下拉框
                self.updateAllAudioItemCategories()
                
                # 保存音频信息到JSON文件
                self.saveAudioInfoToJson()
                
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