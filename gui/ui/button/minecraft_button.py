from PyQt5.QtCore import Qt, QRect, QSize, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPixmap
from PyQt5.QtWidgets import QPushButton

from ..minecraft_style import get_minecraft_font

class MinecraftPixelButton(QPushButton):
    """像素风格的我的世界按钮"""
    
    def __init__(self, text, parent=None, button_type="green"):
        super().__init__(text, parent)
        self.button_type = button_type  # green, brown, gray
        self.hovered = False
        self.pressed = False
        
        # 设置字体
        self.setFont(get_minecraft_font(12, True))
        
        # 设置鼠标跟踪和光标
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)
        
        # 设置最小尺寸
        self.setMinimumSize(120, 40)
        
        # 移除默认样式
        self.setStyleSheet("")
        
    def enterEvent(self, event):
        self.hovered = True
        self.update()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.hovered = False
        self.update()
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressed = True
            self.update()
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressed = False
            self.update()
        super().mouseReleaseEvent(event)
    
    def paintEvent(self, event):
        """自定义绘制事件，实现像素风格的按钮"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)  # 关闭抗锯齿，保持像素风格
        
        # 获取按钮矩形
        rect = self.rect()
        
        # 根据按钮类型和状态选择颜色
        if self.button_type == "green":
            # 绿色按钮（类似草方块）
            if self.pressed:
                main_color = QColor("#4A6C27")  # 暗绿色
                border_color = QColor("#2D3F18")  # 深绿色
                highlight_color = QColor("#5D8731")  # 草绿色
                shadow_color = QColor("#3B511F")  # 暗绿色
            elif self.hovered:
                main_color = QColor("#6FA044")  # 亮绿色
                border_color = QColor("#3B511F")  # 深绿色
                highlight_color = QColor("#7FB154")  # 更亮的绿色
                shadow_color = QColor("#4A6C27")  # 暗绿色
            else:
                main_color = QColor("#5D8731")  # 草绿色
                border_color = QColor("#3B511F")  # 深绿色
                highlight_color = QColor("#6FA044")  # 亮绿色
                shadow_color = QColor("#4A6C27")  # 暗绿色
        
        elif self.button_type == "brown":
            # 棕色按钮（类似木头）
            if self.pressed:
                main_color = QColor("#866D3F")  # 暗棕色
                border_color = QColor("#574628")  # 深棕色
                highlight_color = QColor("#9C7F4A")  # 木头棕色
                shadow_color = QColor("#6E5831")  # 暗棕色
            elif self.hovered:
                main_color = QColor("#B8965A")  # 亮棕色
                border_color = QColor("#6E5831")  # 深棕色
                highlight_color = QColor("#C9A66A")  # 更亮的棕色
                shadow_color = QColor("#866D3F")  # 暗棕色
            else:
                main_color = QColor("#9C7F4A")  # 木头棕色
                border_color = QColor("#6E5831")  # 深棕色
                highlight_color = QColor("#B8965A")  # 亮棕色
                shadow_color = QColor("#866D3F")  # 暗棕色
        
        else:  # gray
            # 灰色按钮（类似石头）
            if self.pressed:
                main_color = QColor("#5A5A5A")  # 暗灰色
                border_color = QColor("#373737")  # 深灰色
                highlight_color = QColor("#828282")  # 石头灰色
                shadow_color = QColor("#4A4A4A")  # 暗灰色
            elif self.hovered:
                main_color = QColor("#A0A0A0")  # 亮灰色
                border_color = QColor("#5A5A5A")  # 深灰色
                highlight_color = QColor("#B0B0B0")  # 更亮的灰色
                shadow_color = QColor("#5A5A5A")  # 暗灰色
            else:
                main_color = QColor("#828282")  # 石头灰色
                border_color = QColor("#5A5A5A")  # 深灰色
                highlight_color = QColor("#A0A0A0")  # 亮灰色
                shadow_color = QColor("#5A5A5A")  # 暗灰色
        
        # 绘制按钮边框（2像素宽）
        painter.setPen(QPen(border_color, 2))
        painter.setBrush(QBrush(main_color))
        painter.drawRect(rect.adjusted(1, 1, -1, -1))
        
        # 绘制按钮高光（顶部和左侧）
        if not self.pressed:
            highlight_pen = QPen(highlight_color, 1)
            painter.setPen(highlight_pen)
            painter.drawLine(rect.left() + 2, rect.top() + 2, rect.right() - 2, rect.top() + 2)  # 顶部
            painter.drawLine(rect.left() + 2, rect.top() + 2, rect.left() + 2, rect.bottom() - 2)  # 左侧
        
        # 绘制按钮阴影（底部和右侧）
        shadow_pen = QPen(shadow_color, 1)
        painter.setPen(shadow_pen)
        painter.drawLine(rect.left() + 2, rect.bottom() - 2, rect.right() - 2, rect.bottom() - 2)  # 底部
        painter.drawLine(rect.right() - 2, rect.top() + 2, rect.right() - 2, rect.bottom() - 2)  # 右侧
        
        # 绘制文本
        text_rect = rect
        if self.pressed:
            # 按下时文本稍微下移
            text_rect.translate(0, 2)
        
        # 绘制文本阴影
        painter.setPen(QColor("#000000"))
        painter.drawText(text_rect.adjusted(2, 2, 2, 2), Qt.AlignCenter, self.text())
        
        # 绘制文本
        painter.setPen(QColor("#FFFFFF"))
        painter.drawText(text_rect, Qt.AlignCenter, self.text())