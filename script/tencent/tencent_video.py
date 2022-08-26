""""""
import json
import math
import os
import re
import subprocess
import time
import traceback

import parsel
import requests

from backend.utils.CommonUtil import remove_file, create_direction, get_root_path
from backend.video.downloadThread import download_video

'''
    目标网址   ->    腾讯视频 ：https://v.qq.com/
    功能      ->    根据 地址 下载视频
'''

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
}

# 获取当前目录绝对路径
current_path = os.path.dirname(os.path.abspath(__file__))
tencent_cookie_path = "{}/config/tencent_cookie.txt".format(current_path)
tencent_tx_path = "{}/config/tx.js".format(current_path)
tencent_ckey_path = "{}/config/ckey.wasm".format(current_path)
video_download_path = "E:/video/"


class Tencent:
    main_login = 'qq'
    access_token = 'CB92B3C04AB6498E0E971BE4D8B17E62'
    vqq_openid = '2A643EEE51D87B77946C7CFE3481E097'
    vqq_appid = '101483052'
    vqq_vuserid = '424467340'
    # 使用前以下两项需替换
    vusession = 'VFRf1PU6Y7mxudbS-eAJ4g.N'
    guid = '1112c408de16f0e777662cda1a4de96d'

    # 刷新权限认证：用于获取m3u8
    def auth_refresh(self):
        url = 'https://access.video.qq.com/user/auth_refresh'
        params = {
            "vappid": '11059694',
            "vsecret": "fdf61a6be0aad57132bc5cdf78ac30145b6cd2c1470b0cfe",
            'type': 'qq',
            'g_tk': '',
            "g_vstk": "1884432280",  # 需注意
            "g_actk": "838124920",
            'callback': 'jQuery191024437950701339917_1661525269158',
            '-': '1661525269159'
        }
        with open(tencent_cookie_path, "r") as fp:
            tencent_cookie = fp.read()
        if tencent_cookie is None or tencent_cookie == '':
            tencent_cookie = 'vqq_access_token={}; vqq_openid={}; vqq_vuserid={}; vqq_vusession={}' \
                .format(self.access_token, self.vqq_openid, self.vqq_vuserid, self.vusession)
        tencent_headers = {
            "cookie": tencent_cookie,
            "referer": "https://v.qq.com/",
            # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        }
        resp = requests.get(url=url, params=params, headers=tencent_headers)
        text = resp.text
        text_temp = re.compile("(\{.*?\})")
        data = text_temp.findall(text)[0]
        info = json.loads(data)
        set_cookie = "main_login=qq; vqq_access_token={0}; vqq_appid={1}; " \
                     "vqq_openid=2A643EEE51D87B77946C7CFE3481E097; vqq_vuserid={2}; vqq_vusession={3}; " \
                     "vqq_next_refresh_time={4};".format(
            info["access_token"], self.vqq_appid, info["vuserid"], info["vusession"], info["next_refresh_time"])
        with open(tencent_cookie_path, "w", encoding="utf-8") as f:
            f.write(set_cookie)
        self.vusession = info["vusession"]

    # 获取剧集前缀
    def get_url_prefix(self, url):
        id_str = re.findall(r"https://v.qq.com/x/cover/(.*?)\.html", url)[0]
        if id_str.find('/') > 0:
            cover_id = id_str[:id_str.find('/')]
        else:
            cover_id = id_str
        return 'https://v.qq.com/x/cover/' + cover_id

    # 根据url获取 每集视频的信息
    def get_video_info(self, url):
        try:
            response = requests.get(url=url, headers=headers)
            selector = parsel.Selector(response.text)

            pinia_str = selector.re('<script>window.__pinia=(.*)</script>')
            pinia = json.loads(pinia_str[0].replace('undefined', '""'))
            cover_info = pinia['global']['coverInfo']
            video_description = cover_info['description']
            video_pic_url = cover_info['new_pic_hz']
            video_title = cover_info['title']
            video_second_title = cover_info['second_title']
            video_type = cover_info['type_name']
            video_list = []
            first_vid = cover_info['video_ids'][0]
            url_prefix = self.get_url_prefix(url)
            for item in pinia['episodeMain']['listData'][0]:
                if item['item_params']['is_no_store_watch_history'] == '0':
                    video_list.append({
                        'title': item['item_params']['c_title_output'],
                        'imageUrl': item['item_params']['image_url'],
                        'url': url_prefix + "/" + item['item_params']['vid'] + '.html'
                    })

            # 电视剧清晰度
            video_info_url = 'http://vv.video.qq.com/getinfo?otype=json&appver=3.2.19.333&platform=4100201&defnpayver=1&defn=hd&vid' \
                             '={}'.format(first_vid)
            video_info_response = requests.get(url=video_info_url, headers=headers)
            video_info = json.loads(video_info_response.content[len('QZOutputJson='):-1])
            fi_list = video_info['fl']['fi']
            definition_list = []
            for fi in fi_list:
                definition_list.append({
                    'name': fi['name'],
                    'cname': fi['cname'],
                })

            return {
                'title': video_title,
                'secondTitle': video_second_title,
                'picUrl': video_pic_url,
                'description': video_description,
                'type': video_type,
                'videos': video_list,
                'definitions': definition_list
            }
        except:
            traceback.print_exc()
            return {}

    # 根据 ckey.wasm 获取ckey
    def get_ckey(self, vid):
        text = "node {} {} {} {}".format(tencent_tx_path, vid, self.guid, tencent_ckey_path)
        p = subprocess.run(text, shell=True, stdout=subprocess.PIPE)
        return p.stdout.decode("utf-8")

    # 根据视频地址获取所有m3u8链接列表
    def get_m3u8(self, video_url, definition):
        vid = re.findall("https://.*/(.*?).html", video_url)[0]
        ckey = self.get_ckey(vid)
        proxy_http_url = 'https://vd.l.qq.com/proxyhttp'
        params = {
            'buid': 'vinfoad',
            'vinfoparam': 'spsrt=1&charge=0&defaultfmt=auto&otype=ojson&guid=&flowid=&platform=10201&sdtfrom=v1010' \
                          '&defnpayver=1&appVer=3.5.57&host=v.qq.com&ehost=%s&refer=v.qq.com&sphttps=1&tm=%s&spwm=4' \
                          '&logintoken={"main_login":"%s","openid":"%s","appid":"%s","access_token":"%s","vuserid":"%s",' \
                          '"vusession":"%s"}&unid=2798fc67442611eb89cd6c92bf48bcb2&vid=%s&defn=%s&fhdswitch=0&show1080p=1' \
                          '&isHLS=1&dtype=3&sphls=2&spgzip=1&dlver=2&drm=32&hdcp=0&spau=1&spaudio=15&defsrc=2&encryptVer=9' \
                          '.1&cKey=%s&fp2p=1&spadseg=3' % (
                              video_url, str(int(time.time())), self.main_login, self.vqq_appid, self.vqq_appid,
                              self.access_token, self.vqq_vuserid, self.vusession, vid, definition,
                              ckey.replace("\n", "&"))
        }
        proxy_http_headers = {
            "referer": "https://v.qq.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/86.0.4240.198 Safari/537.36",
        }
        proxy_http_res = requests.post(url=proxy_http_url, json=params, headers=proxy_http_headers)
        data = json.loads(proxy_http_res.content.decode("utf-8"))
        vinfo = json.loads(data["vinfo"])
        video = vinfo["vl"]["vi"][0]
        # 视频标题
        title = video["ti"]
        title_index = title.find('_')
        if title_index > 0:
            title = title[title_index + 1:]
        # 视频地址前缀
        url_prefix_list = []
        for m3u8_li in video["ul"]["ui"]:
            m3u8_url = m3u8_li['url']
            url_prefix_list.append(m3u8_url[:m3u8_url.rfind('/') + 1])
        # 每段视频地址（老版本的视频无 url.m3u8 ， 故通过请求链接地址获取所有m3u8片段地址）
        m3u8_response = requests.get(url=m3u8_url, headers=headers)
        m3u8_str = m3u8_response.text
        ts_list = re.findall("#EXTINF:\d+\.\d+,\\n(.*?)\\n", m3u8_str)
        video_info = {
            'title': title,
            'url_prefix_list': url_prefix_list,
            'ts_list': ts_list
        }
        return video_info

    # 自定义剧集下载
    def custom_download(self, video_name, definition, video_url_list):
        tv_dir = video_download_path + video_name
        create_direction(tv_dir)

        for video_url in video_url_list:
            st = time.time()
            video_info = self.get_m3u8(video_url, definition)
            print('\n{} - {} 开始下载'.format(video_name, video_info['title']))
            video_path = tv_dir + '/' + video_info['title'] + '.mp4'
            remove_file(video_path)
            url_prefix_list = video_info['url_prefix_list']
            ts_list = video_info['ts_list']

            if len(ts_list) > 0:
                urls = []
                for ts in ts_list:
                    urls.append(url_prefix_list[0] + ts)

                download_video(video_path, urls)
                et = time.time()
                print("{} - {} 下载完成， 总耗时： {} s".format(video_name, video_info['title'], math.ceil(et - st)))
            else:
                self.auth_refresh()
                print("刷新权限后重新下载 {}".format(video_info['title']))
                self.custom_download(video_name, definition, video_url_list)

    # 全部剧集下载（注意：电影会下载各语言版本）
    def full_download(self, video_url, definition='fhd'):
        ast = time.time()
        info = self.get_video_info(video_url)
        video_name = info['title']
        urls = []
        for video in info['videos']:
            urls.append(video['url'])
        print('{} 所有视频信息获取完成，共 {} 集 准备下载'.format(video_name, len(urls)))
        self.custom_download(video_name, definition, urls)
        aet = time.time()
        print('{} {} 集下载完成, 总耗时 {} s'.format(video_name, len(urls), math.ceil(aet - ast)))


tencent = Tencent()

if __name__ == '__main__':
    video_url = 'https://v.qq.com/x/cover/mzc00200p29gosv/x0036gyn378.html'
    video_name = '斗破苍穹 第4季'
    # 1080p
    definition = 'fhd'
    # 全集下载
    tencent.full_download(video_url)
