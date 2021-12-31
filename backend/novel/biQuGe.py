""""""
import requests
import parsel

'''
    目标网址   ->    笔趣阁 ：https://www.biqugee.com/
    功能      ->    根据 书名 下载小说
'''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36',
}


class BiQuGe:
    # 搜索并打印书籍的信息
    def search(self, name):
        search_url = f"https://www.biqugee.com/search.php?q={name}"
        response = requests.get(url=search_url, headers=headers)
        selector = parsel.Selector(response.text)
        items = selector.css('.result-list .result-game-item')

        search_results = []
        for item in items:
            search_result = {}
            pic_url = item.css('.result-game-item-pic .result-game-item-pic-link-img').css('::attr(src)').get()
            book_title = item.css('.result-game-item-detail .result-game-item-title a')
            book_name = book_title.css('span::text').get()
            book_url = 'https://www.biqugee.com' + book_title.css('::attr(href)').get()
            book_description = item.css('.result-game-item-detail .result-game-item-desc::text').get()
            book_author = item.css('.result-game-item-info p:nth-of-type(1) span:nth-of-type(2)::text').get()
            book_type = item.css('.result-game-item-info p:nth-of-type(2) span:nth-of-type(2)::text').get().replace(
                "小说", "")
            book_update_time = item.css('.result-game-item-info p:nth-of-type(3) span:nth-of-type(2)::text').get()
            book_new_chapter = item.css(
                '.result-game-item-info p:nth-of-type(4) .result-game-item-info-tag-item::text').get()

            search_result['picUrl'] = pic_url
            search_result['name'] = book_name
            search_result['author'] = book_author
            search_result['type'] = book_type
            search_result['newChapter'] = book_new_chapter
            search_result['updateTime'] = book_update_time
            search_result['url'] = book_url
            search_result['description'] = book_description
            search_results.append(search_result)
        return search_results

    # 获取所有章节url
    def catalog(self, url):
        response = requests.get(url=url, headers=headers)
        selector = parsel.Selector(response.text)
        book_info = selector.css('#info')
        book_name = book_info.css('h1::text').get()
        chapter_list = []
        if book_name:
            dds = selector.css('#list dd')
            index = 0
            for dd in dds:
                chapter = {}
                index = index + 1
                chapter_name = dd.css('a::text').get()
                chapter_url = 'https://www.biqugee.com/' + dd.css('a::attr(href)').get()
                chapter['index'] = index
                chapter['name'] = chapter_name
                chapter['url'] = chapter_url
                chapter_list.append(chapter)
        return chapter_list

    # 获取每章节内容
    def get_chapter_detail(self, chapter):
        response = requests.get(url=chapter['url'], headers=headers)
        selector = parsel.Selector(response.text)
        contents = selector.css('#content::text').getall()
        detail = chapter['name'] + '\n'
        for content in contents:
            content = content.replace('\xa0\xa0\xa0\xa0', '   ')
            detail = detail + content + '\n'
        detail = detail + '\n\n\n'
        return detail
