from flask import Blueprint

video = Blueprint('video', __name__)


@video.route('/video')
def video2():
    return 'video2'
