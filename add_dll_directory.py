
# 运行时钩子，添加DLL搜索路径
import os
import sys

# 添加当前目录到DLL搜索路径
if hasattr(os, 'add_dll_directory'):
    os.add_dll_directory(os.path.dirname(sys.executable))
