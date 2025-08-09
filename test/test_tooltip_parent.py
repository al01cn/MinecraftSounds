from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gui.components.tooltip import TooltipIcon, PreferredPosition

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tooltip Parent Test')
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建不同位置的tooltip图标
        positions = [
            PreferredPosition.Top,
            PreferredPosition.Bottom,
            PreferredPosition.Left,
            PreferredPosition.Right,
            PreferredPosition.TopLeft,
            PreferredPosition.TopRight,
            PreferredPosition.BottomLeft,
            PreferredPosition.BottomRight
        ]
        
        for i, pos in enumerate(positions):
            row_layout = QHBoxLayout()
            
            # 创建标签
            label = QLabel(f'{pos.value}:')
            
            # 创建带有tooltip的图标
            icon = TooltipIcon(
                tooltip_title=f'{pos.value}位置',
                tooltip_content=f'这是{pos.value}位置的提示内容\n每个图标都是自己tooltip的父组件',
                preferred_position=pos
            )
            
            # 添加到布局
            row_layout.addWidget(label)
            row_layout.addWidget(icon)
            row_layout.addStretch()
            
            main_layout.addLayout(row_layout)
        
        # 添加说明
        info_label = QLabel('将鼠标悬停在图标上查看tooltip，每个图标都是自己tooltip的父组件')
        info_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(info_label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestWindow()
    window.resize(400, 500)
    window.show()
    sys.exit(app.exec_())