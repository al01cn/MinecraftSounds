from os import path
from core.minecraft.main import MinecraftSounds
from utils import *

class Project:
    def __init__(self, name):
        self.name = name # 项目名称
        self.path = path.join(project_path, self.name) # 项目路径
        self.version = Version("0.0.0") # 项目版本
        self.sounds = {} # 项目中的音效
        self.config = {
            'name': self.name,
            'path': self.path,
            'version': str(self.version),
            'sounds': self.sounds
        } # 项目配置


    def create(self):
        # 创建项目根目录
        if not projectExists(self.name):
            print("创建项目：" + self.path)
            createFolder(self.path)
            self.create_config()
            MinecraftSounds.create(project_name=self.name, icon_path=path.join(root_path, "pack.png"))

        else:
            raise Error('项目已存在')

    def add_sound(self, sound):
        self.sounds.append(sound)

    def del_sound(self, sound):
        self.sounds.remove(sound)

    def create_config(self):
        # 创建项目配置文件
        if not path.exists(path.join(self.path, projectConifgName)):
            createJsonFile(path.join(self.path, projectConifgName), self.config)
        else:
            raise Error('项目配置文件已存在')

    def update_config(self):
        # 更新项目配置文件
        if path.exists(path.join(self.path, projectConifgName)):
            updateJsonFile(path.join(self.path, projectConifgName), self.config)
        else:
            raise Error('项目配置文件不存在')

    def config_content(self):
        # 获取项目配置文件内容
        if path.exists(path.join(self.path, projectConifgName)):
            return getJsonFileContent(path.join(self.path, projectConifgName))
        else:
            raise Error('项目配置文件不存在')

    def config_version(self):
        # 获取项目配置文件版本
        if path.exists(path.join(self.path, projectConifgName)):
            self.version = Version(self.config_content['version'])
            return self.config_content['version']
        else:
            raise Error('项目配置文件不存在')

    def config_sounds(self):
        # 获取项目配置文件中的音效
        if path.exists(path.join(self.path, projectConifgName)):
            self.sounds = self.config_content['sounds']
            return self.config_content['sounds']
        else:
            raise Error('项目配置文件不存在')





