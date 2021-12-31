from flask import Flask
from novel.novel import novel
from video.video import video
from study.download import download

app = Flask(__name__)
# 注册蓝图
app.register_blueprint(novel)
app.register_blueprint(video)
app.register_blueprint(download)


@app.route('/')
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'


if __name__ == '__main__':
    app.run(port='9080')
