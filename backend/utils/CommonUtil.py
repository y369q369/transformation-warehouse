import os
import re


def remove_file(filepath):
    #     """
    #     删除文件
    #     :param filepath: 待下删除的文件路径
    #     """
    if os.path.exists(filepath):
        os.remove(filepath)


def create_direction(direction):
    #     """
    #     创建文件夹（可递归创建）
    #     :param filepath: 待创建的文件夹路径
    #     """
    if not os.path.exists(direction):
        os.makedirs(direction)


def get_root_path():
    #     """
    #     获取项目根目录
    #     """
    # 获取当前目录
    # current_path = os.path.dirname(os.path.abspath(__file__))
    # 获取上一级目录
    return os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


def check_url(url):
    #     """
    #     校验 url 格式
    #     """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return regex.match(url)