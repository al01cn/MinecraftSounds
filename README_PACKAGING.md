# MinecraftSounds 打包说明

## 问题描述

在使用PyInstaller打包MinecraftSounds应用程序时，安装包版本可能会出现以下错误：

```
Failed to load Python DLL 'D:\Vscode\python\MinecraftSounds\build\MinecraftSoundsApp\internal\python312.dll'.
LoadLibrary: 找不到指定的模块。
```

这是因为PyInstaller在打包时没有正确包含所有必要的Python DLL文件，或者DLL文件没有被放置在正确的位置。

## 解决方案

我们已经修改了打包脚本和配置文件，以确保所有必要的DLL文件都被正确包含在打包结果中：

1. 修改了`MinecraftSounds.spec`文件，添加了Python DLL和其他必要的DLL文件
2. 添加了运行时钩子，确保应用程序能够正确加载DLL文件
3. 简化了`build.py`文件，使用spec文件进行打包
4. 添加了`fix_dll.bat`脚本，用于快速修复DLL加载问题

## 使用方法

1. 确保已安装所有依赖：
   ```
   pip install -r requirements.txt
   ```

2. 运行打包脚本：
   ```
   python build.py
   ```
   或者直接运行批处理文件：
   ```
   build.bat
   ```

3. 打包完成后，可以在以下位置找到打包结果：
   - 可执行文件版本：`build\MinecraftSounds`
   - 安装包版本：`build\MinecraftSoundsApp`

## 修复DLL加载问题

如果运行安装包版本时出现Python DLL加载错误，可以使用以下方法修复：

1. 运行项目根目录下的`fix_dll.bat`脚本：
   ```
   fix_dll.bat
   ```
   该脚本会自动将必要的DLL文件从`_internal`目录复制到应用程序根目录。

2. 手动修复：
   - 进入`build\MinecraftSoundsApp\MinecraftSounds\_internal`目录
   - 复制所有`python*.dll`、`VCRUNTIME*.dll`和`ucrtbase.dll`文件
   - 粘贴到`build\MinecraftSoundsApp\MinecraftSounds`目录

## 注意事项

1. 如果仍然出现DLL加载错误，请检查以下几点：
   - 确保使用的Python版本与打包时使用的版本相同
   - 检查`MinecraftSounds.spec`文件中的DLL模式是否包含了所有必要的DLL
   - 尝试手动复制缺失的DLL文件到应用程序目录
   - 确保应用程序根目录中包含`python312.dll`和`python3.dll`文件（版本号可能不同）

2. 对于不同的Python版本，可能需要调整`MinecraftSounds.spec`文件中的Python版本号：
   ```python
   python_version = f"{sys.version_info.major}{sys.version_info.minor}"
   python_dll = f"python{python_version}.dll"
   ```

3. 如果使用的是虚拟环境，请确保在虚拟环境中运行打包脚本。

4. 如果修复后仍然出现问题，可以尝试使用可执行文件版本（`build\MinecraftSounds`目录），该版本通常更稳定。