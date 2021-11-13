import os, re

pwd = os.path.split(os.path.realpath(__file__))[0]


def get_path(file_name):
    """
    相对于项目根目录的文件绝对地址
    :param file_name:
    :return:
    """
    return os.path.join(os.path.split(pwd)[0], file_name)


def read_file(file_name):
    lines = []
    with open(get_path(file_name), "r", encoding="UTF-8") as f:
        for line in f.readlines():
            if line.startswith("#") or "" == line.strip():
                continue
            lines.append([x.strip() for x in line.split(",")])
    return lines


# 匹配中文之间的空格
def remove_space(_str):
    """
    移除中文字符之间的空格，其他空格不处理
    @param _str:
    @return: 移除之后的字符串
    """
    if _str is None:
        return _str

    re_space = r"((?<=[\u4e00-\u9fa5])\s+(?=[\u4e00-\u9fa5]))"
    # 字符串直接移除
    if isinstance(_str, str):
        return re.sub(re_space, '', _str)

    # list 遍历所有移除
    result = list()
    if isinstance(_str, list):
        for item in _str:
            result.append(re.sub(re_space, '', item))
    return result
