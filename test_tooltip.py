import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout, QFrame
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor
from gui.components.tooltip import Tooltip, TooltipIcon, TooltipLabel, TooltipWidget, TooltipPosition, TooltipTheme, TooltipStyle

class TestTooltipWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tooltip 组件测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 启用调试模式
        self.debug_mode = True
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建标题
        title_label = QLabel("Tooltip 组件测试")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 创建分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)
        
        # 创建测试区域
        test_layout = QGridLayout()
        main_layout.addLayout(test_layout)
        
        # 1. 测试基本 Tooltip
        basic_tooltip_section = QWidget()
        basic_tooltip_layout = QVBoxLayout(basic_tooltip_section)
        basic_tooltip_label = QLabel("基本 Tooltip")
        basic_tooltip_label.setStyleSheet("font-weight: bold;")
        basic_tooltip_layout.addWidget(basic_tooltip_label)
        
        # 创建一个按钮，鼠标悬停时显示 Tooltip
        basic_tooltip_button = QPushButton("悬停显示基本 Tooltip")
        basic_tooltip_layout.addWidget(basic_tooltip_button)
        
        # 创建 Tooltip 实例
        self.basic_tooltip = Tooltip(self)
        
        # 为Tooltip添加调试功能
        if self.debug_mode:
            # 保存原始的enterEvent和leaveEvent方法
            original_enter_event = self.basic_tooltip.enterEvent
            original_leave_event = self.basic_tooltip.leaveEvent
            
            # 重写enterEvent方法，添加调试信息
            def debug_enter_event(event):
                print("[调试信息] Tooltip.enterEvent 被触发")
                print(f"[调试信息] 进入前状态: auto_hide={self.basic_tooltip.auto_hide}, is_pinned={self.basic_tooltip.is_pinned if hasattr(self.basic_tooltip, 'is_pinned') else '未定义'}")
                # 调用原始方法
                original_enter_event(event)
                print(f"[调试信息] 进入后状态: auto_hide={self.basic_tooltip.auto_hide}, is_pinned={self.basic_tooltip.is_pinned if hasattr(self.basic_tooltip, 'is_pinned') else '未定义'}")
                print("-----------------------------------")
            
            # 重写leaveEvent方法，添加调试信息
            def debug_leave_event(event):
                print("[调试信息] Tooltip.leaveEvent 被触发")
                print(f"[调试信息] 离开前状态: auto_hide={self.basic_tooltip.auto_hide}, is_pinned={self.basic_tooltip.is_pinned if hasattr(self.basic_tooltip, 'is_pinned') else '未定义'}")
                # 调用原始方法
                original_leave_event(event)
                print(f"[调试信息] 离开后状态: auto_hide={self.basic_tooltip.auto_hide}, is_pinned={self.basic_tooltip.is_pinned if hasattr(self.basic_tooltip, 'is_pinned') else '未定义'}")
                print("-----------------------------------")
            
            # 替换原始方法
            self.basic_tooltip.enterEvent = debug_enter_event
            self.basic_tooltip.leaveEvent = debug_leave_event
        
        # 设置按钮的鼠标悬停事件
        basic_tooltip_button.enterEvent = lambda event: self.show_basic_tooltip(event, basic_tooltip_button)
        basic_tooltip_button.leaveEvent = lambda event: self.basic_tooltip.hideTooltip()
        
        test_layout.addWidget(basic_tooltip_section, 0, 0)
        
        # 2. 测试不同位置的 Tooltip
        position_tooltip_section = QWidget()
        position_tooltip_layout = QVBoxLayout(position_tooltip_section)
        position_tooltip_label = QLabel("不同位置的 Tooltip")
        position_tooltip_label.setStyleSheet("font-weight: bold;")
        position_tooltip_layout.addWidget(position_tooltip_label)
        
        # 创建一个网格布局，用于放置不同位置的按钮
        position_grid = QGridLayout()
        position_tooltip_layout.addLayout(position_grid)
        
        # 创建不同位置的按钮
        positions = [
            (TooltipPosition.TopLeft, "左上", 0, 0),
            (TooltipPosition.Top, "上", 0, 1),
            (TooltipPosition.TopRight, "右上", 0, 2),
            (TooltipPosition.Left, "左", 1, 0),
            (None, "中", 1, 1),
            (TooltipPosition.Right, "右", 1, 2),
            (TooltipPosition.BottomLeft, "左下", 2, 0),
            (TooltipPosition.Bottom, "下", 2, 1),
            (TooltipPosition.BottomRight, "右下", 2, 2),
        ]
        
        for position, text, row, col in positions:
            if position is not None:
                btn = QPushButton(text)
                btn.setFixedSize(60, 40)
                btn.position = position
                btn.enterEvent = lambda event, btn=btn: self.show_position_tooltip(event, btn)
                btn.leaveEvent = lambda event: self.basic_tooltip.hideTooltip()
                position_grid.addWidget(btn, row, col)
            else:
                # 中间位置放置一个标签
                lbl = QLabel(text)
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setFixedSize(60, 40)
                position_grid.addWidget(lbl, row, col)
        
        test_layout.addWidget(position_tooltip_section, 0, 1)
        
        # 3. 测试不同主题的 Tooltip
        theme_tooltip_section = QWidget()
        theme_tooltip_layout = QVBoxLayout(theme_tooltip_section)
        theme_tooltip_label = QLabel("不同主题的 Tooltip")
        theme_tooltip_label.setStyleSheet("font-weight: bold;")
        theme_tooltip_layout.addWidget(theme_tooltip_label)
        
        # 创建不同主题的按钮
        dark_theme_btn = QPushButton("深色主题")
        dark_theme_btn.theme = TooltipTheme.Dark
        dark_theme_btn.enterEvent = lambda event: self.show_theme_tooltip(event, dark_theme_btn)
        dark_theme_btn.leaveEvent = lambda event: self.basic_tooltip.hideTooltip()
        theme_tooltip_layout.addWidget(dark_theme_btn)
        
        light_theme_btn = QPushButton("浅色主题")
        light_theme_btn.theme = TooltipTheme.Light
        light_theme_btn.enterEvent = lambda event: self.show_theme_tooltip(event, light_theme_btn)
        light_theme_btn.leaveEvent = lambda event: self.basic_tooltip.hideTooltip()
        theme_tooltip_layout.addWidget(light_theme_btn)
        
        custom_theme_btn = QPushButton("自定义主题")
        custom_theme_btn.theme = "custom"
        custom_theme_btn.enterEvent = lambda event: self.show_theme_tooltip(event, custom_theme_btn)
        custom_theme_btn.leaveEvent = lambda event: self.basic_tooltip.hideTooltip()
        theme_tooltip_layout.addWidget(custom_theme_btn)
        
        test_layout.addWidget(theme_tooltip_section, 0, 2)
        
        # 4. 测试 TooltipIcon
        icon_tooltip_section = QWidget()
        icon_tooltip_layout = QVBoxLayout(icon_tooltip_section)
        icon_tooltip_label = QLabel("TooltipIcon 组件")
        icon_tooltip_label.setStyleSheet("font-weight: bold;")
        icon_tooltip_layout.addWidget(icon_tooltip_label)
        
        # 创建 TooltipIcon 实例
        tooltip_icon = TooltipIcon(
            icon_name="SolarInfoCircleOutline",
            tooltip_title="TooltipIcon 示例",
            tooltip_content="这是一个 TooltipIcon 组件，支持鼠标悬停和点击显示 Tooltip。",
            preferred_position=TooltipPosition.Top
        )
        icon_tooltip_layout.addWidget(tooltip_icon, alignment=Qt.AlignCenter)
        
        # 创建另一个使用自定义主题的 TooltipIcon
        custom_style = TooltipStyle()
        custom_style.setCustomColors(
            background_color=QColor(Qt.darkBlue),
            border_color=QColor(Qt.blue),
            text_color=QColor(Qt.white),
            title_color=QColor(Qt.yellow)
        )
        
        tooltip_icon2 = TooltipIcon(
            icon_name="SolarQuestionCircleOutline",
            tooltip_title="自定义样式 TooltipIcon",
            tooltip_content="这个 TooltipIcon 使用了自定义样式，背景为深蓝色，边框为蓝色，文本为白色，标题为黄色。",
            preferred_position=TooltipPosition.Bottom
        )
        tooltip_icon2.setTooltipStyle(custom_style)
        icon_tooltip_layout.addWidget(tooltip_icon2, alignment=Qt.AlignCenter)
        
        test_layout.addWidget(icon_tooltip_section, 1, 0)
        
        # 5. 测试 TooltipLabel
        label_tooltip_section = QWidget()
        label_tooltip_layout = QVBoxLayout(label_tooltip_section)
        label_tooltip_title = QLabel("TooltipLabel 组件")
        label_tooltip_title.setStyleSheet("font-weight: bold;")
        label_tooltip_layout.addWidget(label_tooltip_title)
        
        # 创建 TooltipLabel 实例
        tooltip_label = TooltipLabel(
            label_text="带有 Tooltip 的标签",
            tooltip_title="TooltipLabel 示例",
            tooltip_content="这是一个 TooltipLabel 组件，包含标签文本和一个带有 Tooltip 功能的图标。",
            icon_name="SolarInfoCircleOutline",
            preferred_position=TooltipPosition.Right
        )
        label_tooltip_layout.addWidget(tooltip_label)
        
        # 创建另一个使用浅色主题的 TooltipLabel
        tooltip_label2 = TooltipLabel(
            label_text="浅色主题 TooltipLabel",
            tooltip_title="浅色主题示例",
            tooltip_content="这个 TooltipLabel 使用了浅色主题，背景为浅灰色，文本为深色。",
            icon_name="SolarQuestionCircleOutline",
            preferred_position=TooltipPosition.Bottom
        )
        tooltip_label2.setTooltipTheme(TooltipTheme.Light)
        label_tooltip_layout.addWidget(tooltip_label2)
        
        test_layout.addWidget(label_tooltip_section, 1, 1)
        
        # 6. 测试自定义 TooltipWidget
        custom_tooltip_section = QWidget()
        custom_tooltip_layout = QVBoxLayout(custom_tooltip_section)
        custom_tooltip_label = QLabel("自定义 TooltipWidget")
        custom_tooltip_label.setStyleSheet("font-weight: bold;")
        custom_tooltip_layout.addWidget(custom_tooltip_label)
        
        # 创建一个自定义的 TooltipWidget
        class CustomButton(QPushButton, TooltipWidget):
            def __init__(self, text, tooltip_title, tooltip_content, preferred_position=None, parent=None):
                QPushButton.__init__(self, text, parent)
                TooltipWidget.__init__(self, tooltip_title, tooltip_content, preferred_position, 3, parent)
        
        # 创建自定义按钮实例
        custom_btn = CustomButton(
            "自定义 TooltipWidget 按钮",
            "自定义 TooltipWidget",
            "这是一个继承自 TooltipWidget 的自定义按钮，鼠标悬停时会显示 Tooltip。",
            TooltipPosition.Top
        )
        custom_tooltip_layout.addWidget(custom_btn)
        
        test_layout.addWidget(custom_tooltip_section, 1, 2)
        
        # 7. 测试 auto_hide 功能
        auto_hide_section = QWidget()
        auto_hide_layout = QVBoxLayout(auto_hide_section)
        auto_hide_label = QLabel("Auto Hide 功能测试")
        auto_hide_label.setStyleSheet("font-weight: bold;")
        auto_hide_layout.addWidget(auto_hide_label)
        
        # 添加调试控制区域
        debug_control_layout = QHBoxLayout()
        auto_hide_layout.addLayout(debug_control_layout)
        
        # 添加调试开关按钮
        self.debug_toggle_btn = QPushButton("调试模式: 开启" if self.debug_mode else "调试模式: 关闭")
        self.debug_toggle_btn.setCheckable(True)
        self.debug_toggle_btn.setChecked(self.debug_mode)
        self.debug_toggle_btn.clicked.connect(self.toggle_debug_mode)
        debug_control_layout.addWidget(self.debug_toggle_btn)
        
        # 添加状态显示区域
        self.status_label = QLabel("Tooltip状态: 未显示")
        self.status_label.setStyleSheet("border: 1px solid #ccc; padding: 5px; background-color: #f9f9f9;")
        auto_hide_layout.addWidget(self.status_label)
        
        # 创建一个按钮，用于测试启用 auto_hide 的 Tooltip
        auto_hide_btn = QPushButton("启用 auto_hide (默认)")
        auto_hide_btn.clicked.connect(self.show_auto_hide_tooltip)
        auto_hide_layout.addWidget(auto_hide_btn)
        
        # 创建一个按钮，用于测试禁用 auto_hide 的 Tooltip
        no_auto_hide_btn = QPushButton("禁用 auto_hide (固定显示)")
        no_auto_hide_btn.clicked.connect(self.show_no_auto_hide_tooltip)
        auto_hide_layout.addWidget(no_auto_hide_btn)
        
        # 创建一个按钮，用于强制隐藏所有 Tooltip
        force_hide_btn = QPushButton("强制隐藏所有 Tooltip")
        force_hide_btn.clicked.connect(self.force_hide_all_tooltips)
        auto_hide_layout.addWidget(force_hide_btn)
        
        # 创建一个专用于 auto_hide 测试的 Tooltip
        self.auto_hide_tooltip = Tooltip(self)
        
        # 为auto_hide_tooltip添加调试功能
        if self.debug_mode:
            # 保存原始的enterEvent和leaveEvent方法
            original_enter_event = self.auto_hide_tooltip.enterEvent
            original_leave_event = self.auto_hide_tooltip.leaveEvent
            
            # 重写enterEvent方法，添加调试信息
            def debug_enter_event(event):
                print("[调试信息] auto_hide_tooltip.enterEvent 被触发")
                print(f"[调试信息] 进入前状态: auto_hide={self.auto_hide_tooltip.auto_hide}, is_pinned={self.auto_hide_tooltip.is_pinned if hasattr(self.auto_hide_tooltip, 'is_pinned') else '未定义'}")
                # 调用原始方法
                original_enter_event(event)
                print(f"[调试信息] 进入后状态: auto_hide={self.auto_hide_tooltip.auto_hide}, is_pinned={self.auto_hide_tooltip.is_pinned if hasattr(self.auto_hide_tooltip, 'is_pinned') else '未定义'}")
                print("-----------------------------------")
            
            # 重写leaveEvent方法，添加调试信息
            def debug_leave_event(event):
                print("[调试信息] auto_hide_tooltip.leaveEvent 被触发")
                print(f"[调试信息] 离开前状态: auto_hide={self.auto_hide_tooltip.auto_hide}, is_pinned={self.auto_hide_tooltip.is_pinned if hasattr(self.auto_hide_tooltip, 'is_pinned') else '未定义'}")
                # 调用原始方法
                original_leave_event(event)
                print(f"[调试信息] 离开后状态: auto_hide={self.auto_hide_tooltip.auto_hide}, is_pinned={self.auto_hide_tooltip.is_pinned if hasattr(self.auto_hide_tooltip, 'is_pinned') else '未定义'}")
                print("-----------------------------------")
            
            # 替换原始方法
            self.auto_hide_tooltip.enterEvent = debug_enter_event
            self.auto_hide_tooltip.leaveEvent = debug_leave_event
        
        test_layout.addWidget(auto_hide_section, 2, 0, 1, 3)
        
        # 添加一些空间
        main_layout.addStretch()
    
    def show_basic_tooltip(self, event, button):
        # 获取按钮的全局位置
        pos = button.mapToGlobal(QPoint(button.width() // 2, 0))
        
        # 显示 Tooltip
        self.basic_tooltip.showTooltip(
            pos,
            "基本 Tooltip",
            "这是一个基本的 Tooltip 示例，显示在按钮上方。<br>支持 <b>HTML</b> 格式的文本。"
        )
    
    def show_position_tooltip(self, event, button):
        # 获取按钮的全局位置
        pos = button.mapToGlobal(QPoint(button.width() // 2, button.height() // 2))
        
        # 显示 Tooltip
        self.basic_tooltip.showTooltip(
            pos,
            f"{button.position.value if isinstance(button.position, TooltipPosition) else button.position} 位置",
            f"这个 Tooltip 的首选位置是 {button.position.value if isinstance(button.position, TooltipPosition) else button.position}。<br>根据屏幕边界可能会自动调整位置。",
            button.position
        )
    
    def show_theme_tooltip(self, event, button):
        # 获取按钮的全局位置
        pos = button.mapToGlobal(QPoint(button.width() // 2, 0))
        
        # 设置主题
        if button.theme == "custom":
            # 创建自定义样式
            custom_style = TooltipStyle()
            custom_style.setCustomColors(
                background_color=QColor(Qt.darkGreen),
                border_color=QColor(Qt.green),
                text_color=QColor(Qt.white),
                title_color=QColor(Qt.yellow)
            )
            self.basic_tooltip.setStyle(custom_style)
        else:
            # 使用预定义主题
            self.basic_tooltip.setTheme(button.theme)
        
        # 显示 Tooltip
        theme_name = "自定义" if button.theme == "custom" else ("深色" if button.theme == TooltipTheme.Dark else "浅色")
        self.basic_tooltip.showTooltip(
            pos,
            f"{theme_name}主题 Tooltip",
            f"这是一个使用{theme_name}主题的 Tooltip 示例。<br>可以通过 setTheme() 或 setStyle() 方法设置主题或自定义样式。"
        )

    def show_auto_hide_tooltip(self):
        # 获取按钮的全局位置
        sender = self.sender()
        pos = sender.mapToGlobal(QPoint(sender.width() // 2, sender.height()))
        
        if self.debug_mode:
            print("[调试信息] 显示启用 auto_hide 的 Tooltip")
        
        # 显示启用 auto_hide 的 Tooltip
        self.auto_hide_tooltip.showTooltip(
            pos,
            "启用 auto_hide 的 Tooltip",
            "这个 Tooltip 会在鼠标离开时自动隐藏。<br>这是默认行为。",
            preferred_position=TooltipPosition.Bottom,
            auto_hide=True
        )
        
        # 立即更新状态显示
        self.update_status_display()
        
        # 打印当前状态
        if self.debug_mode:
            print(f"[调试信息] Tooltip状态: auto_hide={self.auto_hide_tooltip.auto_hide}, is_pinned={self.auto_hide_tooltip.is_pinned if hasattr(self.auto_hide_tooltip, 'is_pinned') else '未定义'}")
            print(f"[调试信息] Tooltip位置: x={self.auto_hide_tooltip.x()}, y={self.auto_hide_tooltip.y()}, 宽度={self.auto_hide_tooltip.width()}, 高度={self.auto_hide_tooltip.height()}")
            print("-----------------------------------")
    
    def show_no_auto_hide_tooltip(self):
        # 获取按钮的全局位置
        sender = self.sender()
        pos = sender.mapToGlobal(QPoint(sender.width() // 2, sender.height()))
        
        if self.debug_mode:
            print("[调试信息] 显示禁用 auto_hide 的 Tooltip (固定显示)")
        
        # 显示禁用 auto_hide 的 Tooltip
        self.auto_hide_tooltip.showTooltip(
            pos,
            "禁用 auto_hide 的 Tooltip",
            "这个 Tooltip <b>不会</b>在鼠标离开时自动隐藏。<br>需要点击'强制隐藏'按钮或再次点击此按钮才能隐藏。",
            preferred_position=TooltipPosition.Bottom,
            auto_hide=False
        )
        
        # 立即更新状态显示
        self.update_status_display()
        
        # 打印当前状态
        if self.debug_mode:
            print(f"[调试信息] Tooltip状态: auto_hide={self.auto_hide_tooltip.auto_hide}, is_pinned={self.auto_hide_tooltip.is_pinned if hasattr(self.auto_hide_tooltip, 'is_pinned') else '未定义'}")
            print(f"[调试信息] Tooltip位置: x={self.auto_hide_tooltip.x()}, y={self.auto_hide_tooltip.y()}, 宽度={self.auto_hide_tooltip.width()}, 高度={self.auto_hide_tooltip.height()}")
            print("-----------------------------------")
    
    def force_hide_all_tooltips(self):
        if self.debug_mode:
            print("[调试信息] 强制隐藏所有 Tooltip")
            
            # 打印隐藏前状态
            print(f"[调试信息] 隐藏前 auto_hide_tooltip 状态: auto_hide={self.auto_hide_tooltip.auto_hide}, is_pinned={self.auto_hide_tooltip.is_pinned if hasattr(self.auto_hide_tooltip, 'is_pinned') else '未定义'}")
            print(f"[调试信息] 隐藏前 auto_hide_tooltip 可见性: {self.auto_hide_tooltip.isVisible()}")
        
        # 强制隐藏所有 Tooltip
        self.basic_tooltip.hideTooltip(0, animation=True, force=True)
        self.auto_hide_tooltip.hideTooltip(0, animation=True, force=True)
        
        # 立即更新状态显示
        self.update_status_display()
        
        # 打印隐藏后状态
        if self.debug_mode:
            print(f"[调试信息] 隐藏后 auto_hide_tooltip 状态: auto_hide={self.auto_hide_tooltip.auto_hide}, is_pinned={self.auto_hide_tooltip.is_pinned if hasattr(self.auto_hide_tooltip, 'is_pinned') else '未定义'}")
            print(f"[调试信息] 隐藏后 auto_hide_tooltip 可见性: {self.auto_hide_tooltip.isVisible()}")
            print("-----------------------------------")

    def toggle_debug_mode(self):
        # 切换调试模式
        self.debug_mode = not self.debug_mode
        self.debug_toggle_btn.setText("调试模式: 开启" if self.debug_mode else "调试模式: 关闭")
        print(f"[系统信息] 调试模式已{'开启' if self.debug_mode else '关闭'}")
    
    def update_status_display(self):
        # 更新状态显示
        if hasattr(self, 'auto_hide_tooltip') and self.auto_hide_tooltip.isVisible():
            is_pinned_text = "固定显示" if hasattr(self.auto_hide_tooltip, 'is_pinned') and self.auto_hide_tooltip.is_pinned else "自动隐藏"
            self.status_label.setText(f"Tooltip状态: 显示中 ({is_pinned_text})")
        else:
            self.status_label.setText("Tooltip状态: 未显示")
        
        # 每500毫秒更新一次状态
        if self.debug_mode:
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(500, self.update_status_display)

if __name__ == "__main__":
    # 启用调试信息
    print("[调试信息] Tooltip测试程序启动")
    print("[调试信息] 调试提示：")
    print("1. 点击'启用 auto_hide'按钮，观察Tooltip显示后鼠标移开时是否自动隐藏")
    print("2. 点击'禁用 auto_hide'按钮，观察Tooltip显示后鼠标移开时是否保持显示")
    print("3. 当Tooltip固定显示时，点击'强制隐藏'按钮，观察是否能强制隐藏")
    print("4. 使用'调试模式'开关控制是否显示详细调试信息")
    print("5. 观察状态显示区域和控制台输出，了解Tooltip的状态变化")
    print("-----------------------------------")
    
    app = QApplication(sys.argv)
    window = TestTooltipWindow()
    window.show()
    
    # 启动状态更新定时器
    window.update_status_display()
    
    sys.exit(app.exec_())