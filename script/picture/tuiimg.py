import os
import re
import threading

from tqdm import tqdm
import parsel
import requests

'''
    目标网址   ->    推图网 ：https://www.tuiimg.com/meinv/
    功能      ->    爬美女图片
'''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36',
}

picture_download_path = "E:/picture/Spider/推图网/"
threadNum = 3


def download_one(url):
    html = requests.get(url, headers).content
    picture_name = url.split('/')[len(url.split('/')) - 1]
    picture = picture_download_path + picture_name
    # 进行图片保存
    with open(picture, 'wb') as f:
        f.write(html)


# 美女单个专题，所有图片下载
def download_beauty_list(picture_info):
    # 判断有没有这个保存图片的路径  没有则创建
    directory = picture_download_path + picture_info['catalog'] + '/'
    print('\n' + directory + '      开始下载（' + str(len(picture_info['picture_list'])) + '）')
    if not os.path.exists(directory):
        os.mkdir(directory)
    for picture_name in picture_info['picture_list']:
        picture_file = directory + picture_name
        picture_url = picture_info['url_prefix'] + picture_name
        html = requests.get(picture_url, headers)
        print('       ' + picture_info['catalog'] + '  ~  ' + picture_name + '  ->  ' + str(html.status_code))
        # 进行图片保存
        with open(picture_file, 'wb') as f:
            f.write(html.content)
            f.close()


# 获取美女某个专题的所有图片地址
def get_beauty_picture_list(url):
    response = requests.get(url, headers)
    selector = parsel.Selector(response.text)
    # 专题标题
    directory_name = selector.css('#main h1::text').get()
    # 专题第一张图片地址
    picture_url = selector.css('#content #nowimg::attr(src)').get()
    # 专题图片地址前缀
    picture_url_prefix = picture_url[:picture_url.rindex('/') + 1]
    picture_name = picture_url[picture_url.rindex('/') + 1:]
    # 专题图片格式
    picture_name_suffix = picture_name[picture_name.rindex('.'):]
    picture_num_info = selector.css('#allbtn::text').get()
    picture_num = re.findall("展开全图\(1/(.*?)\)", picture_num_info)[0]
    # 专题图片数量
    picture_num = int(picture_num)
    picture_list = []
    for num in range(1, picture_num + 1):
        picture_list.append(str(num) + picture_name_suffix)
    return {
        'catalog': directory_name,
        'url_prefix': picture_url_prefix,
        'picture_list': picture_list
    }


# 下载美女单个专题所有图片
def download_beauty_topic_one(url):
    picture_info = get_beauty_picture_list(url)
    download_beauty_list(picture_info)


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
                picture_info = get_beauty_picture_list(url)
                download_beauty_list(picture_info)
            except:
                print("\033[31;48m {} 获取异常 \033[0m".format(url))
                # traceback.print_exc()
                picture_info = get_beauty_picture_list(url)
                download_beauty_list(picture_info)


# 下载美女所有专题所有图片
def download_beauty_topic_list(start, end):
    beauty_url = 'https://www.tuiimg.com/meinv/'
    urls = []
    for i in range(start, end + 1):
        page_url = beauty_url + 'list_' + str(i) + '.html'
        response = requests.get(page_url, headers)
        selector = parsel.Selector(response.text)
        li = selector.css('.beauty ul li')
        print(f'美女专题第 {str(i)} 页 {len(li)} 个专题地址获取完成')
        for item in li:
            url = item.css('.title::attr(href)').get()
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
    # download_one('https://i.tuiimg.net/006/2767/2.jpg')
    # 美女单个专题
    # download_beauty_topic_one('https://www.tuiimg.com/meinv/2763/')
    # 美女指定页所有专题 （共 139 页， 第一条：  甜美妹纸余美欣能令无数宅男折腰）
    download_beauty_topic_list(51, 139)
