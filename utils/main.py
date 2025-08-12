import shutil
import os
from os import path
from uu import Error
import json
import urllib.request
import socket
import sys
from PyQt5.QtGui import QIcon
from pypinyin import pinyin, STYLE_NORMAL
import time
import random
# 移除顶层导入，避免循环引用
# from core.project import Project

# 项目根文件夹路径
try:
    # 正常运行时使用相对路径
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    # 打包后使用当前工作目录
    import sys
    if getattr(sys, 'frozen', False):
        root_path = os.path.dirname(sys.executable)
    else:
        root_path = os.getcwd()
app_path = os.path.join(root_path, 'app') # 应用文件夹路径
assets_path = os.path.join(app_path, 'assets') # 资源文件夹路径
icons_path = os.path.join(assets_path, 'icons') # 图标文件夹路径
font_path = os.path.join(assets_path, 'fonts') # 字体文件夹路径
project_path = os.path.join(app_path, 'projects') # 项目文件夹路径
config_path = os.path.join(app_path, 'config.json') # 配置文件路径

ffmpeg_download_urls = [
    "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip",
]

# 从配置文件中读取ffmpeg路径，如果不存在则使用默认路径
def get_ffmpeg_path():
    default_ffmpeg_path = os.path.join(app_path, 'ffmpeg', 'ffmpeg.exe')
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                if 'ffmpeg_path' in config:
                    custom_path = os.path.join(config['ffmpeg_path'], 'ffmpeg.exe')
                    if os.path.exists(custom_path):
                        return custom_path
    except Exception as e:
        print(f"读取ffmpeg配置失败: {e}")
    return default_ffmpeg_path

ffmpeg_path = get_ffmpeg_path() # ffmpeg.exe文件路径
history_path = os.path.join(app_path, 'history.json') # 历史项目记录文件路径

mcver_path = os.path.join(app_path, 'mc.ver') #  minecraft版本文件路径
logo_path = os.path.join(assets_path, 'logo.png') # 应用图标文件路径
defaultIcon_path = os.path.join(assets_path, 'default_pack.png') # 默认图标文件路径


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

def getDefaultIcon():
    return defaultIcon_path

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

def getGithubProxy():
    """获取GitHub代理列表
    
    Returns:
        list: GitHub代理列表，每个元素为一个字典，包含url、server、ip、location、latency、speed等信息
    """
    try:
        import requests
        import json
        
        # 设置超时时间（秒）
        timeout_seconds = 5
        
        # 请求GitHub代理API
        response = requests.get("https://api.akams.cn/github", timeout=timeout_seconds)
        
        # 检查响应状态码
        if response.status_code == 200:
            data = response.json()
            
            # 检查返回的数据格式
            if data.get("code") == 200 and "data" in data:
                return data["data"]
        
        return []
    except Exception as e:
        print(f"获取GitHub代理失败: {str(e)}")
        return []


def check_ffmpeg():
    """检查系统中是否存在FFmpeg
    
    Returns:
        tuple: (是否存在FFmpeg, FFmpeg路径或None)
    """
    import shutil
    
    # 首先检查配置文件中指定的路径
    if os.path.exists(ffmpeg_path):
        return True, ffmpeg_path
    
    # 检查系统环境中是否有ffmpeg
    system_ffmpeg = shutil.which('ffmpeg')
    if system_ffmpeg is not None:
        return True, system_ffmpeg
    
    # 检查默认路径
    default_ffmpeg_path = os.path.join(app_path, 'ffmpeg', 'ffmpeg.exe')
    if os.path.exists(default_ffmpeg_path):
        return True, default_ffmpeg_path
    
    return False, None

