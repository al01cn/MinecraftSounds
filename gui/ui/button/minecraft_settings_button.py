from PyQt5.QtCore import Qt, QRect, QSize, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPixmap, QFont
from PyQt5.QtWidgets import QPushButton

from ..minecraft_style import get_minecraft_font

class MinecraftSettingsButton(QPushButton):
    """我的世界风格的设置按钮"""
    
    def __init__(self, text="设置", parent=None):
        super().__init__(text, parent)
        self.hovered = False
        self.pressed = False
        self.text = text
        
        # 设置固定大小
        self.setFixedSize(40, 40)
        
        # 设置鼠标跟踪和光标
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)
        
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
        """自定义绘制事件，实现像素风格的设置按钮"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)  # 关闭抗锯齿，保持像素风格
        
        # 获取按钮矩形
        rect = self.rect()
        
        # 根据状态选择颜色（使用石头风格）
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
        
        # 绘制齿轮图标
        self._draw_gear_icon(painter, rect, self.pressed)
    
    def _draw_gear_icon(self, painter, rect, is_pressed):
        """绘制像素风格的齿轮图标"""
        # 设置图标颜色
        painter.setPen(QPen(QColor("#FFFFFF"), 2))
        
        # 计算中心点和偏移
        center_x = rect.width() // 2
        center_y = rect.height() // 2
        offset = 2 if is_pressed else 0  # 按下时图标下移
        
        # 绘制齿轮外圈（像素风格）
        size = min(rect.width(), rect.height()) // 2 - 6
        
        # 绘制齿轮外圈（像素风格）
        # 外圈是一个8边形
        outer_points = [
            QPoint(center_x - size, center_y - size//2 + offset),
            QPoint(center_x - size//2, center_y - size + offset),
            QPoint(center_x + size//2, center_y - size + offset),
            QPoint(center_x + size, center_y - size//2 + offset),
            QPoint(center_x + size, center_y + size//2 + offset),
            QPoint(center_x + size//2, center_y + size + offset),
            QPoint(center_x - size//2, center_y + size + offset),
            QPoint(center_x - size, center_y + size//2 + offset)
        ]
        
        # 绘制齿轮外圈
        for i in range(len(outer_points)):
            painter.drawLine(outer_points[i], outer_points[(i+1) % len(outer_points)])
        
        # 绘制内圈（圆形）
        inner_size = size // 2
        painter.drawRect(QRect(
            center_x - inner_size, 
            center_y - inner_size + offset, 
            inner_size * 2, 
            inner_size * 2
        ))