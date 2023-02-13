import json
import math
import os
import re
import subprocess
import time
import urllib

import parsel
import requests

'''
    目标网址   ->    腾讯视频 ：https://www.youku.com/
    功能      ->    根据 地址 下载优酷视频
'''

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'referer': 'https://www.bilibili.com'
}

# 获取当前目录绝对路径
current_path = os.path.dirname(os.path.abspath(__file__))
video_download_path = "E:/video/"


class BiLi:

    # 获取电视剧信息
    def get_video_info(self, url):
        header = {
            'cookie': 'cna=gAXaGUK+3w8CAXAUXTWZcdbb'
        }
        response = requests.get(url=url, headers=header)
        selector = parsel.Selector(response.text)

        init_data_str = selector.re('window.__INITIAL_DATA__ =(.*);</script>')
        init_data = json.loads(init_data_str[0].replace('undefined', '""'))
        # 获取视频基本信息
        extra_data = init_data['data']['data']['data']['extra']
        video_title = extra_data['showName']
        video_second_title = extra_data['showSubtitle']
        video_type = extra_data['showCategory']
        video_pic_url = extra_data['showImgV']
        video_description = init_data['data']['data']['nodes'][0]['nodes'][0]['nodes'][0]['data']['desc']

        # 获取列表信息
        end_stage = extra_data['episodeFinalStage']
        video_id = extra_data['videoId']
        show_id = extra_data['showId']
        videos = self.get_video_list(show_id, video_id, end_stage)

        return {
            'title': video_title,
            'secondTitle': video_second_title,
            'picUrl': video_pic_url,
            'description': video_description,
            'type': video_type,
            'videos': videos,
            'definitions': []
        }

    def custom_download(self, url_list):
        for url in url_list:
            headers['range'] = 'bytes=112268-296136'
            response = requests.get(url, headers=headers)
            # print(response.text)
            with open(video_download_path + 'test/' + 't1.m4s', 'ab') as video:
                video.write(response.content)
            video.close()

    def get_download_list(self):
        url = 'https://valipl10.cp31.ott.cibntv.net/65731D34B763671755732370E/03000900006299ACCC8BB780000000726D6C89-58A4-4C09-BEF6-3D5C3CBC1A73-11-54247245.m3u8?ccode=0502&duration=2721&expire=18000&psid=0234e02b87701ed20969e4b8acf2337941346&ups_client_netip=2471915a&ups_ts=1661926416&ups_userid=999830345&utid=gAXaGUK%2B3w8CAXAUXTWZcdbb&vid=XNTg1MjcwNjQwNA%3D%3D&vkey=Bd4e75e70fbed600cf783b52c26ee85ed&s=bbfdcd5525264a2eb8fd&iv=1&eo=0&t=8cb8d34768c724b&cug=1&fms=ce0126c0343c302c&tr=2706&le=958e1be54f19b23c5c4541e95c6e2412&ckt=5&m_onoff=0&rid=20000000CD33CFD64E89FBA1E4026417683056A402000000&type=mp4hd3v3&bc=2&dre=u151&si=573&dst=1&sm=1&operate_type=1&hotvt=1'
        res = requests.get(url)
        download_url_list = re.findall('\nhttp(.*)\n', res.content.decode("utf-8"))
        for index in range(len(download_url_list)):
            download_url_list[index] = 'http' + download_url_list[index]
        return download_url_list


b = BiLi()
if __name__ == '__main__':
    url_list = [
        'https://cn-ahhn-cm-01-04.bilivideo.com/upgcxcode/67/10/803181067/803181067-1-100023.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1662106534&gen=playurlv2&os=bcache&oi=0&trid=0000fe757c01c11a4109845f8a663b185e40u&mid=64743288&platform=pc&upsig=0f5692916a2536e9060b355979e983eb&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&cdnid=10101&bvc=vod&nettype=0&orderid=0,3&agrr=1&bw=28648&logo=80000000']
    b.custom_download(url_list)
