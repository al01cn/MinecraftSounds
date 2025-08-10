from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit
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


class MinecraftInputDialog(QDialog):
    """
    我的世界风格的输入弹窗
    """
    def __init__(self, parent=None, title="输入", prompt="请输入：", default_text=""):
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
        
        # 创建提示文本
        self.prompt_label = QLabel(prompt)
        self.prompt_label.setFont(get_minecraft_font(11))
        self.prompt_label.setStyleSheet(f"color: {MC_COLORS['white']};")
        self.prompt_label.setWordWrap(True)
        self.prompt_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.content_layout.addWidget(self.prompt_label)
        
        # 创建输入框
        self.input_field = QLineEdit(default_text)
        self.input_field.setFont(get_minecraft_font(11))
        self.input_field.setStyleSheet(f"""
            QLineEdit {{
                background-color: {MC_COLORS['black']};
                color: {MC_COLORS['white']};
                border: 2px solid {MC_COLORS['stone_gray']};
                padding: 5px;
                selection-background-color: {MC_COLORS['light_blue']};
            }}
            QLineEdit:focus {{
                border: 2px solid {MC_COLORS['light_blue']};
            }}
        """)
        self.content_layout.addWidget(self.input_field)
        
        self.main_layout.addWidget(self.content_frame)
        
        # 创建按钮区域
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(10)
        
        # 添加确定和取消按钮
        self.ok_button = MinecraftPixelButton("确定", button_type="green")
        self.ok_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.ok_button)
        
        self.cancel_button = MinecraftPixelButton("取消", button_type="red")
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.cancel_button)
        
        self.main_layout.addLayout(self.button_layout)
        
        # 设置默认按钮
        self.ok_button.setDefault(True)
        
        # 设置焦点到输入框
        self.input_field.setFocus()
    
    def get_input_text(self):
        """
        获取输入框中的文本
        """
        return self.input_field.text()
    
    def exec_(self):
        """
        显示对话框并返回结果
        """
        result = super().exec_()
        if result:
            return MinecraftMessageBoxResult.ok
        else:
            return MinecraftMessageBoxResult.cancel


class MinecraftCheckboxDialog(QDialog):
    """
    我的世界风格的多选框弹窗
    """
    def __init__(self, parent=None, title="选择", prompt="请选择：", items=None):
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
        
        # 初始化选项列表
        self.items = items or []
        self.checkboxes = []
        
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
        
        # 创建提示文本
        self.prompt_label = QLabel(prompt)
        self.prompt_label.setFont(get_minecraft_font(11))
        self.prompt_label.setStyleSheet(f"color: {MC_COLORS['white']};")
        self.prompt_label.setWordWrap(True)
        self.prompt_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.content_layout.addWidget(self.prompt_label)
        
        # 导入复选框组件
        from PyQt5.QtWidgets import QCheckBox
        
        # 创建复选框
        for item in self.items:
            checkbox = QCheckBox(item)
            checkbox.setFont(get_minecraft_font(10))
            checkbox.setStyleSheet(f"""
                QCheckBox {{
                    color: {MC_COLORS['white']};
                    spacing: 5px;
                }}
                QCheckBox::indicator {{
                    width: 16px;
                    height: 16px;
                    border: 2px solid {MC_COLORS['stone_gray']};
                    background-color: {MC_COLORS['black']};
                }}
                QCheckBox::indicator:checked {{
                    background-color: {MC_COLORS['grass_green']};
                }}
                QCheckBox::indicator:unchecked:hover {{
                    border: 2px solid {MC_COLORS['light_blue']};
                }}
            """)
            self.content_layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)
        
        self.main_layout.addWidget(self.content_frame)
        
        # 创建按钮区域
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(10)
        
        # 添加确定和取消按钮
        self.ok_button = MinecraftPixelButton("确定", button_type="green")
        self.ok_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.ok_button)
        
        self.cancel_button = MinecraftPixelButton("取消", button_type="red")
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.cancel_button)
        
        self.main_layout.addLayout(self.button_layout)
        
        # 设置默认按钮
        self.ok_button.setDefault(True)
    
    def get_selected_items(self):
        """
        获取选中的项目列表
        """
        selected_items = []
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.isChecked():
                selected_items.append(self.items[i])
        return selected_items
    
    def exec_(self):
        """
        显示对话框并返回结果
        """
        result = super().exec_()
        if result:
            return MinecraftMessageBoxResult.ok
        else:
            return MinecraftMessageBoxResult.cancel