import os
import yaml

class YamlTool:
    """ 获取 yaml 文件中的数据 """

    def __init__(self, file_abs_path=""):
        self.file_abs_path = file_abs_path

    def read_yaml_data(self) -> dict:
        """
        获取 yaml 中的数据
        :param: fileDir:
        :return:
        """
        # 判断文件是否存在
        if os.path.exists(self.file_abs_path):
            data = open(self.file_abs_path, 'r', encoding='utf-8')
            res = yaml.load(data, Loader=yaml.FullLoader)
        else:
            raise FileNotFoundError("文件路径不存在")
        return res

    def update_yaml_data(self, key: str, value) -> int:
        """
        更改 yaml 文件中的值, 并且保留注释内容
        :param key: 字典的key
        :param value: 写入的值
        :return:
        """
        with open(self.file_abs_path, 'r', encoding='utf-8') as file:
            # 创建了一个空列表，里面没有元素
            lines = []
            for line in file.readlines():
                if line != '\n':
                    lines.append(line)
            file.close()

        with open(self.file_abs_path, 'w', encoding='utf-8') as file:
            flag = 0
            for line in lines:
                left_str = line.split(":")[0]
                if key == left_str and '#' not in line:
                    newline = f"{left_str}: {value}"
                    line = newline
                    file.write(f'{line}\n')
                    flag = 1
                else:
                    file.write(f'{line}')
            file.close()
            return flag

    def write_dict_to_yaml(self, file_abspath, dict_content):
        with open(file_abspath, 'w', encoding='utf-8') as open_file:
            yaml.dump(data=dict_content, stream=open_file, allow_unicode=True)
        open_file.close()

