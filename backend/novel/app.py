from flask import Blueprint

novel = Blueprint('novel', __name__)


@novel.route('/novel')
def novel2():
    return 'novel2'
