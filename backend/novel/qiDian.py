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


class QiDian:
    # 搜索书籍
    def search(self, name):
        search_url = f"https://www.qidian.com/search?kw={name}"
        response = requests.get(url=search_url, headers=headers)
        selector = parsel.Selector(response.text)
        lis = selector.css('.book-img-text li')

        search_results = []
        for li in lis:
            search_result = {}
            pic_url = "https:" + li.css('.book-img-box img::attr(src)').get()
            book_name_html = li.css('.book-mid-info h4 a').get()
            book_name_html = book_name_html.replace('<cite class="red-kw">', "").replace('</cite>', "")
            book_name = book_name_html[book_name_html.find(">") + 1:book_name_html.find("<", 2)]
            book_url = "https:" + li.css('.book-mid-info h4 a::attr(href)').get()
            book_description = li.css('.book-mid-info .intro::text').get()
            book_author = li.css('.book-mid-info .author a:nth-of-type(1)::text').get()
            book_type = li.css('.book-mid-info .author a:nth-of-type(2)::text').get()
            book_status = li.css('.book-mid-info .author span::text').get()
            book_update_time = li.css('.book-mid-info .update span::text').get()
            book_new_chapter = li.css('.book-mid-info .update a::text').get()

            search_result['picUrl'] = pic_url
            search_result['name'] = book_name
            search_result['author'] = book_author
            search_result['type'] = book_type
            search_result['newChapter'] = book_new_chapter
            search_result['updateTime'] = book_update_time
            search_result['status'] = book_status
            search_result['url'] = book_url
            search_result['description'] = book_description
            search_results.append(search_result)
        return search_results
