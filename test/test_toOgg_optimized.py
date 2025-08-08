import os
import sys
import tempfile
from utils.main import toOgg, Error

def test_toOgg_optimized():
    print("测试优化后的 toOgg 函数")
    
    # 测试场景1: 输出到目录
    try:
        # 创建临时目录作为输出目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 假设有一个测试音频文件
            test_file = "d:\\Vscode\\python\\MinecraftSounds\\app\\assets\\test_audio.mp3"
            
            # 如果测试文件不存在，创建一个空的测试文件
            if not os.path.exists(test_file):
                print(f"测试文件 {test_file} 不存在，跳过测试")
            else:
                # 测试转换到目录
                output_path = toOgg(test_file, temp_dir)
                print(f"测试1成功: 输出文件路径 {output_path}")
                
                # 验证输出文件是否存在
                if os.path.exists(output_path):
                    print(f"输出文件存在，大小: {os.path.getsize(output_path)} 字节")
                else:
                    print("错误: 输出文件不存在")
    except Error as e:
        print(f"测试1失败: {str(e)}")
    
    # 测试场景2: 输出到指定文件路径
    try:
        # 创建临时文件作为输出文件
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as temp_file:
            temp_path = temp_file.name
        
        # 删除临时文件，让函数创建它
        os.unlink(temp_path)
        
        # 假设有一个测试音频文件
        test_file = "d:\\Vscode\\python\\MinecraftSounds\\app\\assets\\test_audio.mp3"
        
        # 如果测试文件不存在，创建一个空的测试文件
        if not os.path.exists(test_file):
            print(f"测试文件 {test_file} 不存在，跳过测试")
        else:
            # 测试转换到指定文件
            output_path = toOgg(test_file, temp_path)
            print(f"测试2成功: 输出文件路径 {output_path}")
            
            # 验证输出文件是否存在
            if os.path.exists(output_path):
                print(f"输出文件存在，大小: {os.path.getsize(output_path)} 字节")
                # 清理
                os.unlink(output_path)
            else:
                print("错误: 输出文件不存在")
    except Error as e:
        print(f"测试2失败: {str(e)}")
    
    # 测试场景3: 处理已经是ogg格式的文件
    try:
        # 创建临时ogg文件
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as temp_file:
            temp_file.write(b"fake ogg data")
            test_ogg = temp_file.name
        
        # 创建临时目录作为输出目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 测试复制到目录
            output_path = toOgg(test_ogg, temp_dir)
            print(f"测试3成功: 输出文件路径 {output_path}")
            
            # 验证输出文件是否存在
            if os.path.exists(output_path):
                print(f"输出文件存在，大小: {os.path.getsize(output_path)} 字节")
            else:
                print("错误: 输出文件不存在")
        
        # 清理
        os.unlink(test_ogg)
    except Error as e:
        print(f"测试3失败: {str(e)}")

if __name__ == "__main__":
    test_toOgg_optimized()