import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.main import toOgg, Error

def test_ffmpeg_detection():
    """测试ffmpeg路径检测功能"""
    print("测试ffmpeg路径检测功能")
    
    # 检查app/ffmpeg目录是否存在
    app_ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'ffmpeg')
    if os.path.exists(app_ffmpeg_path):
        print(f"指定的ffmpeg文件夹存在: {app_ffmpeg_path}")
        
        # 检查ffmpeg.exe是否存在
        ffmpeg_exe = os.path.join(app_ffmpeg_path, 'ffmpeg.exe')
        if os.path.exists(ffmpeg_exe):
            print(f"ffmpeg.exe存在: {ffmpeg_exe}")
        else:
            print(f"ffmpeg.exe不存在: {ffmpeg_exe}")
    else:
        print(f"指定的ffmpeg文件夹不存在: {app_ffmpeg_path}")
    
    # 尝试调用toOgg函数
    try:
        # 由于没有实际的音频文件，这里只是测试函数的ffmpeg检测部分
        # 创建一个临时的空文件作为测试
        test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_temp.mp3')
        with open(test_file, 'w') as f:
            f.write("This is a test file, not a real MP3")
        
        print("\n尝试调用toOgg函数...")
        try:
            # 测试默认参数
            print("测试默认质量参数...")
            toOgg(test_file)
        except Error as e:
            # 预期会因为不是真正的MP3文件而失败，但应该能看到ffmpeg路径检测的输出
            print(f"预期的错误(默认参数): {e}")
            
        try:
            # 测试自定义质量参数
            print("\n测试自定义质量参数...")
            toOgg(test_file, quality="256k")
        except Error as e:
            print(f"预期的错误(自定义质量): {e}")
            
        try:
            # 测试自定义ffmpeg参数
            print("\n测试自定义ffmpeg参数...")
            toOgg(test_file, parameters=["-q:a", "8"])
        except Error as e:
            print(f"预期的错误(自定义参数): {e}")
        
        # 清理临时文件
        if os.path.exists(test_file):
            os.remove(test_file)
            
    except Exception as e:
        print(f"测试过程中出现错误: {e}")

if __name__ == "__main__":
    test_ffmpeg_detection()