def get_ffmpeg_download_urls(progress_callback=None):
    """获取并测试FFmpeg下载链接
    
    Args:
        progress_callback (function, optional): 进度回调函数，接收下载进度百分比和状态消息。
    
    Returns:
        tuple: (有效链接列表, 链接速度字典, 最快的链接)
    """
    import urllib.request
    import time
    from urllib.parse import urlparse
    
    # 初始化结果变量
    valid_urls = []
    url_speeds = {}
    fastest_url = None
    
    # 获取GitHub代理
    if progress_callback:
        progress_callback(5, "正在获取GitHub代理...")
    
    github_proxies = getGithubProxy()
    
    # 准备测试的链接列表
    test_urls = list(ffmpeg_download_urls)  # 原始链接
    
    # 添加代理链接
    for proxy in github_proxies:
        proxy_url = proxy.get("url", "")
        if proxy_url and proxy_url.strip():
            # 为每个原始链接添加代理
            for original_url in ffmpeg_download_urls:
                # 拼接代理链接
                if proxy_url.endswith("/"):
                    proxy_url = proxy_url[:-1]  # 移除末尾的斜杠
                
                # 确保原始URL是完整的URL
                if original_url.startswith("http"):
                    # 构建代理URL
                    proxy_test_url = f"{proxy_url}/{original_url}"
                    test_urls.append(proxy_test_url)
    
    # 显示测试链接窗口（如果有回调函数）
    if progress_callback:
        domains = [urlparse(url).netloc for url in test_urls]
        progress_callback(10, f"准备测试 {len(test_urls)} 个下载链接...")
        
        # 先测试所有域名
        unique_domains = set(domains)
        for domain in unique_domains:
            progress_callback(10, f"开始测试域名: {domain}")
        
        # 然后测试所有链接
        for url in test_urls:
            progress_callback(10, f"开始测试链接: {url}")
    
    # 测试每个链接
    for url in test_urls:
        try:
            domain = urlparse(url).netloc
            if progress_callback:
                progress_callback(15, f"正在测试链接: {domain}")
            
            # 通知连接有效，开始测速
            if progress_callback:
                progress_callback(15, f"链接 {url} 连接有效，开始测速")
                
            # 测量下载速度
            start_time = time.time()
            
            # 设置超时时间（秒）
            timeout_seconds = 5
            
            # 只下载前8KB来测试速度
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0',
                    'Range': 'bytes=0-8192'
                }
            )
            
            # 设置socket超时
            socket.setdefaulttimeout(timeout_seconds)
            
            with urllib.request.urlopen(req, timeout=timeout_seconds) as response:
                chunk = response.read(8192)
                if len(chunk) > 0:
                    # 计算下载速度（KB/s）
                    download_time = time.time() - start_time
                    speed = len(chunk) / 1024 / download_time if download_time > 0 else 0
                    
                    # 记录有效链接和速度
                    valid_urls.append(url)
                    url_speeds[url] = speed
                    
                    if progress_callback:
                        progress_callback(15, f"链接 {url} 测速完成，速度: {speed:.2f} KB/s")
        except Exception as e:
            if progress_callback:
                progress_callback(15, f"链接 {url} 连接失败: {str(e)}")
    
    # 选择最快的链接
    if valid_urls:
        # 按速度排序所有链接
        sorted_urls = sorted(url_speeds.items(), key=lambda x: x[1], reverse=True)
        fastest_url = sorted_urls[0][0]
        
        if progress_callback:
            # 报告最快的链接
            domain = urlparse(fastest_url).netloc
            speed = url_speeds[fastest_url]
            progress_callback(18, f"最快的链接: {fastest_url}，速度: {speed:.2f} KB/s")
            
            # 报告所有有效链接的速度（按速度排序）
            progress_callback(18, f"所有有效链接测速结果:")
            for url, speed in sorted_urls:
                progress_callback(18, f"链接 {url} 速度: {speed:.2f} KB/s")
    
    return valid_urls, url_speeds, fastest_url

