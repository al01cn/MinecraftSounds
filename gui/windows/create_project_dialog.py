from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QTextEdit, QPushButton, QFileDialog, QComboBox)
from PIL import Image
import json
import os
from utils import mcver_path, getVersionToPack_format
from gui.ui import MinecraftFrame, MinecraftTitleLabel, MinecraftLabel, apply_minecraft_style
from gui.ui.button import MinecraftPixelButton
from gui.ui.minecraft_dialog import MinecraftMessageBox, MinecraftMessageBoxResult

# 定义通用的Minecraft风格输入控件样式
MINECRAFT_INPUT_STYLE = """
    background-color: #373737;
    color: #FFFFFF;
    border: 2px solid #1F1F1F;
    border-radius: 2px;
    padding: 4px;
    font-family: 'Courier New';
"""

MINECRAFT_INPUT_FOCUS_STYLE = """
    border: 2px solid #5A5A5A;
"""

MINECRAFT_COMBOBOX_STYLE = """
    QComboBox {
        background-color: #373737;
        color: #FFFFFF;
        border: 2px solid #1F1F1F;
        border-radius: 2px;
        padding: 4px;
        font-family: 'Courier New';
    }
    QComboBox:hover {
        border: 2px solid #5A5A5A;
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left: 1px solid #1F1F1F;
        background-color: #4A4A4A;
    }
    QComboBox::down-arrow {
        image: none;
        width: 10px;
        height: 10px;
        background-color: #AAAAAA;
    }
    QComboBox QAbstractItemView {
        background-color: #373737;
        color: #FFFFFF;
        selection-background-color: #4A4A4A;
        selection-color: #FFFFFF;
        border: 2px solid #1F1F1F;
    }
"""

class CreateProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("创建新项目")
        self.setMinimumSize(500, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.pack_format = 1
        self.key_error = False  # 添加主键错误标志
        
        # 应用我的世界风格
        apply_minecraft_style(self)
        
        # 创建主布局
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(15)
        
        # 创建标题
        self.titleLabel = MinecraftTitleLabel("创建新项目")
        self.mainLayout.addWidget(self.titleLabel, 0, Qt.AlignCenter)
        
        # 创建表单框架
        self.formFrame = MinecraftFrame(frame_type="stone")
        self.formLayout = QVBoxLayout(self.formFrame)
        self.formLayout.setContentsMargins(15, 15, 15, 15)
        self.formLayout.setSpacing(10)
        
        # 音乐包名称
        self.nameContainer = QVBoxLayout()
        self.nameLayout = QHBoxLayout()
        self.nameLabel = MinecraftLabel("音乐包名称")
        self.nameEdit = QLineEdit()
        self.nameEdit.setMaxLength(10)  # 限制最多10个字
        self.nameEdit.setStyleSheet(f"QLineEdit {{{MINECRAFT_INPUT_STYLE}}} QLineEdit:focus {{{MINECRAFT_INPUT_FOCUS_STYLE}}}")
        self.nameLayout.addWidget(self.nameLabel)
        self.nameLayout.addWidget(self.nameEdit)
        self.nameContainer.addLayout(self.nameLayout)
        
        # 音乐包名称错误提示
        self.nameErrorLabel = QLabel()
        self.nameErrorLabel.setStyleSheet("color: #FF5555; font-size: 10px; margin-top: 2px;")
        self.nameErrorLabel.setVisible(False)
        self.nameContainer.addWidget(self.nameErrorLabel)
        self.formLayout.addLayout(self.nameContainer)
        
        # 音乐包简介
        self.descLayout = QHBoxLayout()
        self.descLabel = MinecraftLabel("音乐包简介")
        self.descEdit = QLineEdit()
        self.descEdit.setMaxLength(10)  # 限制最多10个字
        self.descEdit.setStyleSheet(f"QLineEdit {{{MINECRAFT_INPUT_STYLE}}} QLineEdit:focus {{{MINECRAFT_INPUT_FOCUS_STYLE}}}")
        self.descLayout.addWidget(self.descLabel)
        self.descLayout.addWidget(self.descEdit)
        self.formLayout.addLayout(self.descLayout)
        
        # 音乐包图标
        self.iconLayout = QHBoxLayout()
        self.iconLabel = MinecraftLabel("音乐包图标")
        self.iconPathLabel = MinecraftLabel("未选择图标")
        self.iconButton = MinecraftPixelButton("选择图标", button_type="brown")
        self.iconButton.clicked.connect(self.selectIcon)
        self.iconLayout.addWidget(self.iconLabel)
        self.iconLayout.addWidget(self.iconPathLabel, 1)  # 1表示拉伸因子
        self.iconLayout.addWidget(self.iconButton)
        self.formLayout.addLayout(self.iconLayout)
        
        # 游戏版本
        self.versionContainer = QVBoxLayout()
        self.versionLayout = QHBoxLayout()
        self.versionLabel = MinecraftLabel("游戏版本")
        self.versionCombo = QComboBox()
        self.versionCombo.setStyleSheet(MINECRAFT_COMBOBOX_STYLE)
        self.loadVersions()  # 加载版本信息
        self.versionLayout.addWidget(self.versionLabel)
        self.versionLayout.addWidget(self.versionCombo)
        self.versionContainer.addLayout(self.versionLayout)
        
        # 游戏版本错误提示
        self.versionErrorLabel = QLabel()
        self.versionErrorLabel.setStyleSheet("color: #FF5555; font-size: 10px; margin-top: 2px;")
        self.versionErrorLabel.setVisible(False)
        self.versionContainer.addWidget(self.versionErrorLabel)
        self.formLayout.addLayout(self.versionContainer)
        
        # 主键
        self.keyContainer = QVBoxLayout()
        self.keyLayout = QHBoxLayout()
        self.keyLabel = MinecraftLabel("主键")
        self.keyEdit = QLineEdit("mcsd")  # 默认值为mcsd
        self.keyEdit.setStyleSheet(f"QLineEdit {{{MINECRAFT_INPUT_STYLE}}} QLineEdit:focus {{{MINECRAFT_INPUT_FOCUS_STYLE}}}")
        self.keyLayout.addWidget(self.keyLabel)
        self.keyLayout.addWidget(self.keyEdit)
        self.keyContainer.addLayout(self.keyLayout)
        
        # 主键错误提示
        self.keyErrorLabel = QLabel()
        self.keyErrorLabel.setStyleSheet("color: #FF5555; font-size: 10px; margin-top: 2px;")
        self.keyErrorLabel.setVisible(False)
        self.keyContainer.addWidget(self.keyErrorLabel)
        self.formLayout.addLayout(self.keyContainer)
        
        # 添加表单框架到主布局
        self.mainLayout.addWidget(self.formFrame)
        
        # 创建按钮布局
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setContentsMargins(0, 10, 0, 0)
        self.buttonLayout.setSpacing(10)
        
        # 创建确认和取消按钮
        self.confirmButton = MinecraftPixelButton("确认", button_type="green")
        self.confirmButton.clicked.connect(self.accept)
        self.cancelButton = MinecraftPixelButton("取消", button_type="brown")
        self.cancelButton.clicked.connect(self.reject)
        
        # 添加按钮到布局
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.confirmButton)
        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.addStretch(1)
        
        # 添加按钮布局到主布局
        self.mainLayout.addLayout(self.buttonLayout)
        
        # 初始化变量
        self.iconPath = ""
        
        # 连接信号和槽
        self.nameEdit.textChanged.connect(self.onNameChanged)
        self.versionCombo.currentIndexChanged.connect(self.onVersionChanged)
        self.keyEdit.textChanged.connect(self.onKeyChanged)
    
    def loadVersions(self):
        """加载游戏版本信息"""
        try:
            # 读取mc.ver文件
            with open(mcver_path, 'r', encoding='utf-8') as f:
                versions = json.load(f)
            
            # 添加版本到下拉框
            for version_info in versions:
                self.versionCombo.addItem(f"{version_info['version']}")
        except Exception as e:
            print(f"加载版本信息失败: {e}")
            # 添加一个默认版本
            self.versionCombo.addItem(versions[0]['version'])
    
    def selectIcon(self):
        """选择音乐包图标"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择音乐包图标", "", "图片文件 (*.png)"
        )
        if file_path:
            # 检查图片尺寸和比例
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    # 检查是否为1:1比例且尺寸小于等于256x256
                    if width != height or width > 256:
                        # 显示提示信息
                        MinecraftMessageBox.show_warning(
                            self,
                            "图片不符合要求",
                            "图片必须是1:1比例且不大于256x256像素。\n\n请使用其他工具裁剪图片后再选择，或者选择其他符合要求的图片。"
                        )
                        return
                    else:
                        # 图片符合要求，直接使用
                        self.iconPath = file_path
                        self.iconPathLabel.setText(os.path.basename(file_path))
            except Exception as e:
                print(f"检查图片失败: {e}")
                MinecraftMessageBox.show_warning(
                    self,
                    "图片检查失败",
                    f"无法检查图片格式: {e}\n\n请确保选择有效的PNG图片文件。"
                )
    
    def clearErrors(self):
        """清除所有错误提示"""
        self.nameErrorLabel.setText("")
        self.nameErrorLabel.setVisible(False)
        self.versionErrorLabel.setText("")
        self.versionErrorLabel.setVisible(False)
        self.keyErrorLabel.setText("")
        self.keyErrorLabel.setVisible(False)
    
    def onNameChanged(self, text):
        """音乐包名称输入变化时清除错误提示"""
        self.nameErrorLabel.setVisible(False)
    
    def onVersionChanged(self, index):
        """游戏版本选择变化时清除错误提示"""
        self.versionErrorLabel.setVisible(False)
    
    def onKeyChanged(self, text):
        """主键输入变化时清除错误提示"""
        self.keyErrorLabel.setVisible(False)
    
    def accept(self):
        """确认创建项目"""
        # 清除之前的错误提示
        self.clearErrors()
        
        # 验证标志
        valid = True
        
        # 验证输入 - 音乐包名称
        if not self.nameEdit.text().strip():
            self.nameErrorLabel.setText("请输入音乐包名称")
            self.nameErrorLabel.setVisible(True)
            valid = False
        
        # 验证输入 - 游戏版本
        if self.versionCombo.currentIndex() == -1 or not self.versionCombo.currentText():
            self.versionErrorLabel.setText("请选择游戏版本")
            self.versionErrorLabel.setVisible(True)
            valid = False
            
        # 验证输入 - 主键
        if not self.keyEdit.text().strip():
            self.keyErrorLabel.setText("请输入主键")
            self.keyErrorLabel.setVisible(True)
            valid = False
        
        # 如果验证不通过，直接返回
        if not valid:
            return
        
        # 显示确认对话框
        result = MinecraftMessageBox.show_confirmation(
            self,
            "确认创建",
            f"确定要创建音乐包 '{self.nameEdit.text()}' 吗？\n游戏版本: {self.versionCombo.currentText()}\n主键: {self.keyEdit.text()}",
            "创建",
            "取消"
        )
        
        if result == MinecraftMessageBoxResult.ok:
            super().accept()
            print("创建项目")
        # 如果用户选择取消，则不关闭对话框
    
    def getProjectInfo(self):
        """获取项目信息"""
        # 从版本字符串中提取pack_format
        version_text = self.versionCombo.currentText()
        self.pack_format = getVersionToPack_format(version_text)

        
        return {
            "name": self.nameEdit.text(),
            "description": self.descEdit.text(),
            "icon_path": self.iconPath,
            "version": self.versionCombo.currentText(),
            "pack_format": self.pack_format,
            "sound_main_key": self.keyEdit.text()  # 添加主键
        }