from PyQt5.QtCore import Qt, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QTextEdit, QFileDialog
import os
import shutil
import time
import subprocess

from core.minecraft.projectPath import ProjectPath
from gui.ui import MinecraftFrame, MinecraftLabel, apply_minecraft_style
from gui.ui.button import MinecraftPixelButton
from gui.ui.minecraft_dialog import MinecraftMessageBox
from utils import toOgg, copyFile, getProject

class ExportStep(QWidget):
    """导出步骤组件"""
    def __init__(self, step_number, title, parent=None):
        super().__init__(parent)
        self.step_number = step_number
        self.title = title
        self.is_active = False
        self.is_completed = False
        
        # 创建布局
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 10, 5)
        self.layout.setSpacing(10)
        
        # 创建步骤数字标签
        self.numberLabel = MinecraftLabel(str(step_number))
        self.numberLabel.setFixedSize(30, 30)
        self.numberLabel.setAlignment(Qt.AlignCenter)
        self.numberLabel.setStyleSheet("""
            QLabel {
                background-color: #555555;
                border: 2px solid #333333;
                border-radius: 15px;
                color: #FFFFFF;
                font-weight: bold;
            }
        """)
        
        # 创建标题标签
        self.titleLabel = MinecraftLabel(title)
        self.titleLabel.setStyleSheet("""
            QLabel {
                color: #AAAAAA;
                font-size: 16px;
            }
        """)
        
        # 添加组件到布局
        self.layout.addWidget(self.numberLabel)
        self.layout.addWidget(self.titleLabel)
        self.layout.addStretch(1)
    
    def setActive(self, active):
        """设置步骤是否激活"""
        self.is_active = active
        if active:
            self.numberLabel.setStyleSheet("""
                QLabel {
                    background-color: #5555FF;
                    border: 2px solid #3333AA;
                    border-radius: 15px;
                    color: #FFFFFF;
                    font-weight: bold;
                }
            """)
            self.titleLabel.setStyleSheet("""
                QLabel {
                    color: #FFFFFF;
                    font-size: 16px;
                    font-weight: bold;
                }
            """)
        else:
            if self.is_completed:
                self.setCompleted(True)
            else:
                self.numberLabel.setStyleSheet("""
                    QLabel {
                        background-color: #555555;
                        border: 2px solid #333333;
                        border-radius: 15px;
                        color: #FFFFFF;
                        font-weight: bold;
                    }
                """)
                self.titleLabel.setStyleSheet("""
                    QLabel {
                        color: #AAAAAA;
                        font-size: 16px;
                    }
                """)
    
    def setCompleted(self, completed):
        """设置步骤是否完成"""
        self.is_completed = completed
        if completed:
            self.numberLabel.setStyleSheet("""
                QLabel {
                    background-color: #55AA55;
                    border: 2px solid #338833;
                    border-radius: 15px;
                    color: #FFFFFF;
                    font-weight: bold;
                }
            """)
            self.titleLabel.setStyleSheet("""
                QLabel {
                    color: #AAAAAA;
                    font-size: 16px;
                }
            """)

