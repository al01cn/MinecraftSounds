from os import path
from utils import *
from .projectPath import *


class MinecraftSounds:
    # 我的世界音频包，文件结构

    @staticmethod
    def create(project_name: str, pack_format: int = 1, description: str = "", icon_path: str = ""):

        pack = ProjectPath(project_name)

        if not path.exists(pack.src()): # 源文件目录
            createFolder(pack.src())

        if not path.exists(pack.dist()): # 输出目录
            createFolder(pack.dist())

        if not path.exists(pack.cache()): # 缓存目录
            createFolder(pack.cache())


        if not path.exists(pack.assets()): # 资源根目录
            createFolder(pack.assets())
        if not path.exists(pack.minecraft()): # 命名空间
            createFolder(pack.minecraft())
        if not path.exists(pack.sounds()): # 音效目录
            createFolder(pack.sounds())
        if not path.exists(pack.packMcmeta()): # 音频包元数据
            createJsonFile(pack.packMcmeta(), {
                "pack": {
                    "pack_format": pack_format, # 游戏版本号, 必须
                    "description": description, # 音频包描述, 可选
                    "supported_formats": {
                        "min_inclusive": 1,
                        "max_inclusive": 65.1
                    }
                }
            })
        if icon_path != "" and icon_path != None:
            # 复制图标到指定文件夹
            if path.exists(icon_path):
                copyFile(icon_path, pack.src())

        if not path.exists(pack.soundsJson()): # 音效映射表
            createJsonFile(pack.soundsJson())

    @staticmethod
    def replaceIcon(project_name: str, icon_path: str):
        pack = ProjectPath(project_name)

        if path.exists(pack.packIcon()):
            delFile(pack.packIcon())
        if icon_path != "":
            # 复制图标到指定文件夹
            copyFile(icon_path, pack.packIcon())


    @staticmethod
    def createSounds(project_name: str, sound_name: str):
        pack = ProjectPath(project_name)
        # 创建音频目录
        if not path.exists(pack.soundf(sound_name)):
            createFolder(pack.soundf(sound_name))

    @staticmethod
    def addSound(project_name: str, sound_path: str, sound_name: str = None):
        pack = ProjectPath(project_name)

        if sound_name == None:
            # 添加音效到根目录
            if not path.exists(pack.sounds()):
                # 复制文件到指定文件夹
                copyFile(sound_path, pack.sounds())

        else:
            # 添加音效到自定义目录
            if not path.exists(pack.sounds(sound_name)):
                copyFile(sound_path, pack.sound(sound_name))
    
    @staticmethod
    def delSound(project_name: str, sound_path: str, sound_name: str = None):
        pack = ProjectPath(project_name)

        if sound_name == None:
            # 删除根目录的音效
            if path.exists(pack.sound(sound_path)):
                delFile(pack.sound(sound_path))
        else:
            # 删除自定义目录的音效
            if path.exists(pack.sound(sound_name, sound_path)):
                delFile(pack.sound(sound_name, sound_path))

    @staticmethod
    def findOggFiles(base_path):
        ogg_names = []
        base_path = os.path.normpath(base_path)  # 规范化路径（处理斜杠/反斜杠）
        
        for root, _, files in os.walk(base_path):
            for file in files:
                if file.lower().endswith('.ogg'):
                    # 获取文件的完整路径
                    full_path = os.path.join(root, file)
                    
                    # 计算相对于base_path的相对路径
                    rel_path = os.path.relpath(full_path, base_path)
                    
                    # 去除.ogg后缀并替换路径分隔符
                    name_no_ext = os.path.splitext(rel_path)[0]
                    normalized_name = name_no_ext.replace('\\', '/')
                    
                    ogg_names.append(normalized_name)
        
        return ogg_names