import subprocess
import sys

# 创建补丁函数，用于在Windows系统上隐藏ffmpeg控制台窗口
def apply_pydub_patch():
    """
    应用pydub补丁，防止在Windows系统上调用ffmpeg时弹出控制台窗口
    """
    if sys.platform != 'win32':
        # 非Windows系统不需要应用此补丁
        return
    
    try:
        # 保存原始的subprocess.Popen函数
        original_popen = subprocess.Popen
        
        # 创建一个新的Popen函数，添加startupinfo参数
        def patched_popen(*args, **kwargs):
            # 只有在Windows系统上才添加startupinfo参数
            if sys.platform == 'win32':
                # 创建startupinfo对象
                startupinfo = subprocess.STARTUPINFO()
                # 设置dwFlags，使窗口不显示
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                # 添加startupinfo参数
                kwargs['startupinfo'] = startupinfo
            # 调用原始的Popen函数
            return original_popen(*args, **kwargs)
        
        # 替换全局的subprocess.Popen函数
        subprocess.Popen = patched_popen
        
        print("已应用pydub补丁，防止ffmpeg弹出控制台窗口")
        return True
    except Exception as e:
        print(f"应用pydub补丁失败: {e}")
        return False