""""""
import math
import re
import time

import parsel
import requests
import urllib3
from fake_useragent import UserAgent

from script.utils.novel_util import split_process_download, save_file

'''
    目标网址   ->    飘天文学 ：https://www.ptwxz.com/
    功能      ->    根据 地址 下载小说
'''

headers = {'User-Agent': UserAgent().random}

video_download_path = "E:/ebook/novel/special2/"

encodings = 'gbk'


# 获取章节信息
def get_chapter_info(url):
    # 获取 书名、作者、章节列表
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(url=url, headers=headers, verify=False)
    response.encoding = encodings
    selector = parsel.Selector(response.text)
    title = selector.css('h1 ::text').get()
    author_str = selector.css('#content table table:nth-of-type(1) tr:nth-of-type(2) td:nth-of-type(2) ::text').get()
    author = author_str.replace('作    者：', '')
    temp_chapter_url = selector.css('caption  a::attr(href)').get().replace('index.html', '')
    if temp_chapter_url.startswith('http'):
        all_chapter_url = temp_chapter_url
    else:
        url_prefix = url[:url.index('/', 10)]
        all_chapter_url = url_prefix + temp_chapter_url

    # 获取所有章节
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response2 = requests.get(url=all_chapter_url, headers=headers, verify=False)
    response2.encoding = 'gbk'
    selector2 = parsel.Selector(response2.text)

    catalog = []
    ul_list = selector2.css('.centent ul')
    for ul in ul_list:
        li_list = ul.css('li')
        for chapter in li_list:
            chapter_url = chapter.css('a::attr(href)').get()
            if chapter_url is not None:
                name = chapter.css('a::text').get()
                catalog.append({
                    'name': name,
                    'url': all_chapter_url + chapter_url
                })
    return {
        'title': title + ' - ' + author,
        'chapter_list': catalog
    }


# 下载单本小说
def download_one(url):
    st = time.time()
    info = get_chapter_info(url)
    content_list = split_process_download(5, info['chapter_list'], encodings)

    # 整理内容
    novel_detail_list = []
    for chapter in content_list:
        # 非严格html格式，用正则匹配出来
        context_list = re.findall('&nbsp;&nbsp;&nbsp;&nbsp;(.*?)<br />[\\r][\\n]<br />', chapter['text'])
        print(chapter['text'])
        detail = chapter['name'].replace('‘', '').replace('’', '') + '\n\n'
        for index, content in enumerate(context_list):
            if index > 0 or content == info['title']:
                detail += '    ' + content + '\n\n'
        detail += '\n\n'
        novel_detail_list.append(detail)

    save_file(video_download_path, info['title'], novel_detail_list)

    et = time.time()
    print("\033[35;48m \n{} 下载完成， 总耗时： {} s \033[0m".format(info['title'], math.ceil(et - st)))


if __name__ == '__main__':
    # 挂VPN
    download_one('https://www.ptwxz.com/bookinfo/7/7230.html')
