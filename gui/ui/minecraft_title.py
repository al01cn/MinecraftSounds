from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QPixmap, QFontMetrics
from PyQt5.QtWidgets import QLabel

class MinecraftTitle(QLabel):
    """我的世界风格的标题标签"""
    
    def __init__(self, text, parent=None, shadow=True):
        super().__init__(text, parent)
        self.shadow = shadow  # 是否显示阴影
        self.title_text = text
        
        # 尝试使用Minecraft字体，如果不可用则使用备用字体
        self.font = QFont("Minecraft", 24)
        if not self.font.exactMatch():
            fallback_fonts = ["Courier New", "Consolas", "Monospace"]
            for fallback in fallback_fonts:
                self.font = QFont(fallback, 24)
                if self.font.exactMatch():
                    break
        
        # 设置字体粗细和像素化渲染
        self.font.setBold(True)
        self.font.setStyleStrategy(QFont.NoAntialias)
        
        # 设置标签属性
        self.setFont(self.font)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: transparent;")
        
        # 计算文本大小
        fm = QFontMetrics(self.font)
        text_width = fm.horizontalAdvance(text)
        text_height = fm.height()
        
        # 设置最小大小
        self.setMinimumSize(text_width + 20, text_height * 2)
    
    def paintEvent(self, event):
        """自定义绘制事件，实现我的世界风格的文本渲染"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)  # 关闭抗锯齿，保持像素风格
        
        # 设置字体
        painter.setFont(self.font)
        
        # 获取文本矩形
        rect = self.rect()
        
        # 如果启用阴影，先绘制阴影文本
        if self.shadow:
            # 阴影颜色（深灰色）
            painter.setPen(QColor("#3F3F3F"))
            shadow_rect = QRect(rect.x() + 2, rect.y() + 2, rect.width(), rect.height())
            painter.drawText(shadow_rect, Qt.AlignCenter, self.title_text)
        
        # 绘制主文本（黄色，类似我的世界标题）
        painter.setPen(QColor("#FFFF55"))  # 黄色
        painter.drawText(rect, Qt.AlignCenter, self.title_text)