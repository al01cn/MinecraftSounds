from PyQt5.QtCore import Qt, QEvent, QPoint, QTimer, QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QApplication, QGraphicsOpacityEffect
from PyQt5.QtGui import QColor, QPainter, QPen, QFont, QCursor, QIcon, QPixmap
from utils import GetIconSvg
import os
from enum import Enum

class TooltipPosition(Enum):
    """气泡提示组件的显示位置枚举"""
    Top = 'top'
    Bottom = 'bottom'
    Left = 'left'
    Right = 'right'
    TopLeft = 'top-left'
    TopRight = 'top-right'
    BottomLeft = 'bottom-left'
    BottomRight = 'bottom-right'

class TooltipTheme(Enum):
    """气泡提示组件的主题枚举"""
    Dark = 'dark'  # 深色主题
    Light = 'light'  # 浅色主题
    Custom = 'custom'  # 自定义主题

class TooltipStyle:
    """气泡提示组件的样式配置"""
    
    def __init__(self, theme=TooltipTheme.Dark):
        """初始化样式配置"""
        # 设置默认主题
        self.setTheme(theme)
    
    def setTheme(self, theme):
        """设置主题"""
        if theme == TooltipTheme.Dark or theme == 'dark':
            # 深色主题
            self.background_color = QColor(40, 40, 40, 242)  # 背景色
            self.border_color = QColor(85, 85, 85)  # 边框色
            self.text_color = QColor(221, 221, 221)  # 文本色
            self.title_color = QColor(255, 255, 255)  # 标题色
        elif theme == TooltipTheme.Light or theme == 'light':
            # 浅色主题
            self.background_color = QColor(245, 245, 245, 242)  # 背景色
            self.border_color = QColor(200, 200, 200)  # 边框色
            self.text_color = QColor(50, 50, 50)  # 文本色
            self.title_color = QColor(0, 0, 0)  # 标题色
        else:
            # 默认使用深色主题
            self.background_color = QColor(40, 40, 40, 242)  # 背景色
            self.border_color = QColor(85, 85, 85)  # 边框色
            self.text_color = QColor(221, 221, 221)  # 文本色
            self.title_color = QColor(255, 255, 255)  # 标题色
        
        # 其他样式属性
        self.border_radius = 8  # 边框圆角
        self.border_width = 1  # 边框宽度
        self.padding = 10  # 内边距
        self.font_size = 11  # 字体大小
        self.title_font_size = 11  # 标题字体大小
        self.arrow_width = 12  # 箭头宽度
        self.arrow_height = 8  # 箭头高度
        self.min_width = 50  # 最小宽度
        self.max_width = 300  # 最大宽度
        self.min_height = 30  # 最小高度
    
    def setCustomColors(self, background_color, border_color, text_color, title_color=None):
        """设置自定义颜色"""
        self.background_color = background_color
        self.border_color = border_color
        self.text_color = text_color
        self.title_color = title_color if title_color else text_color
    
    def setFontSize(self, font_size, title_font_size=None):
        """设置字体大小"""
        self.font_size = font_size
        self.title_font_size = title_font_size if title_font_size else font_size
    
    def setBorderRadius(self, radius):
        """设置边框圆角"""
        self.border_radius = radius
    
    def setPadding(self, padding):
        """设置内边距"""
        self.padding = padding
    
    def setArrowSize(self, width, height):
        """设置箭头大小"""
        self.arrow_width = width
        self.arrow_height = height
    
    def setWidth(self, min_width, max_width):
        """设置宽度范围"""
        self.min_width = min_width
        self.max_width = max_width

