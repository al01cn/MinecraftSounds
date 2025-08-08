from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtWidgets import QFrame

class MinecraftFrame(QFrame):
    """我的世界风格的框架，用于包装其他UI元素"""
    
    DIRT = "dirt"  # 泥土风格
    STONE = "stone"  # 石头风格
    WOOD = "wood"  # 木头风格
    
    def __init__(self, parent=None, frame_type=STONE):
        super().__init__(parent)
        self.frame_type = frame_type
        
        # 移除默认样式
        self.setStyleSheet("")
        self.setFrameShape(QFrame.NoFrame)
        
        # 设置最小尺寸
        self.setMinimumSize(100, 100)
    
    def paintEvent(self, event):
        """自定义绘制事件，实现像素风格的框架"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)  # 关闭抗锯齿，保持像素风格
        
        # 获取框架矩形
        rect = self.rect()
        
        # 根据框架类型选择颜色
        if self.frame_type == self.DIRT:
            # 泥土风格
            main_color = QColor("#8B5A2B")  # 泥土棕色
            border_color = QColor("#5C3A1D")  # 深棕色
            highlight_color = QColor("#A67C52")  # 亮棕色
            shadow_color = QColor("#704626")  # 暗棕色
            
        elif self.frame_type == self.WOOD:
            # 木头风格
            main_color = QColor("#9C7F4A")  # 木头棕色
            border_color = QColor("#6E5831")  # 深棕色
            highlight_color = QColor("#B8965A")  # 亮棕色
            shadow_color = QColor("#866D3F")  # 暗棕色
            
        else:  # STONE
            # 石头风格
            main_color = QColor("#828282")  # 石头灰色
            border_color = QColor("#5A5A5A")  # 深灰色
            highlight_color = QColor("#A0A0A0")  # 亮灰色
            shadow_color = QColor("#6A6A6A")  # 暗灰色
        
        # 绘制框架背景
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(main_color))
        painter.drawRect(rect.adjusted(3, 3, -3, -3))
        
        # 绘制框架边框（3像素宽）
        painter.setPen(QPen(border_color, 3))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(rect.adjusted(1, 1, -1, -1))
        
        # 绘制框架高光（顶部和左侧）
        highlight_pen = QPen(highlight_color, 1)
        painter.setPen(highlight_pen)
        painter.drawLine(rect.left() + 3, rect.top() + 3, rect.right() - 3, rect.top() + 3)  # 顶部
        painter.drawLine(rect.left() + 3, rect.top() + 3, rect.left() + 3, rect.bottom() - 3)  # 左侧
        
        # 绘制框架阴影（底部和右侧）
        shadow_pen = QPen(shadow_color, 1)
        painter.setPen(shadow_pen)
        painter.drawLine(rect.left() + 3, rect.bottom() - 3, rect.right() - 3, rect.bottom() - 3)  # 底部
        painter.drawLine(rect.right() - 3, rect.top() + 3, rect.right() - 3, rect.bottom() - 3)  # 右侧
        
        # 调用父类的绘制事件，以便子控件能够正常绘制
        super().paintEvent(event)