def download_ffmpeg_file(url, target_dir=None, progress_callback=None):
    """下载FFmpeg文件
    
    Args:
        url (str): 下载链接
        target_dir (str, optional): 下载目标目录。默认为配置文件中指定的目录或app/ffmpeg目录。
        progress_callback (function, optional): 进度回调函数，接收下载进度百分比和状态消息。
    
    Returns:
        bool: 下载是否成功
    """
    import tempfile
    import zipfile
    import urllib.request
    from urllib.parse import urlparse
    
    # 设置目标目录
    if not target_dir:
        # 使用配置文件中的路径或默认路径
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if 'ffmpeg_path' in config:
                        target_dir = config['ffmpeg_path']
        except Exception as e:
            print(f"读取ffmpeg配置失败: {e}")
        
        # 如果配置中没有或读取失败，使用默认路径
        if not target_dir:
            target_dir = os.path.join(app_path, 'ffmpeg')
    
    # 确保目标目录存在
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, mode=0o755, exist_ok=True)
    
    # 创建临时文件用于下载
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
    temp_file.close()
    
    try:
        domain = urlparse(url).netloc
        if progress_callback:
            progress_callback(20, f"开始从 {domain} 下载FFmpeg...")
        
        # 设置下载进度回调
        def report_progress(block_num, block_size, total_size):
            if total_size > 0:
                percent = min(100, int(block_num * block_size * 100 / total_size))
                if progress_callback:
                    progress_callback(20 + percent * 0.6, f"正在下载FFmpeg... {percent}%")
        
        # 设置超时时间（秒）
        timeout_seconds = 10
        
        # 设置socket超时
        socket.setdefaulttimeout(timeout_seconds)
        
        # 下载文件
        urllib.request.urlretrieve(
            url,
            temp_file.name,
            reporthook=report_progress
        )
        
        if progress_callback:
            progress_callback(80, "下载完成，正在解压文件...")
        
        # 解压文件
        with zipfile.ZipFile(temp_file.name, 'r') as zip_ref:
            # 获取压缩包内的ffmpeg.exe路径
            ffmpeg_exe_path = None
            for file in zip_ref.namelist():
                if file.endswith('ffmpeg.exe'):
                    ffmpeg_exe_path = file
                    break
            
            if ffmpeg_exe_path:
                # 提取ffmpeg.exe到目标目录
                source = zip_ref.open(ffmpeg_exe_path)
                target = open(os.path.join(target_dir, 'ffmpeg.exe'), 'wb')
                shutil.copyfileobj(source, target)
                source.close()
                target.close()
                
                if progress_callback:
                    progress_callback(90, "FFmpeg解压完成")
                return True
            else:
                if progress_callback:
                    progress_callback(80, "压缩包中未找到ffmpeg.exe")
                return False
    except Exception as e:
        if progress_callback:
            progress_callback(0, f"下载失败: {str(e)}")
        return False
    finally:
        # 删除临时文件
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

def setup_ffmpeg_directory(target_dir, progress_callback=None):
    """设置FFmpeg目录
    
    Args:
        target_dir (str): FFmpeg目录
        progress_callback (function, optional): 进度回调函数
    
    Returns:
        bool: 设置是否成功
    """
    try:
        # 确保目标目录存在
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, mode=0o755, exist_ok=True)
        
        # 检查ffmpeg.exe是否存在
        ffmpeg_exe_path = os.path.join(target_dir, 'ffmpeg.exe')
        if not os.path.exists(ffmpeg_exe_path):
            if progress_callback:
                progress_callback(95, "FFmpeg安装失败: 未找到ffmpeg.exe")
            return False
        
        # 更新配置文件
        try:
            config = {}
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            
            config['ffmpeg_path'] = target_dir
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            
            # 更新全局变量
            global ffmpeg_path
            ffmpeg_path = ffmpeg_exe_path
            
            if progress_callback:
                progress_callback(100, "FFmpeg安装完成")
            
            return True
        except Exception as e:
            if progress_callback:
                progress_callback(95, f"更新配置文件失败: {str(e)}")
            return False
    except Exception as e:
        if progress_callback:
            progress_callback(95, f"设置FFmpeg目录失败: {str(e)}")
        return False

