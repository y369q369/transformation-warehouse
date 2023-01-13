""""""
import math
import threading
import time
import traceback

import parsel
import requests

'''
    目标网址   ->    笔趣阁 ：http://www.ibiqu.org/
    功能      ->    根据 地址 下载小说
    备用      ->     www.biqg99.com
                    www.biqugse.com
                    www.slyqw.com
'''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36',
}

video_download_path = "E:/ebook/"

threadNum = 5


class ChapterContent(threading.Thread):
    """
        获取小说章节内容 线程
    """

    def __init__(self, chapter_list, content_list):
        threading.Thread.__init__(self)
        self.chapter_list = chapter_list
        self.content_list = content_list

    def run(self):
        for chapter in self.chapter_list:
            print("{} 开始获取".format(chapter['name']))
            try:
                res = requests.get(chapter['url'])
                # 解决中文符号乱码问题
                res.encoding = 'gbk'
                self.content_list.append({
                    'name': chapter['name'],
                    'text': res.text
                })
            except:
                print("\033[31;48m {}   {} 章节获取异常 \033[0m".format(chapter['name'], chapter['url']))
                # traceback.print_exc()
                res = requests.get(chapter['url'], timeout=20)
                self.content_list.append(res.text)


# 获取所有章节url
def catalog_list(url):
    response = requests.get(url=url, headers=headers)
    selector = parsel.Selector(response.text)

    info_title = selector.css('#info h1::text').get()
    author = selector.css('#info p:nth-child(2) ::text').get().replace('作　　者：', '')
    chapter_list = []

    detail_list = selector.css('#list dl dd')[9:]
    for detail in detail_list:
        chapter_name = detail.css('a::text').get()
        if chapter_name is not None:
            chapter_url = 'http://www.ibiqu.org' + detail.css('a::attr(href)').get()
            chapter_list.append({
                'name': chapter_name,
                'url': chapter_url
            })

    novel = {
        'title': info_title + ' - ' + author,
        'chapter_list': chapter_list
    }
    return novel


# 获取每章节内容
def download(info):
    st = time.time()
    chapter_list = info['chapter_list']
    # chapter_list = info['chapter_list'][0:40]

    # 拆分线程获取小说内容
    piece_size = len(chapter_list) // threadNum
    threads = []
    content_list = []

    for i in range(threadNum):
        if i == threadNum - 1:
            temp_chapter_list = chapter_list[i * piece_size:]
        else:
            temp_chapter_list = chapter_list[i * piece_size:(i + 1) * piece_size]
        temp_content_list = []
        content_list.append(temp_content_list)
        thread = ChapterContent(temp_chapter_list, temp_content_list)
        threads.append(thread)
        thread.start()
    # 等待所有线程完成
    for t in threads:
        t.join()

    # 保存文件
    file = video_download_path + info['title'] + '.txt'
    with open(file, 'w', encoding='utf-8') as novel:
        book_info = "{} \n\n\n\n".format(info['title'])
        novel.write(book_info)
        novel.close()

    # 所有内容输出到文件中
    for thread_content_list in content_list:
        for chapter_content in thread_content_list:
            selector = parsel.Selector(chapter_content['text'])

            detail = chapter_content['name'].replace('‘', '').replace('’', '') + '\n\n'
            context_list = selector.css('#content p::text').getall()
            for content in context_list:
                detail += content + '\n\n'

            detail += '\n\n'

            with open(file, 'a', encoding='utf-8') as novel:
                novel.write(detail)
                novel.close()
    et = time.time()
    print("\033[35;48m \n{} 下载完成， 总耗时： {} s \033[0m".format(info['title'], math.ceil(et - st)))


if __name__ == '__main__':
    url = 'http://www.ibiqu.org/book/2247/'
    info = catalog_list(url)
    download(info)
