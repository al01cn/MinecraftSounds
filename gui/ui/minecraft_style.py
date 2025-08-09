from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QPixmap, QPainter, QBrush, QLinearGradient, QFontDatabase
from PyQt5.QtWidgets import QStyleFactory, QPushButton, QLabel, QWidget, QFrame
import os

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

# 我的世界风格的字体路径
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONTS_PATH = os.path.join(ROOT_PATH, 'app', 'assets', 'fonts')
MC_REGULAR_FONT = os.path.join(FONTS_PATH, 'MinecraftRegular-Bmg3.otf')
MC_BOLD_FONT = os.path.join(FONTS_PATH, 'MinecraftBold-nMK1.otf')
MC_ITALIC_FONT = os.path.join(FONTS_PATH, 'MinecraftItalic-R8Mo.otf')
MC_BOLD_ITALIC_FONT = os.path.join(FONTS_PATH, 'MinecraftBoldItalic-1y1e.otf')

# 字体ID
MC_FONT_REGULAR_ID = "Minecraft Regular"
MC_FONT_BOLD_ID = "Minecraft Bold"
MC_FONT_ITALIC_ID = "Minecraft Italic"
MC_FONT_BOLD_ITALIC_ID = "Minecraft Bold Italic"

# 备用字体列表
FALLBACK_FONTS = ["Courier New", "Consolas", "Monospace"]


# 初始化字体数据库
def init_minecraft_fonts():
    """初始化并加载Minecraft字体到字体数据库"""
    font_db = QFontDatabase()
    
    # 检查并加载常规字体
    if os.path.exists(MC_REGULAR_FONT):
        font_db.addApplicationFont(MC_REGULAR_FONT)
    
    # 检查并加载粗体字体
    if os.path.exists(MC_BOLD_FONT):
        font_db.addApplicationFont(MC_BOLD_FONT)
    
    # 检查并加载斜体字体
    if os.path.exists(MC_ITALIC_FONT):
        font_db.addApplicationFont(MC_ITALIC_FONT)
    
    # 检查并加载粗斜体字体
    if os.path.exists(MC_BOLD_ITALIC_FONT):
        font_db.addApplicationFont(MC_BOLD_ITALIC_FONT)

# 字体初始化函数将在应用程序启动后调用
# 不要在这里调用 init_minecraft_fonts()

def get_minecraft_font(size=12, bold=False, italic=False):
    """获取我的世界风格的字体"""
    font = QFont()
    
    # 根据粗体和斜体选择合适的字体
    if bold and italic:
        font = QFont(MC_FONT_BOLD_ITALIC_ID, size)
    elif bold:
        font = QFont(MC_FONT_BOLD_ID, size)
    elif italic:
        font = QFont(MC_FONT_ITALIC_ID, size)
    else:
        font = QFont(MC_FONT_REGULAR_ID, size)
    
    # 如果字体不可用，尝试备用字体
    if not font.exactMatch():
        for fallback in FALLBACK_FONTS:
            font = QFont(fallback, size)
            if font.exactMatch():
                break
        # 手动设置粗体和斜体
        if bold:
            font.setBold(True)
        if italic:
            font.setItalic(True)
    
    # 设置像素化渲染（模拟我的世界像素风格）
    font.setStyleStrategy(QFont.NoAntialias)
    
    return font


class MinecraftButton(QPushButton):
    """我的世界风格的按钮"""
    
    def __init__(self, text, parent=None, primary=True):
        super().__init__(text, parent)
        self.primary = primary  # 主按钮或次要按钮
        self.setFont(get_minecraft_font(12, bold=True))
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
        self.setFont(get_minecraft_font(10, bold=False, italic=False))
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
        self.setFont(get_minecraft_font(18, bold=True))
        self.setStyleSheet("""
            QLabel {
                color: #FFFF55; /* 黄色文本 */
                background-color: transparent;
            }
        """)
        self.setAlignment(Qt.AlignCenter)


class MinecraftLabel(QLabel):
    """我的世界风格的普通标签"""
    
    def __init__(self, text, parent=None, bold=False, italic=False):
        super().__init__(text, parent)
        self.setFont(get_minecraft_font(12, bold=bold, italic=italic))
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