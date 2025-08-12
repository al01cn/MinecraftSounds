# Minecraft Sounds 应用程序

这是一个用于管理和创建Minecraft音效包的应用程序。

## 功能特点

- 创建和管理Minecraft音效包项目
- 导入和编辑音效文件
- 支持多种Minecraft版本
- 导出符合Minecraft格式的音效资源包

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行应用

```bash
python main.py
```

## 打包应用

### 打包为可执行文件和安装包

```bash
python build.py
```

打包后的文件将保存在 `build` 目录中：

- `build/MinecraftSounds/` - 可执行文件版本
- `build/MinecraftSoundsApp/` - 安装包版本

## 项目结构

- `app/` - 应用资源文件
  - `assets/` - 图标、字体等资源
  - `ffmpeg/` - 音频处理工具
  - `projects/` - 用户项目存储目录
- `core/` - 核心功能模块
- `gui/` - 图形界面模块
- `utils/` - 工具函数
- `main.py` - 程序入口
- `build.py` - 打包脚本

## 注意事项

- 应用需要管理员权限运行
- 需要安装FFmpeg（应用会自动下载）
- 打包时确保已安装所有依赖