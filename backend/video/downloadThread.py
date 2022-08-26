import math
import traceback
import requests
import threading
import os
import time


class Download(threading.Thread):
    def __init__(self, temp_file_path, tempUrls):
        threading.Thread.__init__(self)
        self.tempFilePath = temp_file_path
        self.tempUrls = tempUrls
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    def run(self):
        st = time.time()
        with open(self.tempFilePath, 'ab') as video:
            for downloadUrl in self.tempUrls:
                try:
                    res = requests.get(downloadUrl, timeout=3)
                    video.write(res.content)
                    time.sleep(0.1)
                except:
                    print("{}   {} 下载异常".format(self.tempFilePath, downloadUrl))
                    traceback.print_exc()
                    res = requests.get(downloadUrl, timeout=3)
                    video.write(res.content)
                    time.sleep(0.1)
            video.close()
        et = time.time()
        print("完成下载： {} 耗时： {} s".format(self.tempFilePath, math.ceil(et - st)))


threadNum = 3


# 合并临时文件
def composite_file(file_path, temp_file_list):
    with open(file_path, "ab") as f:
        for temp_file in temp_file_list:
            with open(temp_file, "rb") as video:
                f.write(video.read())
            video.close()

    for temp_file in temp_file_list:
        os.remove(temp_file)


# 下载视频
def download_video(filePath, urls):
    piece_size = len(urls) // threadNum
    threads = []
    temp_file_list = []

    for i in range(threadNum):
        if i == threadNum - 1:
            temp_urls = urls[i * piece_size:]
        else:
            temp_urls = urls[i * piece_size:(i + 1) * piece_size]
        temp_file = '{}.tmp{}'.format(filePath, i + 1)
        temp_file_list.append(temp_file)
        thread = Download(temp_file, temp_urls)
        threads.append(thread)
        thread.start()
    # 等待所有线程完成
    for t in threads:
        t.join()
    # 合并文件
    composite_file(filePath, temp_file_list)


if __name__ == '__main__':
    ticks = time.time()
    time.sleep(2)
    ticks2 = time.time()
    print(ticks)
    print(ticks2)
    print(ticks2 - ticks)
