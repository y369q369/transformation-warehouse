import os
import re
import datetime
import threading

import parsel
import requests

'''
    目标网址   ->    爱美女 ：https://www.2meinv.com/
    功能      ->    爬美女图片
'''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36',
}

picture_download_path = "E:/picture/Spider/爱美女/"
threadNum = 3


# 获取单个专题
def get_topic_info(url):
    response = requests.get(url, headers)
    selector = parsel.Selector(response.text)
    directory_name = selector.css('.des h1::text').get()
    img_url = selector.css('.pp a img::attr(src)').get()
    date_str = re.findall("attach/(.*?)/", img_url)[0]
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    urls = []
    # 2020 之后的图片都没了
    if date > datetime.date(2019, 12, 31):
        urls.append(img_url)
        pages_info = selector.css('.des h1 span::text').get()
        pages = re.findall("/ (.*?)\)", pages_info)[0]
        for i in range(2, int(pages) + 1):
            cur_url = url.replace('.html', f'-{str(i)}.html')
            cur_response = requests.get(cur_url, headers)
            cur_selector = parsel.Selector(cur_response.text)
            cur_img_url = cur_selector.css('.pp a img::attr(src)').get()
            urls.append(cur_img_url)
    return {
        'catalog': directory_name,
        'urls': urls
    }


# 美女单个专题，所有图片下载
def download_picture_list(picture_info):
    # 判断有没有这个保存图片的路径  没有则创建
    directory = picture_download_path + picture_info['catalog'] + '/'
    print('\n' + directory + '      开始下载（' + str(len(picture_info['urls'])) + '）')
    if not os.path.exists(directory):
        os.mkdir(directory)
    for url in picture_info['urls']:
        picture_file = directory + url[url.rindex('/') + 1:]
        html = requests.get(url, headers)
        print('       ' + picture_info['catalog'] + '  ~  ' + url[url.rindex('/') + 1:] + '  ->  ' + str(
            html.status_code))
        if html.status_code == 200:
            # 进行图片保存
            with open(picture_file, 'wb') as f:
                f.write(html.content)
                f.close()


# 下载单个专题
def download_topic_one(url):
    topic_info = get_topic_info(url)
    # print(topic_info)
    if len(topic_info['urls']) > 0:
        download_picture_list(topic_info)
    else:
        print(topic_info['catalog'] + '    图片不存在')


class TopicDownload(threading.Thread):
    """
        下载图集 线程
    """

    def __init__(self, url_list):
        threading.Thread.__init__(self)
        self.url_list = url_list

    def run(self):
        for url in self.url_list:
            try:
                download_topic_one(url)
            except:
                print("\033[31;48m {} 获取异常 \033[0m".format(url))
                # traceback.print_exc()
                download_topic_one(url)


# 下载所有专题
def download_topic_all(start, end):
    urls = []
    for page in range(start, end + 1):
        response = requests.get(f'https://www.2meinv.com/index-{str(page)}.html', headers)
        selector = parsel.Selector(response.text)
        li = selector.css('.detail-list li')
        for topic in li:
            url = topic.css('a::attr(href)').get()
            urls.append(url)
    if len(urls) > 0:
        # 拆分线程获取小说内容
        piece_size = len(urls) // threadNum
        for i in range(threadNum):
            if i == threadNum - 1:
                url_list = urls[i * piece_size:]
            else:
                url_list = urls[i * piece_size:(i + 1) * piece_size]
            thread = TopicDownload(url_list)
            thread.start()


if __name__ == '__main__':
    # 美女单个专题
    # download_topic_one('https://www.2meinv.com/article-5927.html')
    # 美女所有专题 (当前已下载： 2023-02-03)  1 - 3   221
    download_topic_all(201, 221)
