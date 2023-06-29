""""""
import math
import time

import parsel
import requests
import urllib3
from fake_useragent import UserAgent

from script.utils.novel_util import split_process_download, save_file

'''
    目标网址   ->    插久网 ：https://x9wang.com/index.html
    功能      ->    根据 地址 下载小说
'''

headers = {'User-Agent': UserAgent().random}

video_download_path = "E:/ebook/novel/special2/"


# 获取章节信息
def get_chapter_info(url):
    # 处理https请求认证
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(url=url, headers=headers, verify=False)
    selector = parsel.Selector(response.text)

    title = selector.css('.works-intro-title strong::text').get().strip()
    author = selector.css('.works-intro-digi .first em::text').get().strip()

    catalog = []

    chapter_list = selector.css('.chapter-page-new p')
    for chapter_info in chapter_list:
        url = chapter_info.css('a::attr(href)').get()
        name = chapter_info.css('a::attr(title)').get()
        catalog.insert(0, {
            'name': name,
            'url': 'https://x9wang.com' + url
        })
    return {
        'title': title + ' - ' + author,
        'chapter_list': catalog
    }


# 下载单本小说
def download_one(url):
    st = time.time()
    info = get_chapter_info(url)
    content_list = split_process_download(5, info['chapter_list'], 'utf-8')

    # 整理内容
    novel_detail_list = []
    for chapter in content_list:
        selector = parsel.Selector(chapter['text'])
        detail = chapter['name'].replace('‘', '').replace('’', '') + '\n\n'
        context_list = selector.css('.read-content .content-wrap::text').getall()
        for content in context_list:
            detail += '    ' + content + '\n\n'
        detail += '\n\n'
        novel_detail_list.append(detail)

    save_file(video_download_path, info['title'], novel_detail_list)

    et = time.time()
    print("\033[35;48m \n{} 下载完成， 总耗时： {} s \033[0m".format(info['title'], math.ceil(et - st)))


if __name__ == '__main__':
    download_one('https://x9wang.com/3/20589/info.html')
