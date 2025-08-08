from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtGui import QIcon
from enum import Enum

# 定义消息框结果枚举
class MinecraftMessageBoxResult(Enum):
    """消息框结果枚举"""
    ok = 1      # 确定/是
    cancel = 0  # 取消/否
    yes = 1     # 是（同ok）
    no = 0      # 否（同cancel）

from .minecraft_style import get_minecraft_font, MC_COLORS, MinecraftFrame
from .button import MinecraftPixelButton

class MinecraftMessageBox(QDialog):
    """
    我的世界风格的消息弹窗
    """
    def __init__(self, parent=None, title="消息", text="", icon_type="info", buttons=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(400)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {MC_COLORS['dark_gray']};
                border: 2px solid {MC_COLORS['stone_gray']};
            }}
        """)
        
        # 创建主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(10)
        
        # 创建标题
        self.title_label = QLabel(title)
        self.title_label.setFont(get_minecraft_font(14, True))
        self.title_label.setStyleSheet(f"color: {MC_COLORS['text_yellow']};")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)
        
        # 创建分隔线
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setStyleSheet(f"background-color: {MC_COLORS['stone_gray']};")
        self.separator.setFixedHeight(2)
        self.main_layout.addWidget(self.separator)
        
        # 创建内容区域
        self.content_frame = MinecraftFrame()
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建消息文本
        self.message_label = QLabel(text)
        self.message_label.setFont(get_minecraft_font(11))
        self.message_label.setStyleSheet(f"color: {MC_COLORS['white']};")
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.content_layout.addWidget(self.message_label)
        
        self.main_layout.addWidget(self.content_frame)
        
        # 创建按钮区域
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(10)
        
        # 默认按钮
        if buttons is None:
            buttons = ["确定"]
        
        # 添加按钮
        self.buttons = {}
        for button_text in buttons:
            button = MinecraftPixelButton(button_text)
            button.clicked.connect(lambda checked, text=button_text: self.button_clicked(text))
            self.button_layout.addWidget(button)
            self.buttons[button_text] = button
        
        self.main_layout.addLayout(self.button_layout)
        
        # 设置默认按钮
        if "确定" in self.buttons:
            self.buttons["确定"].setDefault(True)
        elif buttons:
            self.buttons[buttons[0]].setDefault(True)
        
        self.result_button = None
    
    def button_clicked(self, button_text):
        self.result_button = button_text
        self.accept()
    
    @staticmethod
    def show_message(parent=None, title="消息", text="", icon_type="info"):
        """
        显示一个消息弹窗
        """
        dialog = MinecraftMessageBox(parent, title, text, icon_type)
        dialog.exec_()
    
    @staticmethod
    def show_warning(parent=None, title="警告", text=""):
        """
        显示一个警告弹窗
        """
        dialog = MinecraftMessageBox(parent, title, text, "warning")
        dialog.exec_()
    
    @staticmethod
    def show_error(parent=None, title="错误", text=""):
        """
        显示一个错误弹窗
        """
        dialog = MinecraftMessageBox(parent, title, text, "error")
        dialog.exec_()
    
    @staticmethod
    def show_confirmation(parent=None, title="确认", text="", yes_text="是", no_text="否"):
        """
        显示一个确认弹窗，返回MinecraftMessageBoxResult枚举值
        """
        dialog = MinecraftMessageBox(parent, title, text, "question", [yes_text, no_text])
        dialog.exec_()
        
        # 根据按钮文本返回对应的枚举值
        if dialog.result_button == yes_text:
            return MinecraftMessageBoxResult.ok
        else:
            return MinecraftMessageBoxResult.cancel