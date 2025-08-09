from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget
from PyQt5.QtGui import QCursor
import os
from utils import GetIconSvg

class IconLabel(QWidget):
    """
    一个包含图标和标签的组件，用于在UI中显示带有图标的标签
    图标支持鼠标悬停提示功能
    """
    
    def __init__(self, label_text, icon_name, tooltip_text="", parent=None):
        """
        初始化IconLabel组件
        
        参数:
            label_text (str): 标签文本
            icon_name (str): 图标名称（不包含扩展名）
            tooltip_text (str): 鼠标悬停提示文本
            parent: 父组件
        """
        super().__init__(parent)
        self.initUI(label_text, icon_name, tooltip_text)
    
    def initUI(self, label_text, icon_name, tooltip_text):
        """
        初始化UI组件
        """
        layout = QHBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建标签
        self.label = QLabel(label_text)
        
        # 创建图标标签
        self.icon_label = QLabel()
        
        # 使用GetIconSvg函数获取图标
        icon = GetIconSvg(icon_name, icon=False)
        
        # 设置图标
        if icon and icon != "":
            self.icon_label.setPixmap(GetIconSvg(icon_name).pixmap(16, 16))
        else:
            # 如果图标不存在，使用文本"i"作为替代
            self.icon_label.setText("i")
            self.icon_label.setStyleSheet(
                "background-color: #FFD700; color: #000000; border-radius: 8px; "
                "padding: 2px; min-width: 16px; min-height: 16px; "
                "max-width: 16px; max-height: 16px; text-align: center;"
            )
        
        # 设置鼠标悬停提示
        if tooltip_text:
            self.icon_label.setToolTip(tooltip_text)
            self.icon_label.setCursor(QCursor(Qt.WhatsThisCursor))
        
        # 添加组件到布局
        layout.addWidget(self.icon_label)
        layout.addWidget(self.label)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def setText(self, text):
        """
        设置标签文本
        """
        self.label.setText(text)
    
    def setToolTip(self, text):
        """
        设置图标的鼠标悬停提示文本
        """
        self.icon_label.setToolTip(text)