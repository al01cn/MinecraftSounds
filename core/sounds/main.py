from minecraft import ProjectPath
import json


class Sounds:
    """
    声音配置管理器
    用于管理项目的声音配置文件
    """

    def __init__(self, project_name: str):
        """
        初始化声音配置管理器
        
        参数:
            project_name (str): 项目名称
        """
        self.project_name = project_name
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


    def create_sound_entry(self, sound_name):
        return {
            "category": "record",
            "sounds": [{
                "name": sound_name,
                "stream": True
            }]
        }

    def append_sound_data(self, new_sound_name):
        """
        将新的声音条目追加到现有数据中
        
        参数:
            existing_data (dict): 已存在的JSON数据（字典格式）
            new_sound_name (str): 要添加的新声音名称
        
        返回:
            dict: 更新后的完整数据
        """
        # 创建新条目并追加
        self.config[new_sound_name] = self.create_sound_entry(new_sound_name)
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
        return self.config

    def list_sounds(self):
        """列出所有声音名称"""
        return list(self.config.keys())

    def rename_sound(self, old_name, new_name, auto_save=False):
        """
        重命名声音条目
        
        参数:
            old_name (str): 原声音名称
            new_name (str): 新声音名称
            auto_save (bool): 是否自动保存到文件
            
        返回:
            bool: 操作是否成功
        """
        if old_name not in self.config or new_name in self.config:
            return False  # 原声音不存在或新名称已存在
        
        # 复制并更新配置
        self.config[new_name] = self.config[old_name]
        del self.config[old_name]
        
        # 更新内部声音名称引用
        self.config[new_name]["sounds"][0]["name"] = new_name
        
        if auto_save:
            self.save_config()
        return True