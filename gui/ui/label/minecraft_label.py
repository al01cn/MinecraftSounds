from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QLabel

from ..minecraft_style import get_minecraft_font

class MinecraftLabel(QLabel):
    """我的世界风格的标签"""
    
    def __init__(self, text="", parent=None, shadow=True, color="white"):
        super().__init__(text, parent)
        self.shadow_enabled = shadow
        self.text_color = self._get_color(color)
        self.shadow_color = QColor("#3F3F3F")  # 深灰色阴影
        
        # 设置字体
        self.setFont(get_minecraft_font(11))
        
        # 移除默认样式
        self.setStyleSheet("")
    
    def _get_color(self, color_name):
        """获取预定义的颜色"""
        colors = {
            "white": QColor("#FFFFFF"),
            "yellow": QColor("#FFFF55"),
            "green": QColor("#55FF55"),
            "blue": QColor("#5555FF"),
            "red": QColor("#FF5555"),
            "gray": QColor("#AAAAAA"),
            "dark_gray": QColor("#555555"),
            "gold": QColor("#FFAA00")
        }
        return colors.get(color_name.lower(), QColor("#FFFFFF"))
    
    def paintEvent(self, event):
        """自定义绘制事件，实现像素风格的文本"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)  # 关闭抗锯齿，保持像素风格
        
        # 获取文本矩形
        rect = self.rect()
        text = self.text()
        
        # 如果启用阴影，先绘制阴影文本
        if self.shadow_enabled:
            painter.setPen(self.shadow_color)
            painter.setFont(self.font())
            painter.drawText(rect.adjusted(1, 1, 1, 1), self.alignment(), text)
        
        # 绘制主文本
        painter.setPen(self.text_color)
        painter.setFont(self.font())
        painter.drawText(rect, self.alignment(), text)

class MinecraftTitleLabel(MinecraftLabel):
    """我的世界风格的标题标签"""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent, shadow=True, color="yellow")
        
        # 设置更大的字体
        self.setFont(get_minecraft_font(18, True))