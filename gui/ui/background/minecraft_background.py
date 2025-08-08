from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import QWidget

class MinecraftBackground(QWidget):
    """我的世界风格的背景组件"""
    
    DIRT = "dirt"  # 泥土背景
    STONE = "stone"  # 石头背景
    PLANKS = "planks"  # 木板背景
    
    def __init__(self, parent=None, bg_type=DIRT):
        super().__init__(parent)
        self.bg_type = bg_type
        
        # 设置属性，使其作为背景
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.lower()  # 将背景置于底层
        
        # 设置尺寸策略，使其填充父控件
        self.setSizePolicy(QWidget.Expanding, QWidget.Expanding)
    
    def paintEvent(self, event):
        """自定义绘制事件，实现像素风格的背景"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)  # 关闭抗锯齿，保持像素风格
        
        # 获取背景矩形
        rect = self.rect()
        
        # 根据背景类型选择颜色
        if self.bg_type == self.DIRT:
            # 泥土背景
            colors = [
                QColor("#8B5A2B"),  # 主色调
                QColor("#7D512A"),  # 变种1
                QColor("#9A6434"),  # 变种2
                QColor("#704626")   # 变种3
            ]
        elif self.bg_type == self.PLANKS:
            # 木板背景
            colors = [
                QColor("#9C7F4A"),  # 主色调
                QColor("#8A7142"),  # 变种1
                QColor("#A88A50"),  # 变种2
                QColor("#866D3F")   # 变种3
            ]
        else:  # STONE
            # 石头背景
            colors = [
                QColor("#828282"),  # 主色调
                QColor("#757575"),  # 变种1
                QColor("#8E8E8E"),  # 变种2
                QColor("#6A6A6A")   # 变种3
            ]
        
        # 绘制背景方块
        block_size = 16  # 方块大小
        for x in range(0, rect.width(), block_size):
            for y in range(0, rect.height(), block_size):
                # 随机选择一种颜色变体（使用固定模式，而不是真正的随机，以保持一致性）
                color_index = ((x // block_size) + (y // block_size)) % len(colors)
                painter.fillRect(x, y, block_size, block_size, colors[color_index])
                
                # 添加一些像素风格的细节
                if color_index == 1:  # 为某些方块添加小点
                    painter.fillRect(x + 4, y + 4, 2, 2, colors[3])
                    painter.fillRect(x + 10, y + 10, 2, 2, colors[3])
                elif color_index == 2:  # 为某些方块添加线条
                    painter.fillRect(x + 2, y + 8, 12, 1, colors[3])