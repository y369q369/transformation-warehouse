import backend.utils.CommonUtil as Common

from flask import Blueprint, request, jsonify
from backend.video.tencent import Tencent

video = Blueprint('video', __name__)

tencent = Tencent()


@video.route('/video/<string:source>/search/<string:videoType>')
def search(source, videoType):
    url = request.args['url']
    if Common.check_url(url) is not None:
        return tencent.get_video_info(url)
    else:
        return {}


@video.route('/video/<string:source>/download/<string:videoType>', methods=['POST'])
def download(source, videoType):
    name = request.json.get('name')
    urls = request.json.get('urls')
    tencent.tv_custom_download(name, urls)
    return {'code': 0}


# 小说本地存取路径
video_root_direction = Common.get_root_path() + '/download/video/'
tencent_direction = video_root_direction + '腾讯/'
Common.create_direction(tencent_direction)
