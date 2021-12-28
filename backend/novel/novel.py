from flask import Blueprint
from novel.biQuGe import BiQuGe
from novel.qiDian import QiDian
from flask import jsonify

novel = Blueprint('novel', __name__)
biQuGe = BiQuGe()
qiDian = QiDian()


@novel.route('/novel/<string:source>/search/<string:name>')
def search(source, name):
    if source == 'biQuGe' :
        return jsonify(biQuGe.search(name))
    elif source == 'qiDian':
        return jsonify(qiDian.search(name))
    else:
        return jsonify([])


@novel.route('/novel/<string:source>/catalog/<string:name>')
def catalog(source, name):
    if source == 'biQuGe' :
        return jsonify(biQuGe.catalog(name))
    elif source == 'qiDian':
        return jsonify(qiDian.catalog(name))
    else:
        return jsonify([])


@novel.route('/novel/<string:source>/download/<string:name>')
def download(source, name):
    if source == 'biQuGe' :
        return jsonify(biQuGe.search(name))
    elif source == 'qiDian':
        return jsonify(qiDian.search(name))
    else:
        return jsonify([])