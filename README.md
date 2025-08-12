# Minecraft Sounds 应用程序

这是一个用于管理和创建Minecraft音效包的应用程序。

## 功能特点

- 创建和管理Minecraft音效包项目
- 导入和编辑音效文件
- 支持多种Minecraft版本
- 导出符合Minecraft格式的音效资源包
- 功能简单易用

## 使用方法

1. 打开应用程序
2. 创建新项目或打开现有项目
3. 添加音频，系统会自动把添加的音频生成一个对应的soundkey
4. 导出项目，系统会自动把项目导出为一个资源包和对应的命令

## 开发

### 激活虚拟环境Linux

```bash
source venv/Scripts/activate
```

### 激活虚拟环境Windows

```bash
venv\Scripts\activate
```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行应用

```bash
python main.py
```

## 打包应用

### 打包为可执行文件和安装包

```bash
python build.py
```

打包后的文件将保存在 `build` 目录中：

- `build/MinecraftSounds/` - 可执行文件版本（建议使用）
- `build/MinecraftSoundsApp/` - 安装包版本（还有bug，不建议使用）

## 项目结构

- `app/` - 应用资源文件
  - `assets/` - 图标、字体等资源
  - `ffmpeg/` - 音频处理工具
  - `projects/` - 用户项目存储目录
  - `config.json` - 配置文件
  - `history.json` - 最近项目历史
  - `mc.ver` - Minecraft游戏版本文件
- `core/` - 核心功能模块
- `gui/` - 图形界面模块
- `utils/` - 工具函数
- `main.py` - 程序入口
- `build.py` - 打包脚本

## 注意事项

- 应用需要管理员权限运行
- 需要安装FFmpeg（应用会自动下载）
- 打包时确保已安装所有依赖

## 项目依赖

- Python 3.12.2
- PyQt5
- FFmpeg