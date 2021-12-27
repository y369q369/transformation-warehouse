from flask import Blueprint
from novel.biQuGe import BiQuGe
from flask import jsonify

novel = Blueprint('novel', __name__)
biQuGe = BiQuGe()


@novel.route('/novel/biQuGe/<string:name>')
def biQuGe_search(name):
    search_results = biQuGe.search(name)
    # return search_results
    return jsonify(search_results)


@novel.route('/novel/qiDian/qiDian')
def qiDian_search():
    dict1 = {"index":"haha"}
    return jsonify(dict1)

@novel.route('/novel/qiDian/qiDian2')
def qiDian_search2():
    dict1 = ["index","haha"]
    return jsonify(dict1)

@novel.route('/novel/qiDian/qiDian3')
def qiDian_search3():
    dict1 = [{"index":"haha"}]
    return jsonify(dict1)