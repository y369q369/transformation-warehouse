""""""
import requests
import parsel

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
        search_url = f"https://www.qidian.com/soushu/{name}.html"
        response = requests.get(url=search_url, headers=headers)
        selector = parsel.Selector(response.text)
        lis = selector.css('.book-img-text li')

        search_results = []
        for li in lis:
            search_result = {}
            pic_url = "https:" + li.css('.book-img-box img::attr(src)').get()
            book_name_html = li.css('.book-mid-info .book-info-title a').get()
            book_name_html = book_name_html.replace('<cite class="red-kw">', "").replace('</cite>', "")
            book_name = book_name_html[book_name_html.find(">") + 1:book_name_html.find("<", 2)]
            book_url = "https:" + li.css('.book-mid-info .book-info-title a::attr(href)').get()
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

    # 获取所有章节url
    def catalog(self, url):
        response = requests.get(url=url + "#Catalog", headers=headers)
        selector = parsel.Selector(response.text)
        volumes = selector.css('.volume-wrap .volume')
        chapter_list = []
        index = 0
        for volume in volumes:
            lis = volume.css('li')
            for li in lis:
                chapter = {}
                index = index + 1
                chapter_name = li.css('a::text').get()
                chapter_url = "https:" + li.css('a::attr(href)').get()
                chapter['index'] = index
                chapter['name'] = chapter_name
                chapter['url'] = chapter_url
                chapter_list.append(chapter)
        return chapter_list

    # 获取每章节内容
    def get_chapter_detail(self, chapter):
        response = requests.get(url=chapter['url'], headers=headers)
        selector = parsel.Selector(response.text)
        ps = selector.css('.text-wrap .main-text-wrap .read-content p')
        detail = chapter['name'] + '\n'
        for p in ps:
            content = p.css('::text').get()
            detail = detail + content + '\n'
        detail = detail + '\n\n\n'
        return detail