from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QPixmap, QPainter, QBrush, QLinearGradient
from PyQt5.QtWidgets import QStyleFactory, QPushButton, QLabel, QWidget, QFrame

# 我的世界风格的颜色
MC_COLORS = {
    'dirt_brown': '#866043',  # 泥土棕色
    'stone_gray': '#828282',   # 石头灰色
    'grass_green': '#5D8731',  # 草地绿色
    'wood_brown': '#9C7F4A',   # 木头棕色
    'dark_gray': '#373737',    # 深灰色（煤炭方块）
    'light_blue': '#3AAFD9',   # 浅蓝色（钻石方块）
    'black': '#000000',        # 黑色
    'white': '#FFFFFF',        # 白色
    'light_gray': '#C6C6C6',   # 浅灰色
    'text_yellow': '#FFFF55',  # 文本黄色
}

# 我的世界风格的字体
MC_FONT = "Minecraft"

# 备用字体列表
FALLBACK_FONTS = ["Courier New", "Consolas", "Monospace"]


def get_minecraft_font(size=12, bold=False):
    """获取我的世界风格的字体"""
    # 尝试使用Minecraft字体，如果不可用则使用备用字体
    font = QFont(MC_FONT, size)
    
    # 如果Minecraft字体不可用，尝试备用字体
    if not font.exactMatch():
        for fallback in FALLBACK_FONTS:
            font = QFont(fallback, size)
            if font.exactMatch():
                break
    
    # 设置字体粗细
    if bold:
        font.setBold(True)
    
    # 设置像素化渲染（模拟我的世界像素风格）
    font.setStyleStrategy(QFont.NoAntialias)
    
    return font


class MinecraftButton(QPushButton):
    """我的世界风格的按钮"""
    
    def __init__(self, text, parent=None, primary=True):
        super().__init__(text, parent)
        self.primary = primary  # 主按钮或次要按钮
        self.setFont(get_minecraft_font(12, True))
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(40)
        
        # 设置样式
        self._update_style()
        
    def _update_style(self):
        """更新按钮样式"""
        if self.primary:
            # 主按钮样式（绿色，类似草方块）
            self.setStyleSheet("""
                QPushButton {
                    background-color: #5D8731; /* 草绿色 */
                    color: white;
                    border: 2px solid #3B511F; /* 深绿色边框 */
                    border-radius: 2px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #6FA044; /* 亮一点的绿色 */
                }
                QPushButton:pressed {
                    background-color: #4A6C27; /* 暗一点的绿色 */
                    border: 2px solid #2D3F18; /* 更深的绿色边框 */
                    padding-top: 10px; /* 模拟按下效果 */
                    padding-bottom: 6px;
                }
                QPushButton:disabled {
                    background-color: #828282; /* 石头灰色 */
                    color: #C6C6C6; /* 浅灰色 */
                    border: 2px solid #5A5A5A; /* 深灰色边框 */
                }
            """)
        else:
            # 次要按钮样式（棕色，类似木头）
            self.setStyleSheet("""
                QPushButton {
                    background-color: #9C7F4A; /* 木头棕色 */
                    color: white;
                    border: 2px solid #6E5831; /* 深棕色边框 */
                    border-radius: 2px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #B8965A; /* 亮一点的棕色 */
                }
                QPushButton:pressed {
                    background-color: #866D3F; /* 暗一点的棕色 */
                    border: 2px solid #574628; /* 更深的棕色边框 */
                    padding-top: 10px; /* 模拟按下效果 */
                    padding-bottom: 6px;
                }
                QPushButton:disabled {
                    background-color: #828282; /* 石头灰色 */
                    color: #C6C6C6; /* 浅灰色 */
                    border: 2px solid #5A5A5A; /* 深灰色边框 */
                }
            """)


class MinecraftSettingsButton(QPushButton):
    """我的世界风格的设置按钮"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(get_minecraft_font(10))
        self.setCursor(Qt.PointingHandCursor)
        
        # 设置样式
        self.setStyleSheet("""
            QPushButton {
                background-color: #373737; /* 深灰色 */
                color: #FFFF55; /* 黄色文本 */
                border: 2px solid #1F1F1F; /* 黑色边框 */
                border-radius: 2px;
                padding: 4px 12px;
            }
            QPushButton:hover {
                background-color: #4A4A4A; /* 亮一点的灰色 */
            }
            QPushButton:pressed {
                background-color: #2A2A2A; /* 暗一点的灰色 */
                border: 2px solid #0F0F0F; /* 更深的黑色边框 */
                padding-top: 6px; /* 模拟按下效果 */
                padding-bottom: 2px;
            }
        """)


class MinecraftFrame(QFrame):
    """我的世界风格的框架"""
    
    def __init__(self, parent=None, frame_type="stone"):
        super().__init__(parent)
        self.frame_type = frame_type  # stone, dirt, wood
        
        # 设置样式
        self._update_style()
    
    def _update_style(self):
        """更新框架样式"""
        if self.frame_type == "stone":
            self.setStyleSheet("""
                QFrame {
                    background-color: #828282; /* 石头灰色 */
                    border: 2px solid #5A5A5A; /* 深灰色边框 */
                    border-radius: 2px;
                }
            """)
        elif self.frame_type == "dirt":
            self.setStyleSheet("""
                QFrame {
                    background-color: #866043; /* 泥土棕色 */
                    border: 2px solid #5E432F; /* 深棕色边框 */
                    border-radius: 2px;
                }
            """)
        elif self.frame_type == "wood":
            self.setStyleSheet("""
                QFrame {
                    background-color: #9C7F4A; /* 木头棕色 */
                    border: 2px solid #6E5831; /* 深棕色边框 */
                    border-radius: 2px;
                }
            """)


class MinecraftTitleLabel(QLabel):
    """我的世界风格的标题标签"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(get_minecraft_font(18, True))
        self.setStyleSheet("""
            QLabel {
                color: #FFFF55; /* 黄色文本 */
                background-color: transparent;
            }
        """)
        self.setAlignment(Qt.AlignCenter)


class MinecraftLabel(QLabel):
    """我的世界风格的普通标签"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(get_minecraft_font(12))
        self.setStyleSheet("""
            QLabel {
                color: white;
                background-color: transparent;
            }
        """)


def apply_minecraft_style(widget):
    """应用我的世界风格到整个应用"""
    # 设置应用的全局样式
    widget.setStyleSheet("""
        QWidget {
            background-color: #373737; /* 深灰色背景 */
            color: white;
        }
        QScrollBar:vertical {
            border: none;
            background: #1F1F1F;
            width: 12px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background: #5D8731; /* 草绿色 */
            min-height: 20px;
            border-radius: 2px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        QScrollBar:horizontal {
            border: none;
            background: #1F1F1F;
            height: 12px;
            margin: 0px;
        }
        QScrollBar::handle:horizontal {
            background: #5D8731; /* 草绿色 */
            min-width: 20px;
            border-radius: 2px;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
        }
    """)