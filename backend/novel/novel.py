import time
from math import ceil

from flask import Blueprint, request, make_response, send_file
from backend.novel.biQuGe import BiQuGe
from backend.novel.qiDian import QiDian
from flask import jsonify

from backend.novel.saveChapter import saveChapterThread
from backend.utils.CommonUtil import remove_file, create_direction, get_root_path

novel = Blueprint('novel', __name__)
biQuGe = BiQuGe()
qiDian = QiDian()


@novel.route('/novel/<string:source>/search/<string:name>')
def search(source, name):
    novel_obj = get_source(source)
    return jsonify(novel_obj.search(name))


@novel.route('/novel/<string:source>/catalog')
def catalog(source):
    url = request.args['url']
    novel_obj = get_source(source)
    return jsonify(novel_obj.catalog(url))


# 小说本地存取路径
novel_direction = get_root_path() + '/download/novel/'
create_direction(novel_direction)


@novel.route('/novel/<string:source>/download')
def download(source):
    url = request.args['url']
    filename = request.args['fileName']

    novel_obj = get_source(source)
    start = time.time()
    chapter_list = novel_obj.catalog(url)
    if len(chapter_list) > 0:
        filepath = novel_direction + filename
        remove_file(filepath)
        thread_num = ceil(len(chapter_list) / 10.0)
        threads = []
        filename_list = []
        for index in range(thread_num):
            thread_chapter_list = chapter_list[index * 10:(index + 1) * 10]
            thread_filename = filename.replace(".txt", "_{}.txt".format(index))
            thread = saveChapterThread(thread_chapter_list, thread_filename, novel_obj.get_chapter_detail)
            thread.start()
            threads.append(thread)
            filename_list.append(thread_filename)
        for t in threads:
            t.join()
        file = open(filepath, 'a', encoding='utf-8')
        for thread_filename in filename_list:
            for line in open(thread_filename, encoding='utf8'):
                file.write(line)
            remove_file(thread_filename)
        file.close()
        response = make_response(send_file(filepath, as_attachment=True))
        end = time.time()
        print('【{}】 下载完成， 用时 {} 秒'.format(filename, end-start))
        return response

# @novel.route('/novel/<string:source>/download')
# def download(source):
#     url = request.args['url']
#     filename = request.args['fileName']
#     if source == 'biQuGe':
#         return biQuGe.full_download(url, novel_direction + filename)
#         # return biQuGe.file_download(novel_direction + filename, filename)
#         # return biQuGe.file_dir_download(novel_direction, filename)
#         # return biQuGe.file_stream_download(novel_direction, filename)
#     elif source == 'qiDian':
#         qiDian.full_download(url, novel_direction + filename)


def get_source(source):
    if source == 'biQuGe':
        novel_obj = biQuGe
    elif source == 'qiDian':
        novel_obj = qiDian
    return novel_obj


