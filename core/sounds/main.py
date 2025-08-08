from core.minecraft import *
import json


class Sounds:
    """
    声音配置管理器
    用于管理项目的声音配置文件
    """

    def __init__(self, project_name: str, sound_main_key: str = "mcsd"):

        """
        初始化声音配置管理器
        
        参数:
            project_name (str): 项目名称
            sound_main_key (str): 声音主键
        """
        self.project_name = project_name
        self.sound_main_key = sound_main_key
        self.config_path = ProjectPath(self.project_name).soundsJson()
        self.config = {}

    def _load_config(self):
        """从文件加载配置，如果文件不存在则返回空字典"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_config(self):
        """将当前配置保存到文件"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4)
        return True

    def getConfig(self):
        """获取当前配置"""
        if path.exists(self.config_path):
            self.config = self._load_config()
        return self.config


    def get_sound_data(self, sound_name):
        """
        获取指定声音名称的配置数据
        
        参数:
            sound_name (str): 声音名称
        
        返回:
            dict: 声音配置数据（如果存在），否则返回None
        """
        return self.config.get(sound_name)

    def sound_name_format(self, sound_name: str):
        """
        格式化声音名称
        """
        return self.sound_main_key + "." + sound_name.replace("/", ".")
    
    def sound_path_format(self, sound_path: str):
        """
        格式化声音路径
        """
        return sound_path.replace("\\", "/")

    def create_soundsToJson(self):
        """
        自动创建声音配置
        扫描音效文件夹，将所有音效文件包括子文件夹里的音效文件的路径添加到配置文件中
        音效文件的路径格式为：音效文件夹路径/音效文件名
        注意：
            1. 音效文件夹路径为项目的sounds文件夹
            2. 音效文件名必须为.ogg格式
            3. 不可包含特殊字符
            4. 音效名称和子目录名称不可重复

        例如：
            音效文件夹路径：C:/Users/Administrator/Desktop/MinecraftSounds/sounds
            音效文件名：test.ogg
            音效文件路径：C:/Users/Administrator/Desktop/MinecraftSounds/sounds/test.ogg
            返回: test
            音效文件路径：C:/Users/Administrator/Desktop/MinecraftSounds/sounds/test/test.ogg
            返回: test/test

            以此类推，子目录下的音效文件路径为：子目录名/音效文件名
            返回: 子目录名/音效文件名

        返回值：
            {
                "mcsd.test": {
                    "category": "record",
                    "sounds": [{
                        "name": "test",
                        "stream": True
                    }]
                },
                "mcsd.test.test": {
                    "category": "record",
                    "sounds": [{
                        "name": "test/test",
                        "stream": True
                    }]
                }
            }
        """
        self.config = {}
        data = MinecraftSounds.findOggFiles(ProjectPath(self.project_name).sounds())
        for da in data:
            self.config[self.sound_name_format(da)] = self.create_sound_entry(da)
        self.save_config()
        return self.config

    def create_sound_entry(self, sound_path):
        """
        创建新的声音条目
        
        参数:
            sound_name (str): 声音名称
        
        返回:
            dict: 新的声音配置条目
        """

        return {
            "category": "record",
            "sounds": [{
                "name": sound_path,
                "stream": True
            }]
        }

    def append_sound_data(self, new_sound_name, sound_path = None):
        """
        将新的声音条目追加到现有数据中
        
        参数:
            existing_data (dict): 已存在的JSON数据（字典格式）
            new_sound_name (str): 要添加的新声音名称
        
        返回:
            dict: 更新后的完整数据
        """
        # 创建新条目并追加
        self.config[self.sound_name_format(new_sound_name)] = self.create_sound_entry(new_sound_name, sound_path)
        # 保存配置
        self.save_config()
        return self.config
    
    def remove_sound_data(self, sound_name):
        """
        从现有数据中移除指定的声音条目

        参数:
            existing_data (dict): 已存在的JSON数据（字典格式）
            sound_name (str): 要移除的声音名称
        
        返回:
            dict: 更新后的完整数据
        """
        if sound_name in self.config:
            del self.config[sound_name]
            # 保存配置
            self.save_config()
        return self.config

    def list_sounds(self):
        """列出所有声音名称"""
        return list(self.config.keys())