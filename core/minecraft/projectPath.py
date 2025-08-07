from os import path
from utils import *

# 创建音频包项目，项目结构为：
# 项目名
# ├── src (源文件目录, 必须)
# │   ├── pack.mcmeta (音频包元数据, 必须)
# │   ├── pack.png (图标, 16x16-256x256, 可选)
# │   ├── assets (资源根目录, 必须)
# │   │   ├── minecraft (命名空间, 必须)
# │   │   │   ├── sounds.json (音效映射表, 必须)
# │   │   │   ├── sounds (音效目录, 必须)
# │   │   │   │   ├── sound1.ogg (音效文件, 必须)
# │   │   │   │   ├── sound2.ogg (音效文件, 必须)
# │   │   │   │   ├── 自定义空间 (音效目录, 可选)
# │   │   │   │   │   ├── sound3.ogg (音效文件, 根据自定义命名空间来决定是否必须)
# ├── dist (输出目录, 必须)
# │   ├── 项目名.zip
# │   │   ├── pack.mcmeta
# │   │   ├── pack.png
# │   │   ├── assets
# │   │   │   ├── minecraft
# │   │   │   │   ├── sounds.json
# │   │   │   │   ├── sounds
# │   │   │   │   │   ├── sound1.ogg
# │   │   │   │   │   ├── sound2.ogg
# │   │   │   │   │   ├── 自定义命名空间 (音效目录, 可选)
# │   │   │   │   │   │   ├── sound3.ogg (音效文件, 根据自定义命名空间来决定是否必须)

class ProjectPath:
    def __init__(self, project_name):
        self.project_name = project_name # 项目名称
        self.project_path = path.join(project_path, self.project_name) # 项目路径

    # 项目根目录
    def src(self):
        return path.join(self.project_path, "src")
    
    # 项目输出目录
    def dist(self):
        return path.join(self.project_path, "dist")
    
    # 项目输出的音频包
    def distPack(self):
        return path.join(self.dist(), self.project_name + ".zip")

    # 资源包图标
    def packIcon(self):
        return path.join(self.src(), "pack.png")
    
    # 资源包配置文件
    def packMcmeta(self):
        return path.join(self.src(), "pack.mcmeta")
    
    # 资源包根目录
    def assets(self):
        return path.join(self.src(), "assets")

    # 资源包 minecraft 目录
    def minecraft(self):
        return path.join(self.assets(), "minecraft")
    
    # 资源包 minecraft sounds 目录
    def sounds(self):
        return path.join(self.minecraft(), "sounds")
    
    # 资源包 minecraft sounds 目录下的自定义音效目录
    def soundf(self, name):
        return path.join(self.sounds(), name)
    
    # 资源包 minecraft sounds 目录下的自定义音效目录下的音效文件
    def sound(self, root, name):
        return path.join(self.soundf(root), name)

    def soundList(self, root):
        # 获取自定义目录下的所有音效文件
        return getFileList(self.soundf(root))

    # 资源包 minecraft sounds 目录下的音效文件的配置文件
    def soundsJson(self):
        return path.join(self.sounds(), "sounds.json")



















