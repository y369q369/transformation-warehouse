import os


def remove_novel(filepath):
    #     """
    #     移除小说
    #     :param filepath: 待下载的文件路径
    #     """
    if os.path.exists(filepath):
        os.remove(filepath)