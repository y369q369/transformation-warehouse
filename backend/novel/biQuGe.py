""""""
import requests
import parsel
import os
from tqdm import tqdm
from flask import make_response, send_file, send_from_directory, Response

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

    # 全本下载
    def full_download(self, url, filename):
        chapter_list = self.catalog(url)
        if len(chapter_list) > 0:
            remove_novel(filename)
            file = open(filename, 'a', encoding='utf-8')
            for chapter in tqdm(chapter_list):
                detail = self.get_chapter_detail(chapter)
                file.write(detail)
            file.close()
            response = make_response(send_file(filename))
            response.headers["Content-Disposition"] = "attachment; filename={}".format(
                filename.encode().decode('latin-1'))
            return response

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

    def file_download(self, file, filename):
        #     """
        #     单个小文件下载
        #     :param file: 待下载的文件(文件路径+文件名)
        #     :param filename: 下载的文件名称
        #     """
        # 写法一
        response = make_response(send_file(file, as_attachment=True))
        # 写法二
        # response = make_response(send_file(file))
        # response.headers["Content-Disposition"] = "attachment; filename={}".format(
        #     filename.encode().decode('latin-1'))
        return response

    def file_dir_download(self, filepath, filename):
        #     """
        #     基于文件夹路径和文件名下载，两种写法同 file_download
        #     :param filepath: 待下载的文件路径
        #     :param filename: 下载的文件名称
        #     """
        response = make_response(send_from_directory(filepath, filename, as_attachment=True))
        return response

    def file_stream_download(self, filepath, filename):
        #     """
        #     文件流式下载
        #     :param filepath: 待下载的文件路径
        #     :param filename: 下载的文件名称
        #     """
        def send_chunk():
            # 流式读取
            store_path = filepath + filename
            with open(store_path, 'rb') as target_file:
                while True:
                    chunk = target_file.read(10 * 1024)  # 每次读取10K
                    if not chunk:
                        break
                    yield chunk

        response = Response(send_chunk())
        response.headers['content_type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename.encode().decode('latin-1'))
        return response


def remove_novel(filepath):
    #     """
    #     移除小说
    #     :param filepath: 待下载的文件路径
    #     """
    if os.path.exists(filepath):
        os.remove(filepath)



        # 获取所有章节url
    # def catalog(self, url):
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