def download_ffmpeg(target_dir=None, progress_callback=None):
    """下载FFmpeg到指定目录 (兼容旧版本调用)
    
    Args:
        target_dir (str, optional): 下载目标目录。默认为配置文件中指定的目录或app/ffmpeg目录。
        progress_callback (function, optional): 进度回调函数，接收下载进度百分比和状态消息。
    
    Returns:
        bool: 下载是否成功
    """
    # 第一步：获取并测试下载链接
    valid_urls, url_speeds, fastest_url = get_ffmpeg_download_urls(progress_callback)
    
    # 检查是否有有效链接
    if not valid_urls or not fastest_url:
        return False
    
    # 第二步：下载FFmpeg
    success = download_ffmpeg_file(fastest_url, target_dir, progress_callback)
    if not success:
        # 如果下载失败，尝试使用下一个最快的链接
        if len(valid_urls) > 1:
            # 移除失败的链接
            valid_urls.remove(fastest_url)
            url_speeds.pop(fastest_url)
            
            # 选择下一个最快的链接
            if url_speeds:
                next_fastest_url = max(url_speeds.items(), key=lambda x: x[1])[0]
                if progress_callback:
                    from urllib.parse import urlparse
                    domain = urlparse(next_fastest_url).netloc
                    progress_callback(20, f"尝试使用下一个最快的链接: {domain}")
                
                # 再次尝试下载
                success = download_ffmpeg_file(next_fastest_url, target_dir, progress_callback)
    
    # 第三步：设置FFmpeg目录
    if success:
        return setup_ffmpeg_directory(target_dir, progress_callback)
    
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
            os.makedirs(output_dir, mode=0o755, exist_ok=True)
    
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
        os.makedirs(src, mode=0o755)  # 设置读写权限
    else:
        raise Error('文件夹已存在')

def createFile(src):
    # 创建文件
    if not path.exists(src):
        with open(src, 'w', encoding='utf-8') as f:
            f.write('')
        os.chmod(src, 0o644)  # 设置读写权限
    else:
        raise Error('文件已存在')

def createJsonFile(src, content={}):
    # 创建json文件
    if not path.exists(src):
        with open(src, 'w', encoding='utf-8') as f:
            f.write(json.dumps(content, ensure_ascii=False, indent=4))
        os.chmod(src, 0o644)  # 设置读写权限
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
    try:
        if path.exists(src):
            # 尝试移除只读属性
            os.chmod(src, 0o777)
            os.remove(src)
        else:
            raise Error('文件不存在')
    except PermissionError:
        # 如果普通删除失败,尝试使用系统命令强制删除
        import subprocess
        try:
            if os.name == 'nt':  # Windows系统
                subprocess.run(['del', '/f', '/q', src], shell=True, check=True)
            else:  # Unix/Linux系统
                subprocess.run(['rm', '-f', src], check=True)
        except subprocess.CalledProcessError:
            raise Error('文件删除失败:权限不足或文件被占用')
    except Exception as e:
        raise Error(f'文件删除失败:{str(e)}')

def delJsonFile(src):
    # 删除json文件
    if path.exists(src):
        os.remove(src)
    else:
        raise Error('文件不存在')


def copyFile(src, dst):
    # 复制文件到指定文件夹
    # 判断目标路径是否包含文件名(有后缀)
    if not os.path.splitext(dst)[1]:
        # 没有后缀时创建目标文件夹
        if not path.exists(dst):
            os.makedirs(dst, mode=0o755)  # 设置读写权限
    
    # 使用copy2保留文件的元数据信息
    shutil.copy2(src, dst)


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
    if not os.path.splitext(dst)[1]:
        # 没有后缀时创建目标文件夹
        if not path.exists(dst):
            os.makedirs(dst, mode=0o755)  # 设置读写权限
    # 移动文件到指定文件夹
    shutil.move(src, dst)

