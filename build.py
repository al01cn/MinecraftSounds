import os
import sys
import shutil
import subprocess
import site
import glob
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent
# 构建输出目录
BUILD_DIR = ROOT_DIR / 'build'
# 应用名称
APP_NAME = 'MinecraftSounds'

# 确保构建目录存在
BUILD_DIR.mkdir(exist_ok=True)

# 清理之前的构建文件
def clean_build():
    print("清理之前的构建文件...")
    app_build_dir = BUILD_DIR / APP_NAME
    app_dir = BUILD_DIR / f"{APP_NAME}App"
    
    if app_build_dir.exists():
        shutil.rmtree(app_build_dir)
    if app_dir.exists():
        shutil.rmtree(app_dir)

# 构建可执行文件版本
def build_exe():
    print("正在构建可执行文件版本...")
    # 使用PyInstaller打包，使用spec文件
    cmd = [
        'pyinstaller',
        '--clean',  # 清理临时文件
        '--distpath', os.path.join('build'),  # 输出到build目录
        '--workpath', os.path.join('build', 'temp'),  # 临时文件目录
        'MinecraftSounds.spec'  # 使用spec文件
    ]
    
    subprocess.run(cmd, check=True)
    print("可执行文件版本构建完成！")

# 复制所有必要的Python DLL文件
def copy_python_dlls(target_dir):
    print("复制Python DLL文件...")
    # 获取Python安装目录
    python_dir = Path(sys.executable).parent
    python_version = f"{sys.version_info.major}{sys.version_info.minor}"
    
    # 主Python DLL
    main_dll = f"python{python_version}.dll"
    python3_dll = "python3.dll"
    
    # 从_internal目录复制DLL到应用程序根目录
    internal_dir = target_dir / "_internal"
    if internal_dir.exists():
        print("从_internal目录复制DLL到应用程序根目录...")
        for dll_file in internal_dir.glob("*.dll"):
            if dll_file.name.startswith("python") or dll_file.name.startswith("VCRUNTIME") or dll_file.name == "ucrtbase.dll":
                dest_file = target_dir / dll_file.name
                if not dest_file.exists():
                    shutil.copy2(dll_file, dest_file)
                    print(f"已复制 {dll_file.name} 到应用程序根目录")
    
    # 如果_internal目录不存在或没有找到DLL，则从Python目录复制
    if not (target_dir / main_dll).exists() or not (target_dir / python3_dll).exists():
        print("从Python安装目录复制DLL...")
        # 主Python DLL
        if (python_dir / main_dll).exists():
            shutil.copy2(python_dir / main_dll, target_dir / main_dll)
            print(f"已复制 {main_dll}")
        else:
            print(f"警告: 未找到 {main_dll}")
        
        # Python3 DLL
        if (python_dir / python3_dll).exists():
            shutil.copy2(python_dir / python3_dll, target_dir / python3_dll)
            print(f"已复制 {python3_dll}")
        else:
            print(f"警告: 未找到 {python3_dll}")
        
        # 复制其他Python DLL文件
        dll_patterns = [
            f"python{python_version}*.dll",  # 例如 python39.dll, python39_d.dll
            "python3*.dll",                 # python3.dll
            "vcruntime*.dll",               # Visual C++ runtime
            "VCRUNTIME*.dll",
            "api-ms-win-*.dll",              # Windows API
            "ucrtbase*.dll"                 # Universal C Runtime
        ]
        
        # 从Python目录复制DLL
        for pattern in dll_patterns:
            for dll_file in python_dir.glob(pattern):
                if dll_file.is_file():
                    dest_file = target_dir / dll_file.name
                    if not dest_file.exists():
                        shutil.copy2(dll_file, dest_file)
                        print(f"已复制 {dll_file.name}")
    
    # 从系统目录复制DLL
    system_dirs = [
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32'),
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'SysWOW64')
    ]
    
    # 检查是否有缺失的DLL
    print("检查是否有缺失的DLL...")
    try:
        # 尝试加载DLL，检查是否有缺失的依赖
        for dll_file in target_dir.glob("*.dll"):
            print(f"已包含: {dll_file.name}")
    except Exception as e:
        print(f"检查DLL时出错: {e}")
        pass

# 构建安装包版本
def build_installer():
    print("正在构建安装包版本...")
    # 创建安装包目录
    installer_dir = BUILD_DIR / f"{APP_NAME}App"
    installer_dir.mkdir(exist_ok=True)
    
    # 复制可执行文件和依赖到安装包目录
    shutil.copytree(
        BUILD_DIR / APP_NAME,
        installer_dir / APP_NAME,
        dirs_exist_ok=True
    )
    
    # 创建安装包启动器
    with open(installer_dir / f"{APP_NAME}.exe", 'wb') as f:
        # 复制原始可执行文件
        with open(BUILD_DIR / APP_NAME / f"{APP_NAME}.exe", 'rb') as src:
            f.write(src.read())
    
    # 复制所有必要的Python DLL
    copy_python_dlls(installer_dir / APP_NAME)
    
    print("安装包版本构建完成！")

# 主函数
def main():
    try:
        # 清理之前的构建
        clean_build()
        
        # 构建可执行文件版本
        build_exe()
        
        # 构建安装包版本
        build_installer()
        
        print(f"\n构建成功！输出目录: {BUILD_DIR}")
        print(f"1. 可执行文件版本: {BUILD_DIR / APP_NAME}")
        print(f"2. 安装包版本: {BUILD_DIR / f'{APP_NAME}App'}")
        
    except Exception as e:
        print(f"构建失败: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())