class Tooltip(QWidget):
    """通用气泡提示组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent, Qt.ToolTip | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        
        # 初始化样式
        self.style = TooltipStyle()
        
        # 初始化UI
        self.initUI()
        
        # 设置定时器，用于鼠标离开后延迟隐藏
        self.hideTimer = QTimer(self)
        self.hideTimer.setSingleShot(True)
        self.hideTimer.timeout.connect(self.hide)
        
        # 设置动画效果
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)
        
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(150)  # 150毫秒的动画时长
        self.fade_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # 垂直偏移量（正值向上偏移，负值向下偏移）
        self.vertical_offset = 3
        
        # 默认隐藏
        self.hide()
    
    def initUI(self):
        # 创建主布局
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(self.style.padding, self.style.padding, self.style.padding, self.style.padding)
        self.mainLayout.setSpacing(5)
        
        # 创建内容标签
        self.contentLabel = QLabel()
        self.contentLabel.setWordWrap(True)  # 允许文本换行
        self.updateStyle()
        
        # 添加组件到主布局
        self.mainLayout.addWidget(self.contentLabel)
    
    def updateStyle(self):
        """更新样式"""
        # 设置内容标签样式
        self.contentLabel.setStyleSheet(
            f"color: {self.style.text_color.name()}; font-size: {self.style.font_size}px;"
        )
        
        # 设置最小和最大宽度
        self.setMinimumWidth(self.style.min_width)
        self.setMaximumWidth(self.style.max_width)
        self.setMinimumHeight(self.style.min_height)
    
    def setStyle(self, style):
        """设置样式"""
        self.style = style
        self.updateStyle()
        self.update()  # 触发重绘
    
    def setTheme(self, theme):
        """设置主题"""
        self.style.setTheme(theme)
        self.updateStyle()
        self.update()  # 触发重绘
    
    def paintEvent(self, event):
        """重写绘制事件，添加气泡尖角，尖角始终指向目标位置"""
        # 创建画笔
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        
        # 设置画笔颜色
        painter.setPen(QPen(self.style.border_color, self.style.border_width))
        painter.setBrush(self.style.background_color)
        
        # 获取当前的显示位置
        position = getattr(self, 'position', 'bottom')
        
        # 获取指向点的位置（相对于tooltip的坐标）
        target_point = getattr(self, 'target_point', QPoint(self.width() // 2, self.height() // 2))
        
        # 绘制小三角形指向图标
        triangle_width = self.style.arrow_width
        triangle_height = self.style.arrow_height
        
        # 根据位置计算气泡矩形区域和三角形位置
        rect = self.rect()
        points = []
        
        if position == 'bottom':
            # 三角形在底部，尖角指向目标位置
            bubble_rect = rect.adjusted(0, triangle_height, 0, 0)
            # 计算尖角水平位置
            arrow_x = target_point.x()
            # 确保尖角不会太靠近边缘
            arrow_x = max(triangle_width, min(arrow_x, self.width() - triangle_width))
            
            points = [
                QPoint(arrow_x - triangle_width // 2, triangle_height),  # 左下
                QPoint(arrow_x + triangle_width // 2, triangle_height),  # 右下
                QPoint(arrow_x, 0)  # 顶部尖角
            ]
        elif position == 'top':
            # 三角形在顶部，尖角指向目标位置
            bubble_rect = rect.adjusted(0, 0, 0, -triangle_height)
            # 计算尖角水平位置（相对于tooltip左边缘的距离）
            arrow_x = target_point.x()
            # 确保尖角不会太靠近边缘
            arrow_x = max(triangle_width, min(arrow_x, self.width() - triangle_width))
            
            points = [
                QPoint(arrow_x - triangle_width // 2, self.height() - triangle_height),  # 左上
                QPoint(arrow_x + triangle_width // 2, self.height() - triangle_height),  # 右上
                QPoint(arrow_x, self.height())  # 底部尖角
            ]
        elif position == 'right':
            # 三角形在右侧，尖角指向目标位置
            bubble_rect = rect.adjusted(triangle_height, 0, 0, 0)
            # 计算尖角垂直位置
            arrow_y = target_point.y()
            # 确保尖角不会太靠近边缘
            arrow_y = max(triangle_width, min(arrow_y, self.height() - triangle_width))
            
            points = [
                QPoint(triangle_height, arrow_y - triangle_width // 2),  # 右上
                QPoint(triangle_height, arrow_y + triangle_width // 2),  # 右下
                QPoint(0, arrow_y)  # 左侧尖角
            ]
        elif position == 'left':
            # 三角形在左侧，尖角指向目标位置
            bubble_rect = rect.adjusted(0, 0, -triangle_height, 0)
            # 计算尖角垂直位置
            arrow_y = target_point.y()
            # 确保尖角不会太靠近边缘
            arrow_y = max(triangle_width, min(arrow_y, self.height() - triangle_width))
            
            points = [
                QPoint(self.width() - triangle_height, arrow_y - triangle_width // 2),  # 左上
                QPoint(self.width() - triangle_height, arrow_y + triangle_width // 2),  # 左下
                QPoint(self.width(), arrow_y)  # 右侧尖角
            ]
        elif position == 'top-left':
            # 三角形在左下角，尖角指向目标位置
            bubble_rect = rect.adjusted(0, 0, 0, -triangle_height)
            # 计算尖角水平位置，默认距离左边20像素，但可以根据target_point调整
            arrow_x = min(target_point.x(), self.width() // 4)
            # 确保尖角不会太靠近边缘
            arrow_x = max(triangle_width, min(arrow_x, self.width() // 2 - triangle_width))
            
            points = [
                QPoint(arrow_x - triangle_width // 2, self.height() - triangle_height),  # 左上
                QPoint(arrow_x + triangle_width // 2, self.height() - triangle_height),  # 右上
                QPoint(arrow_x, self.height())  # 底部尖角
            ]
        elif position == 'top-right':
            # 三角形在右下角，尖角指向目标位置
            bubble_rect = rect.adjusted(0, 0, 0, -triangle_height)
            # 计算尖角水平位置，默认距离右边20像素，但可以根据target_point调整
            arrow_x = max(target_point.x(), self.width() * 3 // 4)
            # 确保尖角不会太靠近边缘
            arrow_x = max(self.width() // 2 + triangle_width, min(arrow_x, self.width() - triangle_width))
            
            points = [
                QPoint(arrow_x - triangle_width // 2, self.height() - triangle_height),  # 左上
                QPoint(arrow_x + triangle_width // 2, self.height() - triangle_height),  # 右上
                QPoint(arrow_x, self.height())  # 底部尖角
            ]
        elif position == 'bottom-left':
            # 三角形在左上角，尖角指向目标位置
            bubble_rect = rect.adjusted(0, triangle_height, 0, 0)
            # 计算尖角水平位置，默认距离左边20像素，但可以根据target_point调整
            arrow_x = min(target_point.x(), self.width() // 4)
            # 确保尖角不会太靠近边缘
            arrow_x = max(triangle_width, min(arrow_x, self.width() // 2 - triangle_width))
            
            points = [
                QPoint(arrow_x - triangle_width // 2, triangle_height),  # 左下
                QPoint(arrow_x + triangle_width // 2, triangle_height),  # 右下
                QPoint(arrow_x, 0)  # 顶部尖角
            ]
        elif position == 'bottom-right':
            # 三角形在右上角，尖角指向目标位置
            bubble_rect = rect.adjusted(0, triangle_height, 0, 0)
            # 计算尖角水平位置，默认距离右边20像素，但可以根据target_point调整
            arrow_x = max(target_point.x(), self.width() * 3 // 4)
            # 确保尖角不会太靠近边缘
            arrow_x = max(self.width() // 2 + triangle_width, min(arrow_x, self.width() - triangle_width))
            
            points = [
                QPoint(arrow_x - triangle_width // 2, triangle_height),  # 左下
                QPoint(arrow_x + triangle_width // 2, triangle_height),  # 右下
                QPoint(arrow_x, 0)  # 顶部尖角
            ]
        
        # 绘制气泡主体（圆角矩形）
        painter.drawRoundedRect(bubble_rect, self.style.border_radius, self.style.border_radius)
        
        # 绘制三角形
        if points:
            painter.drawPolygon(points)
    
    def setContent(self, title, content):
        """设置Tooltip的内容"""
        # 显示标题和内容
        display_text = ""
        
        # 如果有标题，添加标题
        if title:
            display_text += f"<span style='color: {self.style.title_color.name()}; font-size: {self.style.title_font_size}px;'><b>{title}</b></span>"
            
            # 如果同时有标题和内容，添加换行
            if content:
                display_text += "<br><br>"
        
        # 添加内容
        if content:
            display_text += f"<span style='color: {self.style.text_color.name()};'>{content}</span>"
        
        # 设置文本，支持HTML格式
        self.contentLabel.setText(display_text)
        
        # 调整大小以适应内容
        self.adjustSize()
    
    def showTooltip(self, pos, title, content, preferred_position=None, target_pos=None, animation=True, auto_hide=True):
        """在指定位置显示Tooltip，自动调整位置以避免超出屏幕边界
        
        参数:
            pos: 显示位置
            title: 标题
            content: 内容
            preferred_position: 首选位置
            target_pos: 目标位置（箭头指向的位置）
            animation: 是否使用动画效果
            auto_hide: 是否启用自动隐藏功能，如果为False，则鼠标离开时不会自动隐藏
        """
        # 设置内容
        self.setContent(title, content)
        
        # 获取tooltip尺寸
        tooltip_width = self.sizeHint().width()
        tooltip_height = self.sizeHint().height()
        
        # 如果没有指定目标位置，则使用pos作为目标位置
        if target_pos is None:
            target_pos = pos
        
        # 获取屏幕几何信息
        screen_rect = QApplication.desktop().screenGeometry(QCursor.pos())
        
        # 获取窗口信息（如果有父窗口）
        window_rect = None
        parent_widget = self.parent()
        while parent_widget:
            if parent_widget.isWindow():
                window_rect = parent_widget.geometry()
                window_rect.moveTopLeft(parent_widget.mapToGlobal(parent_widget.rect().topLeft()))
                break
            parent_widget = parent_widget.parent()
        
        # 三角形高度（用于位置调整）
        triangle_height = self.style.arrow_height
        
        # 确定最佳显示位置
        # 如果是枚举类型，获取其值
        if isinstance(preferred_position, TooltipPosition):
            preferred_position = preferred_position.value
        
        # 保存原始首选位置
        original_preferred_position = preferred_position
        position = preferred_position if preferred_position else 'top'
        
        # 检查各个方向的空间并选择最佳位置
        # 如果有窗口信息，则考虑窗口边界
        if window_rect:
            space_top = pos.y() - max(screen_rect.top(), window_rect.top())
            space_bottom = min(screen_rect.bottom(), window_rect.bottom()) - pos.y()
            space_left = pos.x() - max(screen_rect.left(), window_rect.left())
            space_right = min(screen_rect.right(), window_rect.right()) - pos.x()
        else:
            space_top = pos.y() - screen_rect.top()
            space_bottom = screen_rect.bottom() - pos.y()
            space_left = pos.x() - screen_rect.left()
            space_right = screen_rect.right() - pos.x()
        
        # 检查首选位置是否有足够空间，如果没有则自动调整
        if preferred_position:
            # 检查首选位置是否有足够空间
            if position.startswith('top') and space_top < tooltip_height + triangle_height:
                # 上方空间不足，尝试下方
                if space_bottom >= tooltip_height + triangle_height:
                    position = position.replace('top', 'bottom')
                # 如果下方也不足，尝试左右
                elif space_left >= tooltip_width + triangle_height:
                    position = 'left'
                elif space_right >= tooltip_width + triangle_height:
                    position = 'right'
            elif position.startswith('bottom') and space_bottom < tooltip_height + triangle_height:
                # 下方空间不足，尝试上方
                if space_top >= tooltip_height + triangle_height:
                    position = position.replace('bottom', 'top')
                # 如果上方也不足，尝试左右
                elif space_left >= tooltip_width + triangle_height:
                    position = 'left'
                elif space_right >= tooltip_width + triangle_height:
                    position = 'right'
            elif position == 'left' and space_left < tooltip_width + triangle_height:
                # 左侧空间不足，尝试右侧
                if space_right >= tooltip_width + triangle_height:
                    position = 'right'
                # 如果右侧也不足，尝试上下
                elif space_top >= tooltip_height + triangle_height:
                    position = 'top'
                elif space_bottom >= tooltip_height + triangle_height:
                    position = 'bottom'
            elif position == 'right' and space_right < tooltip_width + triangle_height:
                # 右侧空间不足，尝试左侧
                if space_left >= tooltip_width + triangle_height:
                    position = 'left'
                # 如果左侧也不足，尝试上下
                elif space_top >= tooltip_height + triangle_height:
                    position = 'top'
                elif space_bottom >= tooltip_height + triangle_height:
                    position = 'bottom'
        else:
            # 如果没有指定首选位置，则自动选择最佳位置
            # 优先选择上方，如果空间不足则选择其他方向
            if space_top >= tooltip_height + triangle_height:
                position = 'top'
            elif space_bottom >= tooltip_height + triangle_height:
                position = 'bottom'
            elif space_right >= tooltip_width + triangle_height:
                position = 'right'
            elif space_left >= tooltip_width + triangle_height:
                position = 'left'
            else:
                # 如果所有方向都空间不足，选择空间最大的方向
                max_space = max(space_top, space_bottom, space_left, space_right)
                if max_space == space_top:
                    position = 'top'
                elif max_space == space_bottom:
                    position = 'bottom'
                elif max_space == space_left:
                    position = 'left'
                else:
                    position = 'right'
        
        # 根据位置计算tooltip的坐标
        x, y = pos.x(), pos.y()
        
        # 根据位置调整坐标，确保tooltip的尖角始终指向图标
        if position.startswith('top'):
            # TopLeft和TopRight应该显示在上方，与Top一致
            y = pos.y() - tooltip_height - triangle_height - self.vertical_offset  # 根据垂直偏移量调整
                
            if position == 'top-left':
                x = pos.x() - 20  # 左对齐，偏移20像素
            elif position == 'top-right':
                x = pos.x() - tooltip_width + 20  # 右对齐，偏移20像素
            else:  # top
                x = pos.x() - tooltip_width // 2  # 水平居中
        elif position.startswith('bottom'):
            # BottomLeft和BottomRight应该显示在下方，与Bottom一致
            y = pos.y() + triangle_height - self.vertical_offset  # 根据垂直偏移量调整
                
            if position == 'bottom-left':
                x = pos.x() - 20  # 左对齐，偏移20像素
            elif position == 'bottom-right':
                x = pos.x() - tooltip_width + 20  # 右对齐，偏移20像素
            else:  # bottom
                x = pos.x() - tooltip_width // 2  # 水平居中
        elif position == 'left':
            x = pos.x() - tooltip_width - triangle_height
            y = pos.y() - tooltip_height // 2 - self.vertical_offset  # 垂直居中，根据垂直偏移量调整
        elif position == 'right':
            x = pos.x() + triangle_height
            y = pos.y() - tooltip_height // 2 - self.vertical_offset  # 垂直居中，根据垂直偏移量调整
        
        # 计算target_point（相对于tooltip的坐标）
        # 这是气泡尖角指向的位置，相对于tooltip左上角的坐标
        target_x = target_pos.x() - x
        target_y = target_pos.y() - y
        self.target_point = QPoint(target_x, target_y)
        
        # 确保tooltip不会超出屏幕和窗口边界
        # 确定边界
        left_bound = screen_rect.left() + 10
        right_bound = screen_rect.right() - 10
        top_bound = screen_rect.top() + 10
        bottom_bound = screen_rect.bottom() - 10
        
        # 如果有窗口信息，则考虑窗口边界
        if window_rect:
            left_bound = max(left_bound, window_rect.left() + 10)
            right_bound = min(right_bound, window_rect.right() - 10)
            top_bound = max(top_bound, window_rect.top() + 10)
            bottom_bound = min(bottom_bound, window_rect.bottom() - 10)
        
        # 应用边界限制
        if x < left_bound:
            x = left_bound
            # 如果左侧空间不足，可能需要调整位置
            if position in ['right', 'top-right', 'bottom-right']:
                position = position.replace('right', 'left')
        if x + tooltip_width > right_bound:
            x = right_bound - tooltip_width
            # 如果右侧空间不足，可能需要调整位置
            if position in ['left', 'top-left', 'bottom-left']:
                position = position.replace('left', 'right')
        if y < top_bound:
            y = top_bound
            # 如果上方空间不足，切换到底部
            if position.startswith('bottom'):
                position = position.replace('bottom', 'top')
                y = pos.y() - tooltip_height - triangle_height
        if y + tooltip_height > bottom_bound:
            y = bottom_bound - tooltip_height
            # 如果下方空间不足，切换到顶部
            if position.startswith('top'):
                position = position.replace('top', 'bottom')
                y = pos.y() + triangle_height
        
        # 如果位置发生了变化，需要重新计算坐标
        if position != original_preferred_position and original_preferred_position:
            # 根据新位置重新计算坐标
            if position.startswith('top'):
                # 所有top位置都应该显示在上方
                y = pos.y() - tooltip_height - triangle_height - self.vertical_offset  # 根据垂直偏移量调整
                if position == 'top-left':
                    x = pos.x() - 20
                elif position == 'top-right':
                    x = pos.x() - tooltip_width + 20
                else:  # top
                    x = pos.x() - tooltip_width // 2
            elif position.startswith('bottom'):
                # 所有bottom位置都应该显示在下方
                y = pos.y() + triangle_height - self.vertical_offset  # 根据垂直偏移量调整
                if position == 'bottom-left':
                    x = pos.x() - 20
                elif position == 'bottom-right':
                    x = pos.x() - tooltip_width + 20
                else:  # bottom
                    x = pos.x() - tooltip_width // 2
            elif position == 'left':
                x = pos.x() - tooltip_width - triangle_height
                y = pos.y() - tooltip_height // 2 - self.vertical_offset  # 根据垂直偏移量调整
            elif position == 'right':
                x = pos.x() + triangle_height
                y = pos.y() - tooltip_height // 2 - self.vertical_offset  # 根据垂直偏移量调整
            
            # 再次确保不超出屏幕边界
            x = max(min(x, screen_rect.right() - tooltip_width - 10), screen_rect.left() + 10)
            y = max(min(y, screen_rect.bottom() - tooltip_height - 10), screen_rect.top() + 10)
            
            # 重新计算target_point（相对于tooltip的坐标）
            target_x = target_pos.x() - x
            target_y = target_pos.y() - y
            self.target_point = QPoint(target_x, target_y)
        
        # 保存当前位置，用于paintEvent绘制
        self.position = position
        
        # 保存auto_hide参数，用于leaveEvent判断是否自动隐藏
        self.auto_hide = auto_hide
        
        # 设置属性，用于标识tooltip是否处于固定状态（不会自动隐藏）
        self.is_pinned = not auto_hide
        
        # 确保停止任何正在进行的隐藏定时器
        self.hideTimer.stop()
        
        # 设置位置
        self.move(x, y)
        
        # 显示带动画效果
        if animation:
            self.show()
            self.fade_animation.setStartValue(0.0)
            self.fade_animation.setEndValue(1.0)
            self.fade_animation.start()
        else:
            self.opacity_effect.setOpacity(1.0)
            self.show()
        
        # 停止之前的隐藏定时器
        self.hideTimer.stop()
    
    def hideTooltip(self, delay=300, animation=True, force=False):
        """延迟隐藏Tooltip
        
        参数:
            delay: 延迟隐藏的时间（毫秒）
            animation: 是否使用动画效果
            force: 是否强制隐藏，即使auto_hide为False也隐藏
        """
        # 如果禁用自动隐藏且不是强制隐藏，则直接返回
        if not force and (not getattr(self, 'auto_hide', True) or getattr(self, 'is_pinned', False)):
            return
            
        if animation:
            # 使用动画效果隐藏
            def start_hide_animation():
                self.fade_animation.setStartValue(1.0)
                self.fade_animation.setEndValue(0.0)
                self.fade_animation.finished.connect(self.hide)
                self.fade_animation.start()
            
            self.hideTimer.timeout.disconnect()
            self.hideTimer.timeout.connect(start_hide_animation)
            self.hideTimer.start(delay)
        else:
            # 直接隐藏
            self.hideTimer.timeout.disconnect()
            self.hideTimer.timeout.connect(self.hide)
            self.hideTimer.start(delay)
    
    def setVerticalOffset(self, offset):
        """设置垂直偏移量"""
        self.vertical_offset = offset
    
    def enterEvent(self, event):
        # 鼠标进入Tooltip区域时，停止隐藏定时器
        self.hideTimer.stop()
        # 如果tooltip不是固定状态，则设置auto_hide为True
        if not getattr(self, 'is_pinned', False):
            self.auto_hide = True
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        # 鼠标离开Tooltip区域时，启动隐藏定时器
        # 检查鼠标是否真的离开了Tooltip区域
        mouse_pos = QCursor.pos()
        tooltip_rect = self.geometry()
        tooltip_rect.moveTopLeft(self.mapToGlobal(QPoint(0, 0)))
        
        # 如果鼠标仍在Tooltip区域内，不隐藏
        if tooltip_rect.contains(mouse_pos):
            return
        
        # 获取auto_hide属性和is_pinned属性
        auto_hide = getattr(self, 'auto_hide', True)
        is_pinned = getattr(self, 'is_pinned', False)
        
        # 只有当auto_hide为True且tooltip不是固定状态时才隐藏tooltip
        if auto_hide and not is_pinned:
            self.hideTooltip(300)  # 恢复默认的300毫秒延迟
        super().leaveEvent(event)


class TooltipWidget(QWidget):
    """带有Tooltip功能的基础组件"""
    
    def __init__(self, tooltip_title="", tooltip_content="", preferred_position=None, vertical_offset=3, parent=None):
        """初始化TooltipWidget组件"""
        super().__init__(parent)
        
        # 保存Tooltip内容
        self.tooltip_title = tooltip_title
        self.tooltip_content = tooltip_content
        self.preferred_position = preferred_position.value if isinstance(preferred_position, TooltipPosition) else preferred_position
        
        # 创建自定义Tooltip，将自己设置为Tooltip的父组件
        self.tooltip = Tooltip(self)
        # 设置垂直偏移量
        self.tooltip.setVerticalOffset(vertical_offset)
        
        # 设置事件追踪
        self.setMouseTracking(True)
    
    def setTooltipContent(self, title, content):
        """设置Tooltip内容"""
        self.tooltip_title = title
        self.tooltip_content = content
    
    def setTooltipStyle(self, style):
        """设置Tooltip样式"""
        self.tooltip.setStyle(style)
    
    def setTooltipTheme(self, theme):
        """设置Tooltip主题"""
        self.tooltip.setTheme(theme)
    
    def setVerticalOffset(self, offset):
        """设置Tooltip垂直偏移量"""
        self.tooltip.setVerticalOffset(offset)
    
    def setPreferredPosition(self, position):
        """设置Tooltip首选显示位置"""
        self.preferred_position = position.value if isinstance(position, TooltipPosition) else position
    
    def enterEvent(self, event):
        """鼠标进入事件，显示Tooltip"""
        if self.tooltip_title or self.tooltip_content:
            # 获取组件中心位置
            widget_pos = self.mapToGlobal(QPoint(self.width() // 2, self.height() // 2))
            
            # 使用首选位置或默认位置
            position = self.preferred_position
            if not position:
                # 默认在组件上方显示tooltip
                position = 'top'
            
            # 停止任何正在进行的隐藏定时器
            self.tooltip.hideTimer.stop()
            
            # 显示Tooltip，使用确定的位置，并传递组件中心位置作为target_pos
            # 设置auto_hide为True，允许鼠标离开时自动隐藏
            self.tooltip.showTooltip(widget_pos, self.tooltip_title, self.tooltip_content, position, target_pos=widget_pos, auto_hide=True)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """鼠标离开事件，隐藏Tooltip"""
        # 检查鼠标是否真的离开了组件
        # 获取鼠标当前位置
        mouse_pos = QCursor.pos()
        # 获取组件的全局几何区域
        widget_rect = self.geometry()
        widget_rect.moveTopLeft(self.mapToGlobal(QPoint(0, 0)))
        
        # 如果鼠标仍在组件内，不隐藏tooltip
        if widget_rect.contains(mouse_pos):
            return
        
        # 获取tooltip的auto_hide属性，如果未设置，默认为True
        auto_hide = getattr(self.tooltip, 'auto_hide', True)
        
        # 只有当auto_hide为True时才隐藏tooltip
        # 我们在enterEvent中已经设置auto_hide为True，所以这里会隐藏tooltip
        if auto_hide:
            self.tooltip.hideTooltip()
        super().leaveEvent(event)


class TooltipIcon(TooltipWidget):
    """带有Tooltip功能的图标组件"""
    
    def __init__(self, icon_name="SolarInfoCircleOutline", tooltip_title="", tooltip_content="", preferred_position=None, vertical_offset=3, parent=None):
        """初始化TooltipIcon组件"""
        super().__init__(tooltip_title, tooltip_content, preferred_position, vertical_offset, parent)
        
        # 设置布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建图标标签
        self.iconLabel = QLabel(self)
        self.iconLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.iconLabel)
        
        # 设置图标
        self.setIcon(icon_name)
        
        # 设置鼠标样式
        self.setCursor(QCursor(Qt.WhatsThisCursor))
    
    def setIcon(self, icon_name):
        """设置图标"""
        # 使用GetIconSvg函数获取图标
        icon = GetIconSvg(icon_name, icon=False)
        
        # 设置图标
        if icon and icon != "" and os.path.exists(icon):
            self.iconLabel.setPixmap(GetIconSvg(icon_name).pixmap(16, 16))
        else:
            # 如果图标不存在，使用文本"i"作为替代
            self.iconLabel.setText("i")
            self.iconLabel.setStyleSheet(
                "background-color: #FFD700; color: #000000; border-radius: 8px; "
                "padding: 2px; min-width: 16px; min-height: 16px; "
                "max-width: 16px; max-height: 16px; text-align: center;"
            )
        
        # 设置固定大小
        self.setFixedSize(16, 16)
    
    def mousePressEvent(self, event):
        """鼠标点击事件，切换Tooltip显示状态"""
        if event.button() == Qt.LeftButton:
            if self.tooltip.isVisible():
                # 如果tooltip已经显示，则隐藏它（强制隐藏）
                self.tooltip.hideTooltip(0, animation=True, force=True)
            else:
                # 获取图标中心位置
                icon_pos = self.mapToGlobal(QPoint(self.width() // 2, self.height() // 2))
                
                # 使用首选位置或默认位置
                position = self.preferred_position
                if not position:
                    # 默认在图标上方显示tooltip
                    position = 'top'
                
                # 停止任何正在进行的隐藏定时器
                self.tooltip.hideTimer.stop()
                
                # 显示Tooltip，使用确定的位置，并传递图标中心位置作为target_pos
                # 设置auto_hide为False，使tooltip在鼠标不移开时保持显示（固定状态）
                self.tooltip.showTooltip(icon_pos, self.tooltip_title, self.tooltip_content, position, target_pos=icon_pos, auto_hide=False)
                # 设置tooltip为固定状态
                self.tooltip.is_pinned = True
        super().mousePressEvent(event)


class TooltipLabel(QWidget):
    """带有Tooltip图标的标签组件"""
    
    def __init__(self, label_text, tooltip_title="", tooltip_content="", icon_name="SolarInfoCircleOutline", preferred_position=None, vertical_offset=3, parent=None):
        """初始化TooltipLabel组件"""
        super().__init__(parent)
        
        # 创建布局
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # 创建标签
        self.label = QLabel(label_text)
        
        # 创建Tooltip图标
        self.icon = TooltipIcon(icon_name, tooltip_title, tooltip_content, preferred_position, vertical_offset)
        
        # 添加组件到布局
        layout.addWidget(self.icon)
        layout.addWidget(self.label)
        layout.addStretch()
        
        # 设置布局
        self.setLayout(layout)
    
    def setText(self, text):
        """设置标签文本"""
        self.label.setText(text)
    
    def setTooltipContent(self, title, content, preferred_position=None):
        """设置Tooltip内容"""
        self.icon.setTooltipContent(title, content)
        if preferred_position is not None:
            self.icon.setPreferredPosition(preferred_position)
    
    def setTooltipStyle(self, style):
        """设置Tooltip样式"""
        self.icon.setTooltipStyle(style)
    
    def setTooltipTheme(self, theme):
        """设置Tooltip主题"""
        self.icon.setTooltipTheme(theme)
    
    def setVerticalOffset(self, offset):
        """设置Tooltip垂直偏移量"""
        self.icon.setVerticalOffset(offset)


# 为了向后兼容，保留原来的类名
CustomTooltip = Tooltip
PreferredPosition = TooltipPosition