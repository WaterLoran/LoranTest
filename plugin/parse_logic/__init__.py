from func_timeout import func_set_timeout, FunctionTimedOut
from core.init import *
from common.ruoyi_logic import *
from inspect import isfunction


def get_all_function_obj(local_input: dict):
    """
    从本地变量中获取所有的函数对象

    """
    func_obj_dict = {}
    local_dict = local_input
    for key, value in local_dict.items():
        if isfunction(value):
            func_obj_dict.update({key: value})
    return func_obj_dict

def judge_logic_func_type(api_data_list):
    """
    判断logic函数的类型

    logic相关函数会有三种类型:
    1. 最普通的跟单个请求接口对应的logic
    2. 对单个普通logic进行包装的函数, 暂命名为'二次logic'
    3. 使用多个logic来组装层一个全新的操作的函数, 暂命名为'组合logic'会涉及到多个logic的上下文信息

    返回: simple_logic, secondary_logic, combined_logic,
    """
    if api_data_list is None:  # 表示只是对其他函数的一个函数的封装, 即为secondary_logic
        logic_type = "secondary_logic"
    elif "req_url" in api_data_list.keys():  # 普通logic
        logic_type = "simple_logic"
    else:
        logic_type = "combined_logic"
    return logic_type

def get_api_data_list(func_obj):
    @func_set_timeout(0.01)
    def get_data():
        api_data_list = func_obj()
        return api_data_list

    try:
        api_data_list = get_data()
    except:
        api_data_list = None
    return api_data_list


def parse_one_function(one_func_obj):
    """
    将入参的信息提取出来
    将函数体中的所有信息提取出来
    """
    one_func_info_dict = {}
    print("当前正在处理")

    # 初步判断函数是不是logic类型, 如果是的话, 则这个函数会带有__dict__
    in_func_obj = one_func_obj.__dict__
    if in_func_obj == {}:
        print(one_func_obj)
        return None

    while True:
        try:
            if "__wrapped__" in in_func_obj.keys():
                in_func_obj = in_func_obj["__wrapped__"]
        except:
            break
    func_obj = in_func_obj

    func_name = func_obj.__name__
    print("func_name", func_name)
    one_func_info_dict.update({"func_name": func_name})

    # 获取APi_data的信息
    api_data_list = get_api_data_list(func_obj)

    # 判断logic类型, 并更新信息
    logic_type = judge_logic_func_type(api_data_list)
    one_func_info_dict.update({"logic_type": logic_type})

    # 提取信息操作
    if api_data_list is not None:
        one_func_info_dict.update(api_data_list)

    # 处理一下输入的入参, 将输入的入参提取到其中的一个列表中,方便解析
    one_func_info_dict = extract_input_kwargs(one_func_info_dict)

    # 如果提取的信息中存在fill_req_body或者fill_req_params的话, 则对入参染色,再重新请求一次
    if "fill_req_body" in one_func_info_dict.keys() or "fill_req_params" in one_func_info_dict.keys():
        # 获取入参并染色, 即加上_ipt后缀
        new_input_kwargs_dict = {}
        input_kwargs_dict = one_func_info_dict["input_kwargs_dict"]
        for key, value in input_kwargs_dict.items():
            new_input_kwargs_dict.update({key: key+"_ipt"})

        new_api_data = func_obj(**new_input_kwargs_dict)
        # 将染色后的APi的请求信息, 更新到one_func_info_dict中
        one_func_info_dict.update({"req_url_ipt": new_api_data["req_url"]})  # req_url_ipt表示已填充入参的URL
        if "req_body" in new_api_data.keys():
            one_func_info_dict.update({"req_body": new_api_data["req_body"]})
        # 请求体的更新
        if "req_params" in new_api_data.keys():
            one_func_info_dict.update({"req_params": new_api_data["req_params"]})
        elif "req_params" in new_api_data.keys():
            one_func_info_dict.update({"req_params": new_api_data["req_params"]})
        elif "data" in new_api_data.keys():
            one_func_info_dict.update({"data": new_api_data["data"]})
    return one_func_info_dict

def extract_input_kwargs(one_func_info_dict):
    """
    所有不在non_input_variable_list列表中的信息都被认为是输入信息, 将会被提取到输入信息中
    """
    non_input_variable_list = ["func_name", "logic_type", "req_method", "req_url", "req_body", "req_params", "req_rsp",
                               "fill_req_body", "fill_req_params", "rsp_fetch", "kwargs", "rsp_check", "teardown"]

    input_kwargs_dict = {}
    delete_key_list = []
    for key, value in one_func_info_dict.items():
        if key not in non_input_variable_list:
            input_kwargs_dict.update({key: value})
            delete_key_list.append(key)

    # 将输入的参数更新到列表之后, 更新到one_func_info_dict
    one_func_info_dict.update({"input_kwargs_dict": input_kwargs_dict})

    # 循环删除这些key
    for key in delete_key_list:
        one_func_info_dict.pop(key)

    return one_func_info_dict


def parse_all_function(func_obj_dict: dict):
    func_info_list = []

    count = 0
    for key, value in func_obj_dict.items():
        try:
            # TODO 此处会过滤一次logic, 即无法调用的, 需要依赖于外部传参的, 这种可能需要去直接针对文字去解析了
            # TODO 里面的函数实际上也是有一次的过滤, 后续需要统一处理, 现在直接使用函数调用的方式来做基本开发
            one_func_info = parse_one_function(value)
            if one_func_info is not None:
                func_info_list.append(one_func_info)
        except:
            # TODO 这里需要打印出来
            print("ERROR当前函数处理出错, 待后续适配", key, value)
            pass
    return func_info_list

def serialize_to_json(func_info_list):
    cur_path = os.getcwd()
    json_file_path = os.path.join(cur_path, "logic_info.json")
    print("json_file_path", json_file_path)
    with open(json_file_path, "w") as open_file:
        json.dump(func_info_list, open_file, indent=4, ensure_ascii=False)
    pass


if __name__ == "__main__":

    # 从本地变量中提取出所有的函数对象
    func_obj_dict = get_all_function_obj(locals())

    # 对每个函数进行遍历, 参数获取出请求的相关信息
    func_info_list = parse_all_function(func_obj_dict)

    # 序列化到json文件中
    serialize_to_json(func_info_list)