def toPack(src, dst, name='pack'):

    # 压缩文件夹，进行打包
    if path.exists(src):
        # 检查源目录权限
        try:
            if not os.access(src, os.R_OK | os.X_OK):
                raise Error(f"源目录 {src} 无读取权限，请检查权限设置")
        except Exception as e:
            print(f"源目录权限检查失败: {str(e)}")
            raise Error(f"源目录 {src} 权限检查失败: {str(e)}")
        # 确保目标目录存在且可写
        try:
            if not os.path.exists(dst):
                os.makedirs(dst, mode=0o755)  # 设置读写权限
            # 测试目标目录是否可写
            test_file = os.path.join(dst, "test_write_permission.tmp")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
        except (PermissionError, OSError) as e:
            print(f"目标目录权限错误: {str(e)}")
            raise Error(f"目标目录 {dst} 无法访问或写入，请检查权限或关闭占用该目录的程序")
            
        # 检查目标文件是否存在
        target_file = os.path.join(dst, name + '.zip')
        
        # 检查目标文件是否被占用
        if path.exists(target_file):
            try:
                # 尝试打开文件，如果能打开，说明文件没有被占用
                with open(target_file, 'a+b') as f:
                    pass
                # 文件存在但未被占用，删除它
                os.remove(target_file)
                print(f"已删除现有文件: {target_file}")
            except PermissionError:
                # 文件被占用，尝试解除占用
                try:
                    import psutil
                    found_process = False
                    for proc in psutil.process_iter(['pid', 'name', 'open_files']):
                        try:
                            for file in proc.info.get('open_files') or []:
                                if file.path == target_file:
                                    print(f"文件被进程 {proc.info['name']} (PID: {proc.info['pid']}) 占用，尝试结束进程...")
                                    proc.terminate()
                                    proc.wait(timeout=3)
                                    found_process = True
                                    break
                        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                            pass
                    
                    if not found_process:
                        print(f"未找到占用文件的进程，尝试强制删除文件")
                    
                    # 再次尝试删除文件
                    if path.exists(target_file):
                        try:
                            os.remove(target_file)
                            print(f"已成功删除被占用的文件: {target_file}")
                        except PermissionError:
                            # 如果仍然无法删除，尝试使用Windows特定方法
                            import ctypes
                            if ctypes.windll.kernel32.MoveFileExW(target_file, None, 4): # MOVEFILE_DELAY_UNTIL_REBOOT
                                print(f"文件将在系统重启后删除: {target_file}")
                            else:
                                raise Error(f"无法删除文件: {target_file}")
                except ImportError:
                    print("未安装psutil库，无法检测文件占用进程")
                    raise Error(f"文件被占用且无法解除: {target_file}，请安装psutil库或手动关闭占用程序")
                except Exception as e:
                    print(f"尝试解除文件占用失败: {str(e)}")
                    raise Error(f"文件被占用且无法解除: {target_file}")
        
        try:
            # 打包并重命名
            shutil.make_archive(os.path.join(dst, name), 'zip', src)
            print(f"成功创建压缩包: {os.path.join(dst, name)}.zip")
        except PermissionError as e:
            print(f"创建压缩包时权限错误: {str(e)}")
            raise Error(f"无法创建压缩包，目录 {dst} 可能被占用或没有写入权限")
        except Exception as e:
            print(f"创建压缩包时发生错误: {str(e)}")
            raise Error(f"创建压缩包失败: {str(e)}")
    else:
        raise Error(f"源目录不存在: {src}")

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
    
def getProject(pj_name):
    from core.project.main import Project
    # 获取项目
    if projectExists(pj_name):
        pj_path = path.join(project_path, pj_name, "sounds" + exeSuffixName)
        return Project.load(pj_path)
    else:
        raise Error('项目不存在')

def saveProjectHistory(project_name: str):
    """保存项目到历史记录
    
    Args:
        project_name (str): 项目名称
    
    Returns:
        bool: 是否保存成功
    """
    try:
        # 检查项目是否存在
        if not projectExists(project_name):
            return False
        
        # 获取项目路径
        project_path_str = path.join(project_path, project_name)
        project_file = path.join(project_path_str, "sounds" + exeSuffixName)
        
        # 获取当前时间
        current_time = int(time.time())
        
        # 读取历史记录
        history = getProjectHistory()
        
        # 检查项目是否已在历史记录中
        for item in history:
            if item.get("name") == project_name:
                # 更新访问时间
                item["last_access"] = current_time
                break
        else:
            # 添加新项目到历史记录
            history.append({
                "name": project_name,
                "path": project_file,
                "last_access": current_time
            })
        
        # 按最后访问时间排序（降序）
        history.sort(key=lambda x: x.get("last_access", 0), reverse=True)
        
        # 限制历史记录数量（保留最近的10个）
        if len(history) > 10:
            history = history[:10]
        
        # 保存历史记录
        with open(history_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=4)
        
        return True
    except Exception as e:
        print(f"保存历史记录失败: {str(e)}")
        return False

