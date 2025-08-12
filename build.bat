@echo off
echo 正在打包 Minecraft Sounds 应用程序...

:: 检查Python环境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请安装Python 3.6+
    pause
    exit /b 1
)

:: 检查依赖
echo 正在检查依赖...
pip install -r requirements.txt

:: 运行打包脚本
echo 正在运行打包脚本...
python build.py

if %errorlevel% neq 0 (
    echo 打包失败，请查看上面的错误信息
) else (
    echo 打包完成！
    echo 可执行文件版本: %~dp0build\MinecraftSounds
    echo 安装包版本: %~dp0build\MinecraftSoundsApp
    echo.
    echo 如果仍然出现DLL加载错误，请参考README_PACKAGING.md文件
)

pause