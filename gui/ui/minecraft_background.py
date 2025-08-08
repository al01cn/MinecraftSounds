from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPixmap
from PyQt5.QtWidgets import QWidget


class MinecraftBackground(QWidget):
    """我的世界风格的背景小部件"""
    
    def __init__(self, parent=None, pattern="dirt"):
        super().__init__(parent)
        self.pattern = pattern  # 背景图案: dirt, stone, planks
        self.block_size = 32    # 方块大小
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAutoFillBackground(True)
        
        # 创建背景纹理
        self.background_texture = self._create_texture()
    
    def _create_texture(self):
        """创建背景纹理"""
        # 创建单个方块的纹理
        block = QPixmap(self.block_size, self.block_size)
        block.fill(Qt.transparent)
        
        painter = QPainter(block)
        painter.setRenderHint(QPainter.Antialiasing, False)  # 关闭抗锯齿，保持像素风格
        
        if self.pattern == "dirt":
            # 泥土方块纹理
            main_color = QColor("#866043")  # 泥土棕色
            dark_color = QColor("#5E432F")  # 深棕色
            light_color = QColor("#9C7F4A")  # 浅棕色
            
            # 填充主色
            painter.fillRect(0, 0, self.block_size, self.block_size, main_color)
            
            # 添加一些随机的深色和浅色像素点，模拟泥土纹理
            pen = QPen()
            for i in range(0, self.block_size, 4):
                for j in range(0, self.block_size, 4):
                    # 随机选择深色或浅色
                    if (i + j) % 8 == 0:
                        pen.setColor(dark_color)
                    elif (i + j) % 7 == 0:
                        pen.setColor(light_color)
                    else:
                        continue
                    
                    painter.setPen(pen)
                    painter.drawPoint(i, j)
            
            # 添加顶部草地边缘
            if self.pattern == "dirt":
                grass_color = QColor("#5D8731")  # 草绿色
                dark_grass = QColor("#3B511F")  # 深绿色
                
                # 顶部草地
                painter.fillRect(0, 0, self.block_size, 4, grass_color)
                
                # 草地和泥土的过渡区域
                transition_height = 3
                for i in range(transition_height):
                    alpha = 255 - (i * 255 // transition_height)
                    transition_color = QColor(grass_color)
                    transition_color.setAlpha(alpha)
                    
                    pen = QPen(transition_color)
                    painter.setPen(pen)
                    for j in range(0, self.block_size, 2):
                        if (j + i) % 3 != 0:  # 创建一些随机性
                            painter.drawPoint(j, 4 + i)
        
        elif self.pattern == "stone":
            # 石头方块纹理
            main_color = QColor("#828282")  # 石头灰色
            dark_color = QColor("#5A5A5A")  # 深灰色
            light_color = QColor("#A0A0A0")  # 浅灰色
            
            # 填充主色
            painter.fillRect(0, 0, self.block_size, self.block_size, main_color)
            
            # 添加一些随机的深色和浅色像素点，模拟石头纹理
            pen = QPen()
            for i in range(0, self.block_size, 4):
                for j in range(0, self.block_size, 4):
                    # 随机选择深色或浅色
                    if (i * j) % 16 == 0:
                        pen.setColor(dark_color)
                    elif (i * j) % 15 == 0:
                        pen.setColor(light_color)
                    else:
                        continue
                    
                    painter.setPen(pen)
                    painter.drawPoint(i, j)
        
        elif self.pattern == "planks":
            # 木板方块纹理
            main_color = QColor("#9C7F4A")  # 木头棕色
            dark_color = QColor("#6E5831")  # 深棕色
            
            # 填充主色
            painter.fillRect(0, 0, self.block_size, self.block_size, main_color)
            
            # 绘制木板纹理
            pen = QPen(dark_color)
            pen.setWidth(1)
            painter.setPen(pen)
            
            # 水平木板线
            plank_height = self.block_size // 4
            for i in range(4):
                y = i * plank_height
                painter.drawLine(0, y, self.block_size, y)
                
                # 每块木板添加一些垂直的木纹
                for j in range(2):
                    x = (j + 1) * (self.block_size // 3)
                    start_y = y + 2
                    end_y = y + plank_height - 2
                    painter.drawLine(x, start_y, x, end_y)
        
        painter.end()
        return block
    
    def paintEvent(self, event):
        """绘制背景"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)  # 关闭抗锯齿，保持像素风格
        
        # 计算需要绘制的方块数量
        width, height = self.width(), self.height()
        cols = width // self.block_size + 1
        rows = height // self.block_size + 1
        
        # 绘制背景方块
        for row in range(rows):
            for col in range(cols):
                x = col * self.block_size
                y = row * self.block_size
                painter.drawPixmap(x, y, self.background_texture)