def getProjectHistory():
    """获取项目历史记录
    
    Returns:
        list: 项目历史记录列表，按最后访问时间降序排序
    """
    try:
        if path.exists(history_path):
            with open(history_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
            
            # 过滤掉不存在的项目
            valid_history = []
            for item in history:
                project_name = item.get("name")
                if project_name and projectExists(project_name):
                    valid_history.append(item)
            
            return valid_history
        else:
            # 如果历史记录文件不存在，创建空文件
            with open(history_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
            return []
    except Exception as e:
        print(f"获取历史记录失败: {str(e)}")
        return []


def toPinyin(text: str):
    # 转换为拼音
    return pinyin(text, style=STYLE_NORMAL, heteronym=True)

def toPinyinFirst(text: str):
    # 转换为拼音首字母
    return ''.join([i[0] for i in toPinyin(text)])

def toPinyinFirstUpper(text: str):
    # 转换为拼音首字母大写
    return ''.join([i[0].upper() for i in toPinyin(text)])

def toPinyinFirstLower(text: str):
    # 转换为拼音首字母小写
    return ''.join([i[0].lower() for i in toPinyin(text)])

def TextSplit(text: str) -> str:
    """传入中文，把每个字进行分割，随机取三个字
    
    Args:
        text (str): 输入的中文文本
        
    Returns:
        str: 如果输入长度>=5,返回随机5个字;否则返回原文本
    """
    import random
    import re
    import random
    
    # 检查输入是否为空或非字符串类型
    if not text or not isinstance(text, str):
        return ""
    
    # 优化字符过滤,使用set提高查找效率
    invalid_chars = {'\n', '\r', ' ', '\t'}  # 添加制表符到过滤集合
    
    # 移除标点符号和特殊字符
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', text)
    
    # 使用生成器表达式优化内存使用
    chars = [char for char in text if char not in invalid_chars and char.strip()]
    
    # 优化长度判断和随机选择
    char_count = len(chars)
    if char_count >= 5:
        # 使用切片优化random.sample性能
        if char_count > 10:  # 对于较长的文本,先随机选择一个较小的子集
            chars = random.sample(chars, min(10, char_count))
        return ''.join(random.sample(chars, 3))
    
    # 返回过滤后的原文本
    return ''.join(chars)

def cnTextToPinyinFirst(text: str) -> str:
    """传入中文，把每个字进行分割，随机取三个字，然后转成拼音首字母
    
    Args:
        text (str): 输入的中文文本
        
    Returns:
        str: 如果输入长度>=5,返回随机3个字的拼音首字母;否则返回原文本
    """
    # 先对中文进行分割获取三个字符
    chars = TextSplit(text)
    if not chars:
        return ""
        
    # 获取每个字符的拼音列表
    pinyin_list = toPinyin(chars)
    
    # 提取每个拼音的首字母并拼接
    result = []
    for py in pinyin_list:
        if py and py[0]:  # 确保拼音列表不为空
            # 取拼音首字母并转小写
            first_letter = py[0][0].lower()
            result.append(first_letter)
            
    # 直接返回拼音首字母拼接结果
    return ''.join(result)

def enTextToFirst(text: str) -> str:
    """传入英文，把每个字进行分割，随机取五个字，然后转成字母
    
    Args:
        text (str): 输入的英文文本
        
    Returns:
        str: 如果输入长度>=5,返回随机5个字的英文首字母;否则返回原文本
    """
    # 先对英文进行分割获取五个字符
    chars = TextSplit(text)
    if not chars:
        return ""
        
    # 如果字符长度大于等于5,随机取5个字符
    if len(chars) >= 5:
        selected_chars = ''.join(random.sample(chars, 5))
        return selected_chars.lower()
    
    # 长度小于5时返回原文本小写形式
    return chars.lower()
