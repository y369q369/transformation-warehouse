import parsel
import requests

'''
    目标网址   ->    腾讯视频 ：https://www.youku.com/
    功能      ->    根据 地址 下载优酷视频
'''

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
}


class Youku:
    # 获取电视剧每集视频的编号
    def get_video_info(self, url):
        response = requests.get(url=url, headers=headers)
        selector = parsel.Selector(response.text)
        title = selector.css(".thesis-wrap a::text").get()
        page_size = len(selector.css(".top-wrap a"))
        print(title)
        print(page_size)


y = Youku()
y.get_video_info(
    "https://v.youku.com/v_show/id_XMzc1OTA1MDY2MA==.html?spm=a2hbt.13141534.1_2.d1_5&scm=20140719.api.46108.show_69efbfbdefbfbd343a00&s=69efbfbdefbfbd343a00")
