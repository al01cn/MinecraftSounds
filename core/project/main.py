from os import path
from core.sounds import *
from core.minecraft import *
from utils import *

class Project:
    def __init__(self, name, description = "", icon_path = "", pack_format = 1, sound_main_key = "mcsd"):
        self.name = name # 项目名称
        self.description = description # 项目描述
        self.icon_path = icon_path # 项目图标路径
        self.pack_format = pack_format # 项目资源包ID
        self.sound_main_key = sound_main_key # 音效主键
        self.path = path.join(project_path, self.name) # 项目路径
        self.pj_path = ProjectPath(self.name)
        self.version = Version("0.0.1") # 项目版本
        self.sounds = {} # 项目中的音效
        self.config = {
            'name': self.name,
            "description": self.description,
            "icon_path": self.icon_path,
            "pack_format": self.pack_format,
            "sound_main_key": self.sound_main_key,
            'path': self.path,
            'version': str(self.version),
            'sounds': self.sounds,
        } # 项目配置
        self.sound = Sounds(self.name, self.sound_main_key)

    def create(self):
        # 创建项目根目录
        if not projectExists(self.name):
            print("创建项目：" + self.path)
            createFolder(self.path)
            self.create_config()
            MinecraftSounds.create(project_name=self.name, description=self.description, pack_format=self.pack_format, icon_path=self.icon_path)
            self.sound._load_config()
            self.sounds = self.sound.getConfig()
        else:
            raise Error('项目已存在')
    
    def build(self):
        # 打包项目
        try:
            self.config_version()
            self.config_sounds()
            
            # 第一次构建（初始版本且没有音效）
            is_first_build = self.version == "0.0.1" and self.sounds == {}
            if is_first_build:
                self.autoCreateSound()
                self.update_config()
            
            # 检查音效是否有变化
            if not is_first_build and self.sounds == self.config_sounds():
                print("音效未更新，尝试使用autoCreateSound()更新一次")
                # 尝试更新音效
                self.autoCreateSound()
                # 再次检查音效是否有变化
                if self.sounds == self.config_sounds():
                    print("更新后音效仍未变化，跳过构建")
                    return 0

            toPack(self.pj_path.src(), self.pj_path.dist(), self.name + "_" + self.version.__str__())
            self.version = Version().increment_version(self.version)
            self.update_config()
            print(f"构建成功，新版本: {self.version}")
            return 1
        except Exception as e:
            print(f"构建失败: {str(e)}")
            return -1

    def icon(self, icon_path: str):
        MinecraftSounds.replaceIcon(project_name=self.name, icon_path=icon_path)

    def getDescription(self):
        return self.description
    
    def getPackFormat(self):
        return self.pack_format

    def getVersion(self):
        return self.version
    
    def getIconPath(self):
        return self.icon_path
    
    def getName(self):
        return self.name

    def getPath(self):
        return self.path

    def setDescription(self, description: str):
        self.description = description
        self.config["description"] = description

    def setPackFormat(self, pack_format: int):
        self.pack_format = pack_format
        self.config["pack_format"] = pack_format

    def setVersion(self, version: str):
        self.version = version
        self.config["version"] = version

    def getCommand(self):
        soundkey = self.sound.list_sounds()
        print(soundkey)
        return soundkey

    def autoCreateSound(self):
        # 创建项目中的音效目录
        data = self.sound.create_soundsToJson()
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
            "description": self.description,
            "icon_path": self.icon_path,
            "pack_format": self.pack_format,
            'path': self.path,
            'version': str(self.version),
            'sounds': self.sounds,
        })

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
            version = self.config_content()['version']
            self.version = version
            return version
        else:
            raise Error('项目配置文件不存在')

    def config_sounds(self):
        # 获取项目配置文件中的音效
        if path.exists(path.join(self.path, projectConifgName)):
            sounds = self.config_content()['sounds']
            self.sounds = sounds
            return sounds
        else:
            raise Error('项目配置文件不存在')





