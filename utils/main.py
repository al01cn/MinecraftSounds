import shutil
import os
from os import path
from uu import Error
import json


root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # 项目根文件夹路径
app_path = os.path.join(root_path, 'app') # 应用文件夹路径
cache_path = os.path.join(app_path, 'cache') # 缓存文件夹路径
project_path = os.path.join(app_path, 'projects') # 项目文件夹路径
config_path = os.path.join(app_path, 'config.json') # 配置文件路径

exeSuffixName = ".mcsd" # 项目文件后缀名
soundSuffixName = ".ogg" # 音效文件后缀名

projectConifgName = "sounds" + exeSuffixName # 项目配置文件名


def createFolder(src):
    # 创建文件夹
    if not path.exists(src):
        os.makedirs(src)
    else:
        raise Error('文件夹已存在')

def createFile(src):
    # 创建文件
    if not path.exists(src):
        with open(src, 'w', encoding='utf-8') as f:

            f.write('')
    else:
        raise Error('文件已存在')

def createJsonFile(src, content={}):
    # 创建json文件
    if not path.exists(src):
        with open(src, 'w', encoding='utf-8') as f:
            f.write(json.dumps(content, ensure_ascii=False, indent=4))
    else:
        raise Error('文件已存在')

def updateJsonFile(src, content={}):
    # 更新json文件
    if path.exists(src):
        with open(src, 'w', encoding='utf-8') as f:
            f.write(json.dumps(content, ensure_ascii=False, indent=4))
    else:
        raise Error('文件不存在')

def getJsonFileContent(src):
    # 获取json文件内容
    if path.exists(src):
        with open(src, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        raise Error('文件不存在')

def delFolder(src):
    # 删除文件夹
    if path.exists(src):
        shutil.rmtree(src)
    else:
        raise Error('文件夹不存在')

def delFile(src):
    # 删除文件
    if path.exists(src):
        os.remove(src)
    else:
        raise Error('文件不存在')

def delJsonFile(src):
    # 删除json文件
    if path.exists(src):
        os.remove(src)
    else:
        raise Error('文件不存在')


def copyFile(src, dst):
    # 复制文件到指定文件夹
    if not path.exists(dst):
        os.makedirs(dst)
    shutil.copy(src, dst)


def deleteFolder(src):
    # 删除文件夹
    if path.exists(src):
        shutil.rmtree(src)
    else:
        raise Error('文件夹不存在')


def deleteFile(src):
    # 删除文件
    if path.exists(src):
        os.remove(src)
    else:
        raise Error('文件不存在')

def moveFile(src, dst):
    # 移动文件到指定文件夹
    if path.exists(src):
        shutil.move(src, dst)
    else:
        raise Error('文件不存在')

def toPack(src, dst, name='pack'):

    # 压缩文件夹，进行打包
    if path.exists(src):
        # 打包并重命名
        shutil.make_archive(os.path.join(dst, name), 'zip', src)
    else:
        raise Error('文件夹不存在')

def unPack(src, dst):
    # 解压文件到指定文件夹
    if path.exists(src):
        shutil.unpack_archive(src, dst)
    else:
        raise Error('文件不存在')

def getFileList(src):
    # 获取文件夹下的所有文件
    if path.exists(src):
        return [f for f in os.listdir(src) if path.isfile(path.join(src, f))]
    else:
        return []

def getFolderList(src):
    # 获取文件夹下的所有文件夹
    if path.exists(src):
        return [f for f in os.listdir(src) if path.isdir(path.join(src, f))]
    else:
        return []

def projectExists(name):
    # 检查项目是否存在
    if path.exists(path.join(project_path, name)) and path.exists(path.join(project_path, name, "sounds" + exeSuffixName)):
        return True
    else:
        return False
    
def getProject(name):
    # 获取项目
    if projectExists(name):
        return Project(name, path.join(project_path, name))
    else:
        raise Error('项目不存在')

