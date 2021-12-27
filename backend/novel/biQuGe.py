""""""
import requests
import parsel
from tqdm import tqdm

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
        print('搜索结果：')
        for item in items:
            search_result = {}
            book_title = item.css('.result-game-item-detail .result-game-item-title a')
            book_name = book_title.css('span::text').get()
            book_url = 'https://www.biqugee.com/' + book_title.css('::attr(href)').get()
            book_description = item.css('.result-game-item-detail .result-game-item-desc::text').get()
            book_author = item.css('.result-game-item-info p:nth-of-type(1) span:nth-of-type(2)::text').get()
            search_result['bookName'] = book_name
            search_result['bookAuthor'] = book_author
            search_result['bookUrl'] = book_url
            search_result['bookDescription'] = book_description
            search_results.append(search_result)


            print(f'    书名 \033[0;30;43m {book_name} \033[0m')
            print(f'    作者 {book_author}')
            print(f'    地址 {book_url:30}   ')
            print(f'    简介 {book_description} \n\n')
        return search_results


    # # 获取所有章节url
    # def get_catalog(url):
    #     response = requests.get(url=url, headers=headers)
    #     selector = parsel.Selector(response.text)
    #     book_info = selector.css('#info')
    #     book_name = book_info.css('h1::text').get()
    #     chapter_list = []
    #     if book_name:
    #         book_author = book_info.css('p::text').get().replace('作    者：', '')
    #         file_name = book_name + ' - ' + book_author + '.txt'
    #         global file
    #         file = open(file_name, 'a', encoding='utf-8')
    #         print(f"\n  {book_name} 开始下载")
    #         dds = selector.css('#list dd')
    #         for dd in dds:
    #             chapter_name = dd.css('a::text').get()
    #             chapter_url = 'https://www.biqugee.com/' + dd.css('a::attr(href)').get()
    #             chapter_list.append([chapter_name, chapter_url])
    #     else:
    #         print(f"{url} 异常，找不到书籍")
    #     return chapter_list
    #
    #
    # # 获取每章节内容并保存
    # def save_content(url):
    #     response = requests.get(url=url, headers=headers)
    #     selector = parsel.Selector(response.text)
    #     contents = selector.css('#content::text').getall()
    #     for content in contents:
    #         content = content.replace('\xa0\xa0\xa0\xa0', '   ')
    #         file.write(content)
    #         file.write('\n')
    #
    #
    # def full_download(urls=[]):
    #     """
    #     批量全本下载
    #     :param urls: 书籍链接 集合
    #     """
    #     for url in urls:
    #         chapter_list = get_catalog(url)
    #         if len(chapter_list) > 0:
    #             for chapter in tqdm(chapter_list):
    #                 file.write(chapter[0])
    #                 file.write('\n')
    #                 save_content(chapter[1])
    #                 file.write('\n\n\n')
    #             file.close()
    #
    #
    # def specify_download(url, chapter_start_index=0, chapter_end_index=0):
    #     """
    #     指定 链接 下载
    #     :param url: 链接地址
    #     :param chapter_start_index: 开始章节
    #     :param chapter_end_index: 截至章节
    #     """
    #     chapter_list = get_catalog(url)
    #     if len(chapter_list) > 0:
    #         # 获取实际下载章节
    #         if chapter_start_index > 0:
    #             if chapter_end_index > 0:
    #                 real_list = chapter_list[chapter_start_index - 1:chapter_end_index - 1]
    #             else:
    #                 real_list = chapter_list[chapter_start_index - 1:]
    #         else:
    #             if chapter_end_index > 0:
    #                 real_list = chapter_list[0:chapter_end_index - 1]
    #             else:
    #                 real_list = chapter_list
    #         for chapter in tqdm(real_list):
    #             file.write(chapter[0])
    #             file.write('\n')
    #             save_content(chapter[1])
    #             file.write('\n\n\n')
    #         file.close()


# if __name__ == '__main__':
#     # 搜索小说
#     # search("斗破苍穹")
#
#     # 批量全本下载
#     full_download(['https://www.biqugee.com//book/13991/'])
#
#     # 指定章节下载
#     # url = "https://www.biqugee.com/book/13991/"
#     # chapter_start_index = 3
#     # chapter_end_index = 5
#     # specify_download(url, chapter_start_index, chapter_end_index)