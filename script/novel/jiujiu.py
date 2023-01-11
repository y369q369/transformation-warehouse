""""""
import math
import threading
import time
import traceback

import parsel
import requests

'''
    目标网址   ->    九九小说网 ：https://www.9haokan.com/
    功能      ->    根据 地址 下载小说
'''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36',
}

video_download_path = "E:/ebook/"

threadNum = 3


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

    info_title = selector.css('.infotitle h1::text').get()
    author = selector.css('#infobox .username a::text').get()
    detail_list = selector.css('#detaillist')
    chapter_list = []

    # 前部分章节
    top_list = detail_list.css('#toplist li')
    for top in top_list:
        chapter_name = top.css('a::text').get()
        chapter_url = 'https://www.9haokan.com' + top.css('a::attr(href)').get()
        chapter_list.append({
            'name': chapter_name,
            'url': chapter_url
        })

    # 中间隐藏部分章节
    yc = detail_list.css('#yc')
    if yc is not None:
        hide_chapter_info = yc.css('::attr(onclick)').get()
        hide_chapter_info_list = hide_chapter_info.replace('loadzj(', '').replace(');', '').replace('\'', '', 2).split(
            ',')
        hide_chapter_url = 'https://www.9haokan.com/novelsearch/novel/getdlist/?id={}&num={}&order={}' \
            .format(hide_chapter_info_list[0], hide_chapter_info_list[1], hide_chapter_info_list[2])
        response2 = requests.get(url=hide_chapter_url, headers=headers)
        selector2 = parsel.Selector(response2.text)
        hide_chapter_li = selector2.css('li')
        for info in hide_chapter_li:
            chapter_name = info.css('a::text').get()
            chapter_url = 'https://www.9haokan.com' + info.css('a::attr(href)').get()
            chapter_list.append({
                'name': chapter_name,
                'url': chapter_url
            })

    # 后部分章节
    last_list = detail_list.css('#lastchapter li')
    for last in last_list:
        chapter_name = last.css('a::text').get()
        chapter_url = 'https://www.9haokan.com' + last.css('a::attr(href)').get()
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
    # chapter_list = chapter_list[0:10]

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

            detail = chapter_content['name'] + '\n\n'
            context_list = selector.css('#chaptercontent::text').getall()
            for content in context_list:
                # 去除标题重复内容
                if content.find(chapter_content['name']) == -1:
                    detail += content.replace('   \u3000', '').replace('\u3000', '') + '\n\n'

            # 去除广告内容
            filter_str = chapter_content['name'] + '( 情迷女人香（草根成长记）  9haokan/4/4417/ 移动版阅读m.9haokan )'
            detail = detail.replace(filter_str, '')
            filter_str2 = 'wＡp．．cn'
            detail = detail.replace(filter_str2, '')

            detail += '\n\n'

            with open(file, 'a', encoding='utf-8') as novel:
                novel.write(detail)
                novel.close()
    et = time.time()
    print("\033[35;48m \n{} 下载完成， 总耗时： {} s \033[0m".format(info['title'], math.ceil(et - st)))


if __name__ == '__main__':
    url = 'https://www.9haokan.com/novel/48223/#comment'
    info = catalog_list(url)
    download(info)
