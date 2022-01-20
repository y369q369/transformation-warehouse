import backend.utils.CommonUtil as Common

from flask import Blueprint, request
from backend.video.tencent import Tencent

video = Blueprint('video', __name__)

tencent = Tencent()


@video.route('/video/<string:source>/search/<string:videoType>')
def download(source, videoType):
    url = request.args['url']
    if Common.check_url(url) is not None:
        return tencent.get_video_info(url)
    else:
        return {}


# 小说本地存取路径
video_root_direction = Common.get_root_path() + '/download/video/'
tencent_direction = video_root_direction + '腾讯/'
Common.create_direction(tencent_direction)



