""""""
import math
import threading
import time

import parsel
import requests
import urllib3
from fake_useragent import UserAgent

from script.utils.novel_util import split_process_download, save_file

'''
    目标网址   ->    顶点小说网 ：https://www.23wx.cc/
    功能      ->    根据 地址 下载小说
    备用：            https://www.23usp.com/
                     https://www.dingdianorg.com/
'''

headers = {'User-Agent': UserAgent().random}

video_download_path = "E:/ebook/novel/special2/"

encodings = 'gbk'


# 获取所有章节url
def catalog_list(url):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(url=url, headers=headers, verify=False)
    response.encoding = encodings
    selector = parsel.Selector(response.text)
    info_title = selector.css('#info h1::text').get()
    author = selector.css('#info p::text').get().replace('作    者：', '')
    chapter_list = []

    detail_list = selector.css('#list dd')
    for detail in detail_list:
        chapter_name = detail.css('a::text').get()
        if chapter_name is not None:
            chapter_url = url + detail.css('a::attr(href)').get()
            chapter_list.append({
                'name': chapter_name,
                'url': chapter_url
            })

    novel = {
        'title': info_title + ' - ' + author,
        'chapter_list': chapter_list
    }
    return novel


def download_one(url):
    st = time.time()
    info = catalog_list(url)

    content_list = split_process_download(5, info['chapter_list'][:20], encodings)

    # 整理内容
    novel_detail_list = []
    for chapter in content_list:
        selector = parsel.Selector(chapter['text'])

        detail = chapter['name'].replace('‘', '').replace('’', '') + '\n\n'
        context_list = selector.css('#content::text').getall()
        for content in context_list:
            if content != '\r\n':
                detail += '    ' + content.lstrip().replace('\r\n', '') + '\n\n'
        detail += '\n\n'
        novel_detail_list.append(detail)

    save_file(video_download_path, info['title'], novel_detail_list)

    et = time.time()
    print("\033[35;48m \n{} 下载完成， 总耗时： {} s \033[0m".format(info['title'], math.ceil(et - st)))


if __name__ == '__main__':
    url = 'https://www.23dd.cc/du/0/21/'
    download_one(url)
