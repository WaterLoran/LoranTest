import time
import random
import hashlib


class PositionTestDataGenerator:
    """岗位测试数据生成器"""
    
    @staticmethod
    def generate_position_name(prefix="position"):
        """生成唯一的岗位名称"""
        timestamp = int(time.time())
        random_suffix = random.randint(1000, 9999)
        return f"{prefix}_test_{timestamp}_{random_suffix}"
    
    @staticmethod
    def generate_position_code(prefix="POST"):
        """生成唯一的岗位编码"""
        timestamp = int(time.time())
        random_suffix = random.randint(1000, 9999)
        return f"{prefix}_TEST_{timestamp}_{random_suffix}"
    
    @staticmethod
    def generate_position_data(prefix="position", **overrides):
        """生成完整的岗位测试数据
        
        Args:
            prefix: 数据前缀
            **overrides: 覆盖默认值的参数
        
        Returns:
            dict: 岗位测试数据
        """
        timestamp = int(time.time())
        random_suffix = random.randint(1000, 9999)
        
        # 生成唯一标识
        unique_string = f"{timestamp}_{random_suffix}"
        hash_part = hashlib.md5(unique_string.encode()).hexdigest()[:6]
        
        # 基础数据
        base_data = {
            "positionName": f"{prefix}_name_{timestamp}_{hash_part}",
            "positionCode": f"{prefix}_code_{timestamp}_{hash_part}".upper(),
            "postSort": random.randint(1, 100),
            "status": "0",  # 默认启用
            "remark": f"自动化测试创建的岗位_{timestamp}"
        }
        
        # 应用覆盖参数
        if overrides:
            base_data.update(overrides)
        
        return base_data
    
    @staticmethod
    def generate_boundary_test_cases():
        """生成边界值测试用例
        
        Returns:
            list: 边界值测试用例列表
        """
        timestamp = int(time.time())
        
        return [
            # 最大长度测试
            {
                "positionName": "a" * 50,  # 50个字符，最大长度
                "positionCode": "A" * 64,  # 64个字符，最大长度
                "postSort": 0,             # 最小排序值
                "status": "0",
                "remark": "边界测试：最大长度字段"
            },
            # 最小长度测试
            {
                "positionName": "测",
                "positionCode": "P",
                "postSort": 999,           # 最大排序值
                "status": "1",             # 停用状态
                "remark": "边界测试：最小长度字段"
            },
            # 正常边界值
            {
                "positionName": f"正常岗位_{timestamp}",
                "positionCode": f"POST_NORMAL_{timestamp}",
                "postSort": 500,           # 中间值
                "status": "0",
                "remark": "边界测试：正常值"
            }
        ]
    
    @staticmethod
    def generate_validation_test_cases():
        """生成验证测试用例（无效数据）
        
        Returns:
            list: 验证测试用例列表
        """
        timestamp = int(time.time())
        
        return [
            # 空名称
            {
                "positionName": "",
                "positionCode": f"POST_EMPTY_NAME_{timestamp}",
                "postSort": 1,
                "status": "0",
                "remark": "验证测试：空名称"
            },
            # 空编码
            {
                "positionName": f"空编码岗位_{timestamp}",
                "positionCode": "",
                "postSort": 1,
                "status": "0",
                "remark": "验证测试：空编码"
            },
            # 无效状态
            {
                "positionName": f"无效状态岗位_{timestamp}",
                "positionCode": f"POST_INVALID_STATUS_{timestamp}",
                "postSort": 1,
                "status": "2",  # 无效状态值
                "remark": "验证测试：无效状态"
            },
            # 负排序值
            {
                "positionName": f"负排序岗位_{timestamp}",
                "positionCode": f"POST_NEGATIVE_SORT_{timestamp}",
                "postSort": -1,  # 无效排序值
                "status": "0",
                "remark": "验证测试：负排序值"
            },
            # 超长备注
            {
                "positionName": f"超长备注岗位_{timestamp}",
                "positionCode": f"POST_LONG_REMARK_{timestamp}",
                "postSort": 1,
                "status": "0",
                "remark": "a" * 501  # 501个字符，超过500限制
            }
        ]
    
    @staticmethod
    def generate_batch_position_data(count=3, prefix="batch_position"):
        """生成批量岗位测试数据
        
        Args:
            count: 生成的数据数量
            prefix: 数据前缀
        
        Returns:
            list: 批量岗位数据列表
        """
        batch_data = []
        timestamp = int(time.time())
        
        for i in range(1, count + 1):
            position_data = PositionTestDataGenerator.generate_position_data(
                prefix=f"{prefix}_{i}",
                postSort=i,  # 使用不同的排序值
                remark=f"批量测试岗位_{i}_{timestamp}"
            )
            batch_data.append(position_data)
        
        return batch_data
    
    @staticmethod
    def generate_status_transition_data():
        """生成状态转换测试数据
        
        Returns:
            dict: 状态转换测试数据
        """
        timestamp = int(time.time())
        
        return {
            "initial": {
                "positionName": f"状态转换岗位_{timestamp}",
                "positionCode": f"POST_STATUS_TRANS_{timestamp}",
                "postSort": 1,
                "status": "0",  # 初始启用状态
                "remark": "状态转换测试：初始启用状态"
            },
            "disabled": {
                "status": "1",  # 停用状态
                "remark": "状态转换测试：已停用"
            },
            "enabled": {
                "status": "0",  # 重新启用
                "remark": "状态转换测试：重新启用"
            }
        }


def generate_unique_test_id(prefix="test"):
    """生成唯一的测试ID
    
    Args:
        prefix: ID前缀
    
    Returns:
        str: 唯一测试ID
    """
    timestamp = int(time.time() * 1000)  # 毫秒级时间戳
    random_suffix = random.randint(10000, 99999)
    return f"{prefix}_{timestamp}_{random_suffix}"


def get_test_position_template():
    """获取岗位测试数据模板
    
    Returns:
        dict: 岗位测试数据模板
    """
    return {
        "positionName": "岗位名称",
        "positionCode": "岗位编码",
        "postSort": 1,
        "status": "0",
        "remark": "备注信息"
    }


# 使用示例
if __name__ == "__main__":
    # 生成单个岗位数据
    position_data = PositionTestDataGenerator.generate_position_data()
    print("单个岗位数据:", position_data)
    
    # 生成边界值测试用例
    boundary_cases = PositionTestDataGenerator.generate_boundary_test_cases()
    print(f"边界值测试用例数量: {len(boundary_cases)}")
    
    # 生成验证测试用例
    validation_cases = PositionTestDataGenerator.generate_validation_test_cases()
    print(f"验证测试用例数量: {len(validation_cases)}")
    
    # 生成批量数据
    batch_data = PositionTestDataGenerator.generate_batch_position_data(3)
    print(f"批量数据数量: {len(batch_data)}")
    
    # 生成状态转换数据
    status_data = PositionTestDataGenerator.generate_status_transition_data()
    print("状态转换数据:", status_data.keys())
    
    # 生成唯一测试ID
    test_id = generate_unique_test_id("position_test")
    print("唯一测试ID:", test_id)