class ExportWorker(QThread):
    """导出工作线程"""
    # 信号定义
    step_started = pyqtSignal(int)  # 步骤开始信号
    step_completed = pyqtSignal(int)  # 步骤完成信号
    progress_updated = pyqtSignal(int, int)  # 进度更新信号 (当前值, 最大值)
    log_message = pyqtSignal(str)  # 日志消息信号
    export_completed = pyqtSignal(bool, str)  # 导出完成信号 (是否成功, 错误消息)
    
    def __init__(self, project_path: ProjectPath, audio_files):
        super().__init__()
        self.project_path = project_path  # ProjectPath对象
        self.audio_files = audio_files  # 音频文件列表
        self.is_running = False
        self.is_canceled = False
        self.audio_soundkeys = {}  # 存储音频文件与soundkey的映射关系
        self.audio_categories = {}  # 存储音频文件与分类的映射关系
    
    def run(self):
        """线程运行函数"""
        self.is_running = True
        self.is_canceled = False
        
        try:
            import os
            # 步骤1: 转换格式
            self.step_started.emit(1)
            self.log_message.emit("开始转换音频格式...")
            
            # 确保缓存目录存在
            cache_src_dir = self.project_path.cacheSrc()
            cache_dist_dir = self.project_path.cacheDist()
            if not os.path.exists(cache_dist_dir):
                os.makedirs(cache_dist_dir, mode=0o755)  # 设置读写权限
            
            # 转换音频格式
            total_files = len(self.audio_files)
            self.progress_updated.emit(0, total_files)
            
            for i, file_path in enumerate(self.audio_files):
                if self.is_canceled:
                    return
                
                file_name = os.path.basename(file_path)
                self.log_message.emit(f"正在处理: {file_path}")
                
                # 获取soundkey作为输出文件名
                sound_key = self.audio_soundkeys.get(file_path, '')
                if not sound_key:
                    # 如果没有找到soundkey，尝试从音频配置文件中获取
                    try:
                        import json
                        sounds_json_path = self.project_path.cacheConfig()
                        if os.path.exists(sounds_json_path):
                            with open(sounds_json_path, 'r', encoding='utf-8') as f:
                                audio_info = json.load(f)
                            # 查找匹配的文件名
                            if file_name in audio_info and audio_info[file_name].get('sound_key'):
                                sound_key = audio_info[file_name]['sound_key']
                                self.log_message.emit(f"从音频配置文件获取到soundKey: {sound_key}")
                            else:
                                # 如果在配置文件中没找到，使用文件名（不含扩展名）
                                sound_key = os.path.splitext(file_name)[0]
                                self.log_message.emit(f"警告: 未在音频配置文件中找到音频文件的soundKey，将使用文件名: {sound_key}")
                        else:
                            # 如果配置文件不存在，使用文件名（不含扩展名）
                            sound_key = os.path.splitext(file_name)[0]
                            self.log_message.emit(f"警告: 音频配置文件不存在，将使用文件名作为soundKey: {sound_key}")
                    except Exception as e:
                        # 如果出现异常，使用文件名（不含扩展名）
                        sound_key = os.path.splitext(file_name)[0]
                        self.log_message.emit(f"警告: 获取音频配置文件失败: {str(e)}，将使用文件名作为soundKey: {sound_key}")
                
                try:
                    # 获取分类信息
                    category = self.audio_categories.get(file_path, '')
                    
                    # 获取文件相对于cache/src的路径
                    rel_path = os.path.relpath(os.path.dirname(file_path), cache_src_dir) if os.path.dirname(file_path) != cache_src_dir else ''
                    
                    # 如果有分类，创建分类子目录
                    if category:
                        category_dir = os.path.join(cache_dist_dir, category)
                        if not os.path.exists(category_dir):
                            os.makedirs(category_dir, mode=0o755)  # 设置读写权限
                            self.log_message.emit(f"创建分类目录: {category}")
                        
                        # 如果有子目录，创建子目录
                        if rel_path and rel_path != '.':
                            sub_dir = os.path.join(category_dir, rel_path)
                            if not os.path.exists(sub_dir):
                                os.makedirs(sub_dir, mode=0o755)  # 设置读写权限
                                self.log_message.emit(f"创建子目录: {category}/{rel_path}")
                            output_path = os.path.join(sub_dir, f"{sound_key}.ogg")
                        else:
                            output_path = os.path.join(category_dir, f"{sound_key}.ogg")
                    else:
                        # 没有分类，但可能有子目录
                        if rel_path and rel_path != '.':
                            sub_dir = os.path.join(cache_dist_dir, rel_path)
                            if not os.path.exists(sub_dir):
                                os.makedirs(sub_dir, mode=0o755)  # 设置读写权限
                                self.log_message.emit(f"创建子目录: {rel_path}")
                            output_path = os.path.join(sub_dir, f"{sound_key}.ogg")
                        else:
                            # 没有子目录，直接放在dist根目录
                            output_path = os.path.join(cache_dist_dir, f"{sound_key}.ogg")
                    
                    # 如果不是ogg格式，转换为ogg格式
                    if not file_path.lower().endswith('.ogg'):
                        toOgg(file_path, output_path, quality="192k", overwrite=True)
                        self.log_message.emit(f"已转换: {file_name} -> {category+'/' if category else ''}{sound_key}.ogg")
                    else:
                        # 如果已经是ogg格式，直接复制到dist目录并重命名
                        copyFile(file_path, output_path)
                        self.log_message.emit(f"已复制并重命名: {file_name} -> {category+'/' if category else ''}{sound_key}.ogg")
                except Exception as e:
                    self.log_message.emit(f"处理失败: {file_name} - {str(e)}")
                
                self.progress_updated.emit(i + 1, total_files)
            
            self.step_completed.emit(1)
            
            # 步骤2: 移动文件到sounds目录
            self.step_started.emit(2)
            self.log_message.emit("开始移动文件到sounds目录...")
            
            # 获取sounds目录
            sounds_dir = self.project_path.sounds()
            if not os.path.exists(sounds_dir):
                os.makedirs(sounds_dir, mode=0o755)  # 设置读写权限
            else:
                # 清空sounds目录中的所有文件和子目录
                self.log_message.emit("正在清空sounds目录...")
                for item in os.listdir(sounds_dir):
                    item_path = os.path.join(sounds_dir, item)
                    try:
                        if os.path.isfile(item_path):
                            os.unlink(item_path)
                            self.log_message.emit(f"已删除文件: {item}")
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                            self.log_message.emit(f"已删除目录: {item}")
                    except Exception as e:
                        self.log_message.emit(f"清空sounds目录时出错: {str(e)}")
                self.log_message.emit("sounds目录已清空")
            
            # 获取dist目录中的所有ogg文件（包括子目录）
            ogg_files = []
            categories = set()
            
            # 递归遍历目录中的ogg文件
            def collect_ogg_files(directory, category='', rel_path=''):
                for f in os.listdir(directory):
                    full_path = os.path.join(directory, f)
                    if os.path.isdir(full_path):
                        # 如果是顶层目录且不是分类目录，则作为分类处理
                        if not category and not rel_path:
                            categories.add(f)
                            collect_ogg_files(full_path, f, '')
                        else:
                            # 否则作为子目录处理
                            new_rel_path = f if not rel_path else os.path.join(rel_path, f)
                            collect_ogg_files(full_path, category, new_rel_path)
                    elif f.lower().endswith('.ogg'):
                        # 添加到文件列表，包含文件名、分类和相对路径
                        ogg_files.append((f, category, rel_path))  # (文件名, 分类, 相对路径)
            
            # 开始收集文件
            collect_ogg_files(cache_dist_dir)
            
            # 在sounds目录中创建分类子目录
            for category in categories:
                category_sounds_dir = os.path.join(sounds_dir, category)
                if not os.path.exists(category_sounds_dir):
                    os.makedirs(category_sounds_dir, mode=0o755)  # 设置读写权限
                    self.log_message.emit(f"在sounds目录中创建分类目录: {category}")
                
                # 创建子目录结构
                for _, cat, rel_path in ogg_files:
                    if cat == category and rel_path:
                        sub_dir = os.path.join(sounds_dir, category, rel_path)
                        if not os.path.exists(sub_dir):
                            os.makedirs(sub_dir, mode=0o755)  # 设置读写权限
                            self.log_message.emit(f"在sounds目录中创建子目录: {category}/{rel_path}")
            
            # 创建没有分类但有子目录的结构
            for _, cat, rel_path in ogg_files:
                if not cat and rel_path:
                    sub_dir = os.path.join(sounds_dir, rel_path)
                    if not os.path.exists(sub_dir):
                        os.makedirs(sub_dir, mode=0o755)  # 设置读写权限
                        self.log_message.emit(f"在sounds目录中创建子目录: {rel_path}")
            
            total_files = len(ogg_files)
            self.progress_updated.emit(0, total_files)
            
            for i, (file_name, category, rel_path) in enumerate(ogg_files):
                if self.is_canceled:
                    return
                
                # 获取soundkey作为文件名
                sound_key = os.path.splitext(file_name)[0]  # 默认使用文件名（不含扩展名）
                
                # 首先尝试从audio_soundkeys中查找
                found = False
                for orig_path, sk in self.audio_soundkeys.items():
                    if sk == sound_key:
                        self.log_message.emit(f"从audio_soundkeys找到匹配的soundKey: {sound_key}")
                        found = True
                        break
                
                # 如果没找到，尝试从音频配置文件中获取
                if not found:
                    try:
                        import json
                        sounds_json_path = self.project_path.cacheConfig()
                        if os.path.exists(sounds_json_path):
                            with open(sounds_json_path, 'r', encoding='utf-8') as f:
                                audio_info = json.load(f)
                            # 查找匹配的文件名
                            if file_name in audio_info and audio_info[file_name].get('sound_key'):
                                sound_key = audio_info[file_name]['sound_key']
                                self.log_message.emit(f"从音频配置文件获取到soundKey: {sound_key}")
                                found = True
                    except Exception as e:
                        self.log_message.emit(f"警告: 获取音频配置文件失败: {str(e)}")
                
                if not found:
                    self.log_message.emit(f"使用默认soundKey: {sound_key}")

                
                # 构建源路径和目标路径，保留子目录结构
                if category:
                    if rel_path:
                        # 有分类和子目录
                        src_path = os.path.join(cache_dist_dir, category, rel_path, file_name)
                        dst_path = os.path.join(sounds_dir, category, rel_path, file_name)
                        dst_dir = os.path.join(sounds_dir, category, rel_path)
                    else:
                        # 只有分类，没有子目录
                        src_path = os.path.join(cache_dist_dir, category, file_name)
                        dst_path = os.path.join(sounds_dir, category, file_name)
                        dst_dir = os.path.join(sounds_dir, category)
                else:
                    if rel_path:
                        # 没有分类，但有子目录
                        src_path = os.path.join(cache_dist_dir, rel_path, file_name)
                        dst_path = os.path.join(sounds_dir, rel_path, file_name)
                        dst_dir = os.path.join(sounds_dir, rel_path)
                    else:
                        # 没有分类，也没有子目录
                        src_path = os.path.join(cache_dist_dir, file_name)
                        dst_path = os.path.join(sounds_dir, file_name)
                        dst_dir = sounds_dir
                
                # 确保目标目录存在
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir, mode=0o755)  # 设置读写权限
                
                try:
                    # 复制文件到sounds目录
                    copyFile(src_path, dst_path)
                    
                    # 构建日志路径信息
                    src_rel_path = f"{category+'/' if category else ''}{rel_path+'/' if rel_path else ''}{file_name}"
                    dst_rel_path = f"sounds/{category+'/' if category else ''}{rel_path+'/' if rel_path else ''}{file_name}"
                    self.log_message.emit(f"已移动: {src_rel_path} -> {dst_rel_path}")
                except Exception as e:
                    error_path = f"{category+'/' if category else ''}{rel_path+'/' if rel_path else ''}{file_name}"
                    self.log_message.emit(f"移动失败: {error_path} - {str(e)}")
                
                self.progress_updated.emit(i + 1, total_files)
            
            self.step_completed.emit(2)
            
            # 步骤3: 打包项目
            self.step_started.emit(3)
            self.log_message.emit("开始打包项目...")
            
            try:
                # 获取Project对象
                project = getProject(self.project_path.project_name)
                self.log_message.emit("正在获取项目信息...")
                
                # 检查项目目录权限
                import os
                if not os.access(self.project_path.project_path, os.R_OK | os.W_OK | os.X_OK):
                    raise Exception(f"项目目录无权限: {self.project_path.project_path}")
                
                # 检查dist目录权限
                dist_path = self.project_path.dist()
                if not os.path.exists(dist_path):
                    self.log_message.emit(f"创建输出目录: {dist_path}")
                    from utils import createFolder
                    try:
                        createFolder(dist_path)
                    except Exception as e:
                        raise Exception(f"创建输出目录失败: {str(e)}")
                elif not os.access(dist_path, os.R_OK | os.W_OK | os.X_OK):
                    raise Exception(f"输出目录无权限: {dist_path}")
                
                # 打包项目
                self.log_message.emit(f"开始打包项目: {self.project_path.project_name}")
                self.log_message.emit(f"项目路径: {self.project_path.project_path}")
                
                result = project.build()
                
                if result == 1:
                    version = project.getVersion()
                    self.log_message.emit(f"打包成功!")
                    self.log_message.emit(f"资源包版本: {version}")
                    self.log_message.emit(f"资源包位置: {self.project_path.dist()}")
                    self.step_completed.emit(3)
                elif result == 0:
                    self.log_message.emit("打包已跳过")
                    self.log_message.emit("原因: 音效文件未发生变化，无需重新打包")
                    self.log_message.emit(f"可在 {self.project_path.dist()} 找到上一次打包的资源包")
                    self.step_completed.emit(3)
                else:
                    self.log_message.emit("打包失败")
                    self.log_message.emit("错误: 打包过程返回未知状态码")
                    self.export_completed.emit(False, "打包失败: 未知错误")
                    return
            except Exception as e:
                self.log_message.emit("打包过程出现异常")
                self.log_message.emit(f"异常类型: {type(e).__name__}")
                self.log_message.emit(f"异常信息: {str(e)}")
                self.log_message.emit("打包操作已终止")
                self.export_completed.emit(False, f"打包失败: {str(e)}")
                return
            
            # 步骤4: 生成命令
            self.step_started.emit(4)
            self.log_message.emit("生成游戏命令...")
            
            try:
                # 获取命令
                commands = project.getCommand()
                for cmd in commands:
                    self.log_message.emit(f"1.7.10及以下版本：/playsound {cmd} @a ~ ~ ~ 10000")
                    self.log_message.emit(f"1.8及以上版本：/playsound {cmd} record @a ~ ~ ~ 10000")

                self.log_message.emit(f"命令已生成，可在 {self.project_path.dist()} 找到")
                self.step_completed.emit(4)
            except Exception as e:
                self.log_message.emit(f"生成命令失败: {str(e)}")
                self.export_completed.emit(False, f"生成命令失败: {str(e)}")
                return
            
            # 导出完成
            self.log_message.emit("导出完成！")
            self.export_completed.emit(True, "")
            
        except Exception as e:
            self.log_message.emit(f"导出过程中发生错误: {str(e)}")
            self.export_completed.emit(False, f"导出过程中发生错误: {str(e)}")
        
        finally:
            self.is_running = False
    
    def cancel(self):
        """取消导出"""
        self.is_canceled = True

