from flask import Flask
from novel.novel import novel
from viedo.video import video

app = Flask(__name__)
# 注册蓝图
app.register_blueprint(novel)
app.register_blueprint(video)


@app.route('/')
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'


if __name__ == '__main__':
    app.run(port='9080')
