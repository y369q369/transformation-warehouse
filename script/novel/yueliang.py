""""""
import re

import parsel
import requests

'''
    目标网址   ->    月亮小说 ：https://yueliangwz42.buzz/
    功能      ->    根据 地址 下载小说
'''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36',
}

video_download_path = "E:/ebook/novel/special/"


# 下载单本小说
def download_one(url):
    response = requests.get(url=url, headers=headers)
    selector = parsel.Selector(response.text)

    title = selector.css('.post-title::text').get().strip()

    content_all_str = selector.css('.post-content-content').getall()[0]
    content_all_str2 = content_all_str[content_all_str.find('<h3>'):]
    content_all_str3 = content_all_str2[:content_all_str2.rfind('</p>') + 4]
    content_all_str4 = content_all_str3.replace('\U0008f335', '一').replace('\U0008f333', '，').replace('\U0008f332',
                                                                                                      '。').replace(
        '\U0008f330', '”').replace('\U0008f331', '“').replace('\U0008f334', '：')
    content_all_str5 = content_all_str4.replace('<p>', '    ').replace('</p>', '\n')

    regex = re.compile(r'<h3><span id="lwptoc\d+">')
    content_all_str6 = regex.sub('\n', content_all_str5).replace('</span></h3>', '\n\n')

    # 保存文件
    file = video_download_path + title + '.txt'
    with open(file, 'w', encoding='utf-8') as novel:
        novel.write(content_all_str6)
        novel.close()
    print("{}   下载完成".format(title))


# 下载一系列小说
def download_many(url):
    response = requests.get(url=url, headers=headers)
    selector = parsel.Selector(response.text)

    title_list = selector.css('.post-content-content ul li')
    for title in title_list:
        title_url = 'https://yueliangwz42.buzz/' + title.css('a::attr(href)').get()
        download_one(title_url)


if __name__ == '__main__':
    # download_one('https://yueliangwz42.buzz/42669.html')
    download_many('https://yueliangwz42.buzz/41149.html')