class ExportPage(QWidget):
    """导出页面"""
    # 返回编辑器页面信号
    backToEditorPage = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 应用我的世界风格
        apply_minecraft_style(self)
        
        # 创建主布局
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(20)
        
        # 创建顶部按钮区域
        self.topButtonLayout = QHBoxLayout()
        self.topButtonLayout.setContentsMargins(0, 0, 0, 0)
        self.topButtonLayout.setSpacing(20)
        
        # 创建返回按钮
        self.backButton = MinecraftPixelButton("返回编辑器", button_type="brown")
        self.backButton.setMinimumSize(120, 40)
        self.backButton.clicked.connect(self.onBack)
        
        # 添加按钮到顶部布局
        self.topButtonLayout.addWidget(self.backButton)
        self.topButtonLayout.addStretch(1)
        
        # 添加顶部按钮布局到主布局
        self.mainLayout.addLayout(self.topButtonLayout)
        
        # 创建步骤条区域
        self.stepsFrame = MinecraftFrame(frame_type="stone")
        self.stepsLayout = QVBoxLayout(self.stepsFrame)
        self.stepsLayout.setContentsMargins(15, 15, 15, 15)
        self.stepsLayout.setSpacing(10)
        
        # 创建步骤标题
        self.stepsTitle = MinecraftLabel("导出步骤")
        self.stepsTitle.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #FFFFFF;
                padding: 5px;
            }
        """)
        self.stepsLayout.addWidget(self.stepsTitle)
        
        # 创建步骤列表
        self.steps = [
            ExportStep(1, "转换格式: 将非ogg格式音频转换为ogg格式"),
            ExportStep(2, "移动文件: 将音频文件移动到sounds目录"),
            ExportStep(3, "打包项目: 将src目录打包为资源包"),
            ExportStep(4, "生成命令: 生成游戏中使用的命令")
        ]
        
        for step in self.steps:
            self.stepsLayout.addWidget(step)
        
        # 添加步骤条区域到主布局
        self.mainLayout.addWidget(self.stepsFrame)
        
        # 创建进度条区域
        self.progressFrame = MinecraftFrame(frame_type="stone")
        self.progressLayout = QVBoxLayout(self.progressFrame)
        self.progressLayout.setContentsMargins(15, 15, 15, 15)
        self.progressLayout.setSpacing(10)
        
        # 创建进度条标题
        self.progressTitle = MinecraftLabel("当前进度")
        self.progressTitle.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #FFFFFF;
                padding: 5px;
            }
        """)
        self.progressLayout.addWidget(self.progressTitle)
        
        # 创建进度条
        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.progressBar.setStyleSheet("""
            QProgressBar {
                background-color: #373737;
                border: 2px solid #1F1F1F;
                border-radius: 5px;
                color: #FFFFFF;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #5555FF;
                border-radius: 3px;
            }
        """)
        self.progressLayout.addWidget(self.progressBar)
        
        # 添加进度条区域到主布局
        self.mainLayout.addWidget(self.progressFrame)
        
        # 创建日志区域
        self.logFrame = MinecraftFrame(frame_type="stone")
        self.logLayout = QVBoxLayout(self.logFrame)
        self.logLayout.setContentsMargins(15, 15, 15, 15)
        self.logLayout.setSpacing(10)
        
        # 创建日志标题
        self.logTitle = MinecraftLabel("处理日志")
        self.logTitle.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #FFFFFF;
                padding: 5px;
            }
        """)
        self.logLayout.addWidget(self.logTitle)
        
        # 创建日志文本框
        self.logTextEdit = QTextEdit()
        self.logTextEdit.setReadOnly(True)
        self.logTextEdit.setStyleSheet("""
            QTextEdit {
                background-color: #373737;
                border: 2px solid #1F1F1F;
                color: #FFFFFF;
                font-family: 'Consolas', 'Courier New', monospace;
                padding: 5px;
            }
        """)
        self.logLayout.addWidget(self.logTextEdit)
        
        # 添加日志区域到主布局
        self.mainLayout.addWidget(self.logFrame)
        
        # 创建底部按钮区域
        self.bottomButtonLayout = QHBoxLayout()
        self.bottomButtonLayout.setContentsMargins(0, 0, 0, 0)
        self.bottomButtonLayout.setSpacing(20)
        
        # 创建打开文件夹按钮
        self.openFolderButton = MinecraftPixelButton("打开文件夹", button_type="blue")
        self.openFolderButton.setMinimumSize(120, 40)
        self.openFolderButton.clicked.connect(self.onOpenFolder)
        
        # 创建开始按钮
        self.startButton = MinecraftPixelButton("开始导出", button_type="green")
        self.startButton.setMinimumSize(120, 40)
        self.startButton.clicked.connect(self.onStart)
        
        # 创建取消按钮
        self.cancelButton = MinecraftPixelButton("取消", button_type="red")
        self.cancelButton.setMinimumSize(120, 40)
        self.cancelButton.clicked.connect(self.onCancel)
        self.cancelButton.setEnabled(False)
        
        # 添加按钮到底部布局
        self.bottomButtonLayout.addWidget(self.openFolderButton)
        self.bottomButtonLayout.addStretch(1)
        self.bottomButtonLayout.addWidget(self.startButton)
        self.bottomButtonLayout.addWidget(self.cancelButton)
        
        # 添加底部按钮布局到主布局
        self.mainLayout.addLayout(self.bottomButtonLayout)
        
        # 初始化导出工作线程
        self.worker = None
        self.project_path = None
        self.audio_files = []
    
    def onBack(self):
        """返回按钮点击事件"""
        # 如果正在导出，询问是否取消
        if self.worker and self.worker.is_running:
            result = MinecraftMessageBox.show_question(
                self,
                "取消导出",
                "导出正在进行中，确定要取消并返回吗？"
            )
            if result == MinecraftMessageBox.Yes:
                self.onCancel()
            else:
                return
        
        # 发送返回信号
        self.backToEditorPage.emit()
    
    def onStart(self):
        """开始按钮点击事件"""
        if not self.project_path or not self.audio_files:
            MinecraftMessageBox.show_warning(
                self,
                "无法导出",
                "项目路径或音频文件列表为空"
            )
            return
        
        # 清空日志
        self.logTextEdit.clear()
        
        # 重置步骤状态
        for step in self.steps:
            step.setActive(False)
            step.setCompleted(False)
        
        # 重置进度条
        self.progressBar.setValue(0)
        
        # 从编辑器页面获取音频文件的soundkey
        self.collectSoundKeys()
        
        # 创建并启动工作线程
        self.worker = ExportWorker(self.project_path, self.audio_files)
        self.worker.audio_soundkeys = self.audio_soundkeys
        self.worker.step_started.connect(self.onStepStarted)
        self.worker.step_completed.connect(self.onStepCompleted)
        self.worker.progress_updated.connect(self.onProgressUpdated)
        self.worker.log_message.connect(self.onLogMessage)
        self.worker.export_completed.connect(self.onExportCompleted)
        self.worker.start()
        
        # 更新按钮状态
        self.startButton.setEnabled(False)
        self.cancelButton.setEnabled(True)
        self.backButton.setEnabled(False)
    
    def onCancel(self):
        """取消按钮点击事件"""
        if self.worker and self.worker.is_running:
            self.worker.cancel()
            self.onLogMessage("正在取消导出...")
            
            # 等待线程结束
            self.worker.wait(1000)  # 等待最多1秒
            
            if self.worker.is_running:
                self.onLogMessage("导出取消中，请稍候...")
            else:
                self.onLogMessage("导出已取消")
                
                # 更新按钮状态
                self.startButton.setEnabled(True)
                self.cancelButton.setEnabled(False)
                self.backButton.setEnabled(True)
    
    @pyqtSlot(int)
    def onStepStarted(self, step_number):
        """步骤开始事件"""
        if 1 <= step_number <= len(self.steps):
            self.steps[step_number - 1].setActive(True)
    
    @pyqtSlot(int)
    def onStepCompleted(self, step_number):
        """步骤完成事件"""
        if 1 <= step_number <= len(self.steps):
            self.steps[step_number - 1].setActive(False)
            self.steps[step_number - 1].setCompleted(True)
    
    @pyqtSlot(int, int)
    def onProgressUpdated(self, current, maximum):
        """进度更新事件"""
        if maximum > 0:
            self.progressBar.setMaximum(maximum)
            self.progressBar.setValue(current)
        else:
            self.progressBar.setMaximum(0)  # 设置为不确定模式
    
    @pyqtSlot(str)
    def onLogMessage(self, message):
        """日志消息事件"""
        # 添加时间戳
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        log_message = f"[{timestamp}] {message}"
        
        # 添加到日志文本框
        self.logTextEdit.append(log_message)
        
        # 滚动到底部
        self.logTextEdit.verticalScrollBar().setValue(self.logTextEdit.verticalScrollBar().maximum())
    
    @pyqtSlot(bool, str)
    def onExportCompleted(self, success, error_message):
        """导出完成事件"""
        if success:
            MinecraftMessageBox.show_message(
                self,
                "导出成功",
                "项目导出成功！"
            )
        else:
            print(error_message)
            MinecraftMessageBox.show_warning(
                self,
                "导出失败",
                f"项目导出失败: {error_message}"
            )
        
        # 更新按钮状态
        self.startButton.setEnabled(True)
        self.cancelButton.setEnabled(False)
        self.backButton.setEnabled(True)
    
    def loadProject(self, project_path: ProjectPath, audio_files):
        """加载项目"""
        # self.project_path = ProjectConfig.load_config(project_path)
        self.project_path = project_path
        self.audio_files = audio_files
        
        # 获取音频文件对应的soundkey
        self.audio_soundkeys = {}
        
        # 更新窗口标题
        self.title_text = f"导出 - {self.project_path.project_name}"
        
        # 设置窗口标题
        window = self.window()
        if window:
            window.setWindowTitle(self.title_text)
        
        # 添加初始日志
        self.logTextEdit.clear()
        self.onLogMessage(f"已加载项目: {self.project_path.project_name}")
        self.onLogMessage(f"音频文件数量: {len(audio_files)}")
        self.onLogMessage("点击'开始导出'按钮开始导出过程")
        
    def onOpenFolder(self):
        """打开文件夹按钮点击事件"""
        if not self.project_path:
            MinecraftMessageBox.show_warning(
                self,
                "无法打开文件夹",
                "项目路径为空"
            )
            return
        
        # 获取dist目录路径
        dist_path = self.project_path.dist()
        
        # 检查目录是否存在
        if not os.path.exists(dist_path):
            MinecraftMessageBox.show_warning(
                self,
                "无法打开文件夹",
                f"目录不存在: {dist_path}"
            )
            return
        
        # 使用系统默认文件管理器打开文件夹
        try:
            # 在Windows上使用explorer打开文件夹
            subprocess.Popen(["explorer", dist_path])
            self.onLogMessage(f"已打开文件夹: {dist_path}")
        except Exception as e:
            MinecraftMessageBox.show_warning(
                self,
                "打开文件夹失败",
                f"无法打开文件夹: {str(e)}"
            )
            self.onLogMessage(f"打开文件夹失败: {str(e)}")
    
    def collectSoundKeys(self):
        """从编辑器页面获取音频文件的soundkey和分类信息"""
        # 获取编辑器页面
        parent = self.parent()
        editor_page = None
        
        # 查找编辑器页面
        while parent:
            if hasattr(parent, 'stackedWidget'):
                for i in range(parent.stackedWidget.count()):
                    widget = parent.stackedWidget.widget(i)
                    if hasattr(widget, 'audioList') and hasattr(widget, 'audioFiles'):
                        editor_page = widget
                        break
                break
            parent = parent.parent()
        
        if not editor_page:
            self.onLogMessage("警告: 无法获取编辑器页面，将使用默认soundkey")
            return
        
        # 清空当前映射
        self.audio_soundkeys = {}
        self.audio_categories = {}
        
        # 遍历编辑器页面中的音频列表项
        for i in range(editor_page.audioList.count()):
            item = editor_page.audioList.item(i)
            widget = editor_page.audioList.itemWidget(item)
            if hasattr(widget, 'file_path') and hasattr(widget, 'soundKey'):
                self.audio_soundkeys[widget.file_path] = widget.soundKey
                
                # 获取分类信息
                if hasattr(widget, 'categoryComboBox'):
                    category = widget.categoryComboBox.currentText()
                    if category == "无分类":
                        category = ""
                    self.audio_categories[widget.file_path] = category
                    self.onLogMessage(f"获取到音频文件 {os.path.basename(widget.file_path)} 的soundKey: {widget.soundKey}, 分类: {category if category else '无分类'}")
                else:
                    self.audio_categories[widget.file_path] = ""
                    self.onLogMessage(f"获取到音频文件 {os.path.basename(widget.file_path)} 的soundKey: {widget.soundKey}")
        
        self.onLogMessage(f"共获取到 {len(self.audio_soundkeys)} 个音频文件的soundKey和分类信息")