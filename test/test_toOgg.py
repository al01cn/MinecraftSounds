import os
from utils.main import toOgg

def test_toOgg():
    # 测试文件路径，请替换为实际存在的音频文件
    test_file = "test_audio.mp3"  # 假设当前目录下有一个test_audio.mp3文件
    
    if not os.path.exists(test_file):
        print(f"测试文件 {test_file} 不存在，请提供一个有效的音频文件路径")
        return
    
    try:
        # 调用toOgg函数进行转换
        output_path = toOgg(test_file)
        print(f"转换成功！输出文件: {output_path}")
        
        # 检查输出文件是否存在
        if os.path.exists(output_path):
            print(f"输出文件大小: {os.path.getsize(output_path) / 1024:.2f} KB")
        else:
            print("输出文件不存在，转换可能失败")
    
    except Exception as e:
        print(f"转换失败: {str(e)}")

if __name__ == "__main__":
    test_toOgg()