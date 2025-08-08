import shutil
import os
from os import path
from uu import Error
import json
from PyQt5.QtGui import QIcon

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # 项目根文件夹路径
app_path = os.path.join(root_path, 'app') # 应用文件夹路径
ffmpeg_path = os.path.join(app_path, 'ffmpeg', 'ffmpeg.exe') # ffmpeg.exe文件路径
assets_path = os.path.join(root_path, 'assets') # 资源文件夹路径
icons_path = os.path.join(assets_path, 'icons') # 图标文件夹路径
project_path = os.path.join(app_path, 'projects') # 项目文件夹路径
config_path = os.path.join(app_path, 'config.json') # 配置文件路径

mcver_path = os.path.join(app_path, 'mc.ver') #  minecraft版本文件路径
logo_path = os.path.join(assets_path, 'logo.png') # 应用图标文件路径


exeSuffixName = ".mcsd" # 项目文件后缀名
soundSuffixName = ".ogg" # 音效文件后缀名

projectConifgName = "sounds" + exeSuffixName # 项目配置文件名


def GetLogoIcon(icon: bool = True):
    return QIcon(logo_path) if icon is True else logo_path

def GetIconSvg(iconName: str, icon: bool = True):
    iconf = os.path.join(icons_path, f'{iconName}.svg')
    return QIcon(iconf) if icon is True else iconf


def GetIcon(iconName: str, icon: bool = True):
    iconf = os.path.join(icons_path, f'{iconName}.png')
    return QIcon(iconf) if icon is True else iconf

def getMcVersion():
    # 获取minecraft版本
    if path.exists(mcver_path):
        with open(mcver_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        raise Error('文件不存在')

def getPack_formatToVersion(pack_format: int):
    # 获取pack_format对应的版本
    versions = getMcVersion()
    for version in versions:
        if version['pack_format'] == pack_format:
            return version['version']
    raise Error('pack_format不存在')

def getVersionToPack_format(version: str):
    # 获取版本对应的pack_format
    versions = getMcVersion()
    for ver in versions:
        if ver['version'] == version:
            return ver['pack_format']
    raise Error('版本不存在')

def check_ffmpeg():
    """检查系统中是否存在FFmpeg
    
    Returns:
        tuple: (是否存在FFmpeg, FFmpeg路径或None)
    """
    import shutil
    
    # 检查系统环境中是否有ffmpeg
    system_ffmpeg = shutil.which('ffmpeg')
    if system_ffmpeg is not None:
        return True, system_ffmpeg
    
    # 如果系统环境中没有ffmpeg，检查指定文件夹
    if os.path.exists(ffmpeg_path):
        return True, ffmpeg_path
    
    return False, None

def download_ffmpeg(target_dir=None):
    """下载FFmpeg到指定目录
    
    Args:
        target_dir (str, optional): 下载目标目录。默认为app/ffmpeg目录。
    
    Returns:
        bool: 下载是否成功
    """
    import urllib.request
    import zipfile
    import tempfile
    
    if target_dir is None:
        target_dir = os.path.dirname(ffmpeg_path)
    
    # 确保目标目录存在
    os.makedirs(target_dir, exist_ok=True)
    
    # FFmpeg下载链接 (Windows版本)
    download_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    
    try:
        # 创建临时文件下载ZIP
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_file:
            temp_path = temp_file.name
        
        print(f"正在下载FFmpeg到临时文件: {temp_path}")
        urllib.request.urlretrieve(download_url, temp_path)
        
        # 解压缩文件
        print("正在解压FFmpeg...")
        with zipfile.ZipFile(temp_path, 'r') as zip_ref:
            # 提取需要的文件 (ffmpeg.exe, ffplay.exe, ffprobe.exe)
            for file in zip_ref.namelist():
                if file.endswith(('ffmpeg.exe', 'ffplay.exe', 'ffprobe.exe')):
                    # 提取文件名
                    filename = os.path.basename(file)
                    # 从zip中读取文件内容
                    content = zip_ref.read(file)
                    # 写入到目标目录
                    target_file = os.path.join(target_dir, filename)
                    with open(target_file, 'wb') as f:
                        f.write(content)
                    print(f"已提取: {filename}")
        
        # 删除临时文件
        os.unlink(temp_path)
        
        # 验证文件是否成功提取
        if os.path.exists(os.path.join(target_dir, 'ffmpeg.exe')):
            print("FFmpeg下载并解压成功!")
            return True
        else:
            print("FFmpeg提取失败!")
            return False
            
    except Exception as e:
        print(f"下载FFmpeg时出错: {str(e)}")
        # 清理临时文件
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        return False


def toOgg(file_path: str, output_path: str, quality="192k", parameters=None, overwrite=False, sample_rate=None):
    """将任意音频文件转换为ogg格式并保存到指定路径
    
    Args:
        file_path (str): 原始音频文件路径
        output_path (str): 输出文件路径，如果是目录则保持原文件名并更改扩展名为.ogg
        quality (str, optional): 输出音频的质量，例如"192k"。默认为"192k"。
        parameters (list, optional): 传递给ffmpeg的额外参数列表，例如['-q:a', '0']。默认为None。
        overwrite (bool, optional): 如果输出文件已存在，是否覆盖。默认为False。
        normalize (bool, optional): 是否对音频进行音量标准化处理。默认为False。
        sample_rate (int, optional): 设置输出音频的采样率，例如44100。默认为None（保持原采样率）。
        
    Returns:
        str: 转换后的ogg文件路径
        
    Raises:
        Error: 文件格式不支持或转换失败
    """
    try:
        from pydub import AudioSegment
        import shutil
    except ImportError:
        raise Error('请安装pydub库: pip install pydub')
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise Error(f'文件不存在: {file_path}')
    
    # 处理输出路径
    if os.path.isdir(output_path):
        # 如果输出路径是目录，则在该目录下创建同名的.ogg文件
        file_name = os.path.basename(file_path)
        file_name_without_ext = os.path.splitext(file_name)[0]
        output_path = os.path.join(output_path, f"{file_name_without_ext}.ogg")
    else:
        # 确保输出文件的扩展名是.ogg
        if not output_path.lower().endswith('.ogg'):
            output_path = f"{os.path.splitext(output_path)[0]}.ogg"
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
    
    # 检查输出文件是否已存在
    if os.path.exists(output_path) and not overwrite:
        # 如果文件已存在且不允许覆盖，则返回现有文件路径
        return output_path
        
    # 如果已经是ogg格式且输出路径与输入路径相同，直接返回
    if file_path.lower().endswith('.ogg') and os.path.abspath(file_path) == os.path.abspath(output_path):
        return file_path
        
    # 如果已经是ogg格式但输出路径不同，则复制文件
    if file_path.lower().endswith('.ogg'):
        shutil.copy2(file_path, output_path)
        return output_path
    
    # 获取文件扩展名
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    # 支持的音频格式
    supported_formats = ['.mp3', '.wav', '.flac', '.aac', '.m4a', '.wma', '.opus', '.webm', '.mp4', '.avi', '.mov']
    
    if ext not in supported_formats and not ext == '.ogg':
        raise Error(f'不支持的文件格式: {ext}，支持的格式: {", ".join(supported_formats)}')
    
    # 检查系统环境中是否有ffmpeg
    ffmpeg_in_path = shutil.which('ffmpeg') is not None
    
    # 如果系统环境中没有ffmpeg，检查指定文件夹
    ffmpeg_exists = os.path.exists(ffmpeg_path)
    
    if not ffmpeg_in_path and not ffmpeg_exists:
        raise Error('转换失败: 系统环境和指定文件夹中都没有找到FFmpeg')
    
    # 记录使用的ffmpeg路径，用于错误处理
    ffmpeg_path_used = None
    
    # 如果系统环境中没有ffmpeg但指定文件夹中有，设置环境变量
    if not ffmpeg_in_path and ffmpeg_exists:
        # 获取ffmpeg文件夹路径
        ffmpeg_dir = os.path.dirname(ffmpeg_path)
        # 将ffmpeg路径添加到环境变量
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ["PATH"]
        ffmpeg_path_used = ffmpeg_path
        print(f"使用指定文件夹中的FFmpeg: {ffmpeg_dir}")
    else:
        ffmpeg_path_used = shutil.which('ffmpeg')
    
    try:
        # 根据文件扩展名加载音频
        format_mapping = {
            '.mp3': 'mp3',
            '.wav': 'wav',
            '.flac': 'flac',
            '.m4a': 'm4a',
            '.aac': 'aac',
            '.wma': 'wma',
            '.opus': 'opus',
            '.webm': 'webm',
            '.mp4': 'mp4',
            '.avi': 'avi',
            '.mov': 'mov'
        }
        
        # 根据文件扩展名加载音频
        if ext == '.mp3':
            audio = AudioSegment.from_mp3(file_path)
        elif ext == '.wav':
            audio = AudioSegment.from_wav(file_path)
        elif ext in format_mapping:
            audio = AudioSegment.from_file(file_path, format=format_mapping[ext])
        else:
            # 尝试自动检测格式
            audio = AudioSegment.from_file(file_path)
        
        # 如果需要设置采样率
        if sample_rate:
            audio = audio.set_frame_rate(sample_rate)
        
        # 导出为ogg格式，使用指定的质量参数
        export_args = {
            "format": "ogg",
            "bitrate": quality,
            "codec": "libvorbis",  # 确保使用vorbis编码器
        }
        
        # 如果提供了额外参数，添加到导出参数中
        if parameters:
            export_args["parameters"] = parameters
        
        # 导出文件
        audio.export(output_path, **export_args)
        
        # 验证文件是否成功创建
        if not os.path.exists(output_path):
            raise Error(f'转换失败: 输出文件未创建 {output_path}')
            
        # 验证文件大小是否大于0
        if os.path.getsize(output_path) == 0:
            os.remove(output_path)  # 删除空文件
            raise Error(f'转换失败: 输出文件大小为0 {output_path}')
        
        return output_path
    except Exception as e:
        # 捕获转换过程中的错误
        error_msg = str(e)
        
        # 清理可能创建的不完整文件
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass
        
        # 更详细的错误分类和处理        
        if "ffmpeg" in error_msg.lower():
            if ffmpeg_path_used == ffmpeg_path:
                raise Error(f'转换失败: 使用指定文件夹中的FFmpeg失败。错误信息: {error_msg}')
            else:
                raise Error(f'转换失败: 请确保已安装FFmpeg并添加到系统路径。错误信息: {error_msg}')
        elif "codec" in error_msg.lower() or "format" in error_msg.lower():
            raise Error(f'转换失败: 不支持的音频格式或编解码器。错误信息: {error_msg}')
        elif "sample rate" in error_msg.lower() or "sampling rate" in error_msg.lower():
            raise Error(f'转换失败: 采样率设置错误。错误信息: {error_msg}')
        elif "permission" in error_msg.lower() or "access" in error_msg.lower():
            raise Error(f'转换失败: 文件访问权限错误。错误信息: {error_msg}')
        elif "memory" in error_msg.lower():
            raise Error(f'转换失败: 内存不足。错误信息: {error_msg}')
        else:
            raise Error(f'转换失败: {error_msg}')



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

