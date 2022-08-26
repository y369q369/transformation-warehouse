import traceback

from flask import Blueprint, request

import backend.utils.CommonUtil as Common
from backend.video.tencent import Tencent

video = Blueprint('video', __name__)

tencent = Tencent()


@video.route('/video/<string:source>/searchVideo')
def searchVideo(source):
    url = request.args['url']
    if Common.check_url(url) is not None:
        return tencent.get_video_info(url)
    else:
        return {}


@video.route('/video/<string:source>/download', methods=['POST'])
def download(source):
    try:
        name = request.json.get('name')
        definition = request.json.get('definition')
        urls = request.json.get('urls')
        tencent.custom_download(name, definition, urls)
        return {'code': 200, 'msg': '下载成功'}
    except Exception as e:
        traceback.print_exc()
        return {'code': 201, 'msg': e}


video_root_direction = Common.get_root_path() + '/download/video/'
tencent_direction = video_root_direction + '腾讯/'
Common.create_direction(tencent_direction)
