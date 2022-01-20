import threading
from backend.utils.CommonUtil import remove_file


class saveChapterThread(threading.Thread):
    #     """
    #     线程对象，下载部分章节到指定文件
    #     :param chapter_list: 部分章节链接地址
    #     :param filename: 目标文件（路径+文件名称）
    #     :param get_chapter_detail: 根据章节链接获取章节内容的方法
    #     """
    def __init__(self, chapter_list, filename, get_chapter_detail):
        threading.Thread.__init__(self)
        self.chapter_list = chapter_list
        self.filename = filename
        self.get_chapter_detail = get_chapter_detail

    def run(self):
        remove_file(self.filename)
        file = open(self.filename, 'a', encoding='utf-8')
        for chapter in self.chapter_list:
            # for chapter in tqdm(self.chapter_list):
            detail = self.get_chapter_detail(chapter)
            file.write(detail)
        file.close()
        print(self.filename + " 下载完成")