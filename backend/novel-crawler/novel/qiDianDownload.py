""""""
import requests
import parsel
from tqdm import tqdm

'''
    目标网址   ->    起点中文网（阅文网）：https://www.qidian.com/
    功能      ->    根据 书名 阅文网 下载小说
'''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36',
}


# 搜索书籍的地址
def search(name):
    search_url = f"https://www.qidian.com/search?kw={name}"
    response = requests.get(url=search_url, headers=headers)
    selector = parsel.Selector(response.text)
    lis = selector.css('.book-img-text li')
    for li in lis:
        book_name = li.css('.book-mid-info h4 a::text').get()
        if book_name:
            pass
        else:
            book_name = li.css('.book-mid-info h4 a cite::text').get()
        # 判断书名是否一致
        if book_name == name:
            book_author = li.css('.book-mid-info .author .name::text').get()
            global file_name
            file_name = f'{name} - {book_author}.txt'
            return li.css('.book-mid-info h4 a::attr(href)').get()


# 获取所有章节url
def get_catalog(url):
    catalog_url = "https:" + url + "#Catalog"
    response = requests.get(url=catalog_url, headers=headers)
    selector = parsel.Selector(response.text)
    volumes = selector.css('.volume-wrap .volume')
    chapter_list = []
    for volume in volumes:
        lis = volume.css('li')
        for li in lis:
            chapter = li.css('a::text').get()
            chapter_url = li.css('a::attr(href)').get()
            chapter_list.append([chapter, "https:" + chapter_url])
    return chapter_list


# 获取每章节内容并保存
def save_content(url):
    response = requests.get(url=url, headers=headers)
    selector = parsel.Selector(response.text)
    ps = selector.css('.text-wrap .main-text-wrap .read-content p')
    for p in ps:
        content = p.css('::text').get()
        file.write(content)
        file.write('\n')


def full_download(names):
    """
    批量全本下载
    :param names: 小说名称列表
    """
    for name in names:
        url = search(name)
        if url:
            print(f"{name} 开始下载")
            global file
            file = open(file_name, 'a', encoding='utf-8')
            chapter_list = get_catalog(url)
            for chapter in tqdm(chapter_list):
                file.write(chapter[0])
                file.write('\n')
                save_content(chapter[1])
            file.close()
        else:
            print(f"{name} 未找到")


def specify_download(name, chapter_start_index=0, chapter_end_index=0):
    """
    指定 书名 指定章节 下载
    :param name: 小说名称
    :param chapter_start_index: 开始章节
    :param chapter_end_index: 截至章节
    """
    url = search(name)
    if url:
        print(f"{name} 继续下载")
        global file
        file = open(file_name, 'a', encoding='utf-8')
        chapter_list = get_catalog(url)
        # 获取实际下载章节
        if chapter_start_index > 0:
            if chapter_end_index > 0:
                real_list = chapter_list[chapter_start_index - 1:chapter_end_index - 1]
            else:
                real_list = chapter_list[chapter_start_index - 1:]
        else:
            if chapter_end_index > 0:
                real_list = chapter_list[0:chapter_end_index - 1]
            else:
                real_list = chapter_list
        for chapter in tqdm(real_list):
            file.write(chapter[0])
            file.write('\n')
            save_content(chapter[1])
        file.close()
    else:
        print(f"{name} 未找到")


if __name__ == '__main__':
    # 批量全本下载
    names = ["汉柏"]
    full_download(names)

    # 指定章节下载
    # name = "这个猴子超强却过分谨慎"
    # chapter_start_index = 3
    # chapter_end_index = 5
    # specify_download(name, chapter_start_index, chapter_end_index)
