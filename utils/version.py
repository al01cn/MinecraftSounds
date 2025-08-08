import re

class Version:
    def __init__(self, version: str = "0.0.0", beta: bool = False):
        self.version = version
        self.beta = beta

    def __str__(self):
        return self.version if not self.beta else self.version + "-beta"

    def replaceBeta(self, beta: bool):
        self.beta = beta

    @staticmethod
    def validate_version(version_str):
        """验证版本号格式是否正确
        版本号格式: X.Y.Z[-beta]
        其中:
            X, Y, Z 为非负整数
            -beta 为可选的测试版标识
        返回值:
            True : 版本号格式正确
            False : 版本号格式错误
        """

        pattern = r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$'
        if re.match(pattern, version_str):
            return True
        else:
            return False
    
    @staticmethod
    def compare_simple_versions(version1: str, version2: str) -> int:
        """比较两种简化版本号
        简化版本号格式: X.Y.Z
        其中:
            X, Y, Z 为非负整数
            版本号必须为三段式, 例如: 1.0.0, 2.3.4
        版本号比较规则:
            先比较主版本号, 主版本号相同则比较次版本号, 次版本号相同则比较修订版本号
            测试版版本号大于正式版版本号
            版本号相同, 测试版版本号大于正式版版本号
        例子:
            1.0.0 < 1.0.1 |
            1.0.0 < 1.1.0 |
            1.0.0 < 2.0.0 |
            1.0.0-beta < 1.0.0 |
            1.0.0 < 1.0.0-beta |
        返回值: 
            -1 : version1 < version2
             0 : version1 == version2
             1 : version1 > version2
        """
        # 提取基础版本和版本类型
        v1_base = version1.replace("-beta", "")
        v2_base = version2.replace("-beta", "")
        v1_is_beta = version1.endswith("-beta")
        v2_is_beta = version2.endswith("-beta")
    
        # 解析基础版本为整数列表
        try:
            v1_parts = list(map(int, v1_base.split('.')))
            v2_parts = list(map(int, v2_base.split('.')))
        except ValueError:
            raise ValueError("Invalid version format")
    
        # 确保三段式版本号
        if len(v1_parts) != 3 or len(v2_parts) != 3:
            raise ValueError("Version must have three parts: major.minor.patch")
    
        # 比较基础版本
        for i in range(3):
            if v1_parts[i] < v2_parts[i]:
                return -1
        if v1_parts[i] > v2_parts[i]:
            return 1
    
        # 基础版本相同，比较类型
        if not v1_is_beta and v2_is_beta:  # v1是正式版，v2是测试版
            return 1
        if v1_is_beta and not v2_is_beta:  # v1是测试版，v2是正式版
            return -1
        return 0  # 两者都是测试版或都是正式版

    @staticmethod
    def increment_version(version) -> str:
        """
        增加版本号（只增加修订号）
        
        参数:
            version: 当前版本号（格式为 x.y.z 或 x.y.z-beta），可以是字符串或 Version 对象
            
        返回:
            增加后的版本号（保持相同的版本类型）
        """
        # 如果是 Version 对象，获取其字符串表示
        if isinstance(version, Version):
            version_str = str(version)
        else:
            version_str = str(version)
            
        # 检查是否是测试版
        is_beta = version_str.endswith("-beta")
        
        # 移除测试版后缀
        base_version = version_str.replace("-beta", "") if is_beta else version_str
        
        # 分割版本号
        parts = base_version.split('.')
        if len(parts) != 3:
            raise ValueError(f"Invalid version format: {version_str}")
        
        # 转换为整数
        try:
            major = int(parts[0])
            minor = int(parts[1])
            patch = int(parts[2])
        except ValueError:
            raise ValueError(f"Invalid version format: {version_str}")
        
        # 增加修订号
        patch += 1
        
        # 重新组合版本号
        new_version = f"{major}.{minor}.{patch}"
        
        # 如果是测试版，添加后缀
        if is_beta:
            new_version += "-beta"
        
        return new_version

    @staticmethod
    def decrement_version(version) -> str:
        """
        减少版本号（只减少修订号，不会低于0）
        
        参数:
            version: 当前版本号（格式为 x.y.z 或 x.y.z-beta），可以是字符串或 Version 对象
            
        返回:
            减少后的版本号（保持相同的版本类型）
        """
        # 如果是 Version 对象，获取其字符串表示
        if isinstance(version, Version):
            version_str = str(version)
        else:
            version_str = str(version)
            
        # 检查是否是测试版
        is_beta = version_str.endswith("-beta")
        
        # 移除测试版后缀
        base_version = version_str.replace("-beta", "") if is_beta else version_str
        
        # 分割版本号
        parts = base_version.split('.')
        if len(parts) != 3:
            raise ValueError(f"Invalid version format: {version_str}")
        
        # 转换为整数
        try:
            major = int(parts[0])
            minor = int(parts[1])
            patch = int(parts[2])
        except ValueError:
            raise ValueError(f"Invalid version format: {version_str}")
        
        # 减少修订号（不低于0）
        patch = max(0, patch - 1)
        
        # 重新组合版本号
        new_version = f"{major}.{minor}.{patch}"
        
        # 如果是测试版，添加后缀
        if is_beta:
            new_version += "-beta"
        
        return new_version