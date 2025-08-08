from os import path
from core.sounds import *
from core.minecraft import *
from utils import *

class Project:
    def __init__(self, name):
        self.name = name # 项目名称
        self.path = path.join(project_path, self.name) # 项目路径
        self.pj_path = ProjectPath(self.name)
        self.version = Version("0.0.0") # 项目版本
        self.sounds = {} # 项目中的音效
        self.config = {
            'name': self.name,
            'path': self.path,
            'version': str(self.version),
        } # 项目配置
        self.sound = Sounds(self.name)



    def create(self):
        # 创建项目根目录
        if not projectExists(self.name):
            print("创建项目：" + self.path)
            createFolder(self.path)
            self.create_config()
            MinecraftSounds.create(project_name=self.name, icon_path=path.join(root_path, "pack.png"))
            self.sound._load_config()
            self.sounds = self.sound.getConfig()
        else:
            raise Error('项目已存在')
    
    def build(self):
        # 打包项目
        try:
            self.getCommand()
            toPack(self.pj_path.src(), self.pj_path.dist(), self.name + "_" + self.version.__str__())
            self.version = Version().increment_version(self.version)
            self.update_config()

            return True
        except:
            raise False

    def getCommand(self):
        soundkey = self.sound.list_sounds()
        print(soundkey)
        return soundkey

    def autoCreateSound(self):
        # 创建项目中的音效目录
        data = self.sound.create_soundsToJson()
        print(data)
        self.sounds = data
        return data

    def addSound(self, sound_path: str, sound_name: str = None):
        # 添加音效到项目
        MinecraftSounds.addSound(project_name=self.name, sound_path=sound_path, sound_name=sound_name)
        self.sound.append_sound_data(sound_name)

    def delSound(self, sound_name: str):
        # 删除项目中的音效
        MinecraftSounds.delSound(project_name=self.name, sound_name=sound_name)
        self.sound.remove_sound_data(sound_name)


    def create_config(self):
        # 创建项目配置文件
        if not path.exists(path.join(self.path, projectConifgName)):
            createJsonFile(path.join(self.path, projectConifgName), self.config)
        else:
            raise Error('项目配置文件已存在')

    def update_config(self):
        # 更新项目配置文件
        if path.exists(path.join(self.path, projectConifgName)):
            updateJsonFile(path.join(self.path, projectConifgName), {
            'name': self.name,
            'path': self.path,
            'version': str(self.version),
        })
            print("更新项目配置文件：" + self.path, "版本：" + str(self.version))

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





