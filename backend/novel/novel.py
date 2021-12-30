from flask import Blueprint, request
from novel.biQuGe import BiQuGe
from novel.qiDian import QiDian
from flask import jsonify
import os

novel = Blueprint('novel', __name__)
biQuGe = BiQuGe()
qiDian = QiDian()


@novel.route('/novel/<string:source>/search/<string:name>')
def search(source, name):
    print(request)
    if source == 'biQuGe':
        return jsonify(biQuGe.search(name))
    elif source == 'qiDian':
        return jsonify(qiDian.search(name))
    else:
        return jsonify([])


@novel.route('/novel/<string:source>/catalog')
def catalog(source):
    url = request.args['url']
    if source == 'biQuGe':
        return jsonify(biQuGe.catalog(url))
    elif source == 'qiDian':
        return jsonify(qiDian.catalog(url))
    else:
        return jsonify([])


novel_direction = 'download/novel/'


@novel.route('/novel/<string:source>/download')
def download(source):
    url = request.args['url']
    filename = request.args['fileName']
    if source == 'biQuGe':
        # return biQuGe.full_download(url, novel_direction + filename)
        # return biQuGe.file_download(novel_direction + filename, filename)
        # return biQuGe.file_dir_download(novel_direction, filename)
        return biQuGe.file_stream_download(novel_direction, filename)
    elif source == 'qiDian':
        qiDian.full_download(url, novel_direction + filename)


# 创建小说下载目录
def create_direction(direction):
    if not os.path.exists(direction):
        os.makedirs(direction)


create_direction(novel_direction)
