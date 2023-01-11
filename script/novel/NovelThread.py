import threading

import requests


class ChapterContent:
    def __init__(self, url_list):
        threading.Thread.__init__(self)
        self.url_list = url_list

    def run(self):
        try:
            res = requests.get(downloadUrl, timeout=10)
            video.write(res.content)
            time.sleep(0.1)
        except:
            print("{}   {} 下载异常".format(self.tempFilePath, downloadUrl))
            traceback.print_exc()
            res = requests.get(downloadUrl, timeout=10)
            video.write(res.content)
            time.sleep(0.1)
