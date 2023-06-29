import json
from datetime import datetime

from script.utils.video_util import *

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50'}

video_download_path = "E:/video/test"


def video_download(url):
    st = datetime.now()
    result = requests.get(url, headers=headers)
    m3u8_data = result.text.split("\n")
    url_prefix = url[:url.rindex("/") + 1]
    url_list = []
    file_list = []
    for item in m3u8_data:
        if item != '' and not item.startswith("#"):
            url_list.append(url_prefix + item)
            file_list.append(item[item.rindex("/") + 1:item.index("?")])
    split_process_download(headers, video_download_path, 4, url_list, file_list, "test.mp4")

    et = datetime.now()
    print(f'    耗时 {(et - st).seconds} 秒， {(et - st).seconds // 60} 分钟')


if __name__ == "__main__":
# url = "https://hw-vod.cdn.huya.com/1048585/1099511682177/47526925/0e8d849a23c6a490a8dc49aa8194af41.m3u8?hyvid=604337993&hyauid=2341792254&hyroomid=2341792254&hyratio=1300&hyscence=vod&appid=66&domainid=25&srckey=NjZfMjVfNjA0MzM3OTkz&bitrate=1375&client=109&definition=1300&pid=2341792254&scene=vod&vid=604337993&u=670682210&t=100&sv=2303161809"
# video_download(url)
