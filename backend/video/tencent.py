""""""
import json
import os
import re
import subprocess
import time

import parsel
import requests
from tqdm import tqdm

from backend.utils.CommonUtil import remove_file, create_direction, get_root_path

'''
    目标网址   ->    腾讯视频 ：https://v.qq.com/
    功能      ->    根据 地址 下载视频
'''

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
}

# 获取当前目录绝对路径
root_path = get_root_path()
tencent_cookie_path = "{}/cookies/tencent_cookie.txt".format(root_path)
tencent_tx_path = "{}/video/tencent/tx.js".format(root_path)
tencent_ckey_path = "{}/video/tencent/ckey.wasm".format(root_path)
video_download_path = "{}/download/video/腾讯/".format(root_path)


class Tencent:
    main_login = 'qq'
    access_token = 'CB92B3C04AB6498E0E971BE4D8B17E62'
    vqq_openid = '2A643EEE51D87B77946C7CFE3481E097'
    vqq_appid = '101483052'
    vqq_vuserid = '424467340'
    vusession = 'qKyOo4YqqJ-LzPaU7HCN2A..'
    guid = '6a4a6faaf0becf989d066e8aa8145c6c'

    # def __init__(self):
    #     self.cookie = self.auth_refresh()

    # 刷新权限认证
    def auth_refresh(self):
        url = 'https://access.video.qq.com/user/auth_refresh'
        params = {
            "vappid": '11059694 ',
            "vsecret": "fdf61a6be0aad57132bc5cdf78ac30145b6cd2c1470b0cfe",
            "g_vstk": "212010658",  # 需注意
            "g_actk": "838124920",
            'type': 'qq',
            'callback': 'jQuery1910837930383711655_1642575281941',
            '-': '1642575281942'
        }
        with open(tencent_cookie_path, "r") as fp:
            tencent_cookie = fp.read()
        if tencent_cookie is None or tencent_cookie == '':
            tencent_cookie = 'vqq_access_token={}; vqq_openid={}; vqq_vuserid={}; vqq_vusession={}' \
                .format(self.access_token, self.vqq_openid, self.vqq_vuserid, self.vusession)
        tencent_headers = {
            "cookie": tencent_cookie,
            "referer": "https://v.qq.com/",
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
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
        return set_cookie

    def get_url_prefix(self, url):
        # 获取剧集前缀
        id_str = re.findall(r"https://v.qq.com/x/cover/(.*?)\.html", url)[0]
        if id_str.find('/') > 0:
            cover_id = id_str[:id_str.find('/')]
        else:
            cover_id = id_str
        return 'https://v.qq.com/x/cover/' + cover_id

    # 获取电视剧每集视频的编号
    def get_video_info(self, url):
        try:
            response = requests.get(url=url, headers=headers)
            response.encoding = 'utf-8'
            selector = parsel.Selector(response.text)

            # 电视剧列表
            scripts = selector.css('head script')
            for script in scripts:
                template_flag = script.css('::attr(r-notemplate)').get()
                script_type = script.css('::attr(type)').get()
                if template_flag == 'true' and script_type == 'text/javascript':
                    script_content = script.css('::text').get()
                    video_id_str = re.findall(r"var COVER_INFO = (.*?)\nvar COLUMN_INFO", script_content)

            if video_id_str is not None and len(video_id_str) > 0:
                url_prefix = self.get_url_prefix(url)
                cover_info = json.loads(video_id_str[0])
                video_description = cover_info['description']
                video_pic_url = cover_info['new_pic_hz']
                video_title = cover_info['title']
                video_second_title = cover_info['second_title']
                video_type = cover_info['type_name']
                video_list = []
                first_vid = cover_info['video_ids'][0]
                for video_id in cover_info['video_ids']:
                    video_list.append(url_prefix + "/" + video_id + '.html')

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
                tv_info = {
                    'title': video_title,
                    'secondTitle': video_second_title,
                    'picUrl': video_pic_url,
                    'description': video_description,
                    'type': video_type,
                    'videos': video_list,
                    'definitions': definition_list
                }
                return tv_info
            else:
                return {}
        except:
            print('Error 解析异常')
            return {}

    # 获取电视剧每集视频的编号
    def get_chapter_list(self, cover_id):
        url = 'https://v.qq.com/x/cover/{}.html'.format(cover_id)
        response = requests.get(url=url, headers=headers)
        selector = parsel.Selector(response.text)
        # 电视剧名称
        title = selector.css('.player_title a::text').get()
        # 电视剧列表
        scripts = selector.css('head script')
        video_id_list = []
        for script in scripts:
            template_flag = script.css('::attr(r-notemplate)').get()
            script_type = script.css('::attr(type)').get()
            if template_flag == 'true' and script_type == 'text/javascript':
                cover_info = script.css('::text').get()
                video_id_str = re.findall(r"video_ids\":\[\"(.+?)\"\],\"vertical_pic_url", cover_info)
                video_id_list = video_id_str[0].split('","')
        # 电视剧清晰度
        video_info_url = 'http://vv.video.qq.com/getinfo?otype=json&appver=3.2.19.333&platform=4100201&defnpayver=1&defn=hd&vid' \
                         '={}'.format(video_id_list[0])
        video_info_response = requests.get(url=video_info_url, headers=headers)
        video_info = json.loads(video_info_response.content[len('QZOutputJson='):-1])
        fi_list = video_info['fl']['fi']
        definition_list = []
        for fi in fi_list:
            definition_list.append({
                'name': fi['name'],
                'cname': fi['cname'],
            })
        tv_info = {
            'title': title,
            'video_id_list': video_id_list,
            'definition_list': definition_list
        }
        return tv_info

    # 整个MP4下载（根据you-get摸索出的接口，当前只适配 超清-shd ）
    def download_mp4(self, video_id):
        video_info_url = 'http://vv.video.qq.com/getinfo?otype=json&appver=3.2.19.333&platform=4100201&defnpayver=1&defn=shd&vid' \
                         '={}'.format(video_id)
        video_info_response = requests.get(url=video_info_url, headers=headers)
        video_info = json.loads(video_info_response.content[len('QZOutputJson='):-1])
        url_prefix = video_info['vl']['vi'][0]['ul']['ui'][0]['url']
        filename = video_info['vl']['vi'][0]['fn']
        video_key_url = 'http://vv.video.qq.com/getkey?otype=json&platform=11&format=10217&appver=3.2.19.333&vid' \
                        '={}&filename={}'.format(video_id, filename)
        full_mp4_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/96.0.4664.45 Safari/537.36',
            'Cookie': 'vqq_access_token={}; vqq_appid={}; vqq_openid={}; '
                .format(self.access_token, self.vqq_appid, self.vqq_appid)
        }
        video_key_response = requests.get(url=video_key_url, headers=full_mp4_headers)
        video_key = json.loads(video_key_response.content[len('QZOutputJson='):-1])
        key = video_key['key']
        video_real_url = '{}{}?vkey={}'.format(url_prefix, filename, key)
        video_real_response = requests.get(url=video_real_url, headers=headers)
        content = video_real_response.content

    # 根据 ckey.wasm 获取ckey
    def get_ckey(self, vid):
        text = "node {} {} {} {}".format(tencent_tx_path, vid, self.guid, tencent_ckey_path)
        p = subprocess.run(text, shell=True, stdout=subprocess.PIPE)
        return p.stdout.decode("utf-8")

    # 根据视频地址获取所有m3u8链接列表
    def get_m3u8(self, video_url):
        vid = re.findall("https://.*/(.*?).html", video_url)[0]
        ckey = self.get_ckey(vid)
        proxy_http_url = 'https://vd.l.qq.com/proxyhttp'
        data = {
                    'buid': 'vinfoad',
                    'vinfoparam': 'spsrt=1&charge=0&defaultfmt=auto&otype=ojson&guid=&flowid=&platform=10201&sdtfrom=v1010' \
                                  '&defnpayver=1&appVer=3.5.57&host=v.qq.com&ehost=%s&refer=v.qq.com&sphttps=1&tm=%s&spwm=4' \
                                  '&logintoken={"main_login":"%s","openid":"%s","appid":"%s","access_token":"%s","vuserid":"%s",' \
                                  '"vusession":"%s"}&unid=2798fc67442611eb89cd6c92bf48bcb2&vid=%s&defn=fhd&fhdswitch=0&show1080p=1' \
                                  '&isHLS=1&dtype=3&sphls=2&spgzip=1&dlver=2&drm=32&hdcp=0&spau=1&spaudio=15&defsrc=2&encryptVer=9' \
                                  '.1&cKey=%s&fp2p=1&spadseg=3' % (
                                      video_url, str(int(time.time())), self.main_login, self.vqq_appid, self.vqq_appid,
                                      self.access_token, self.vqq_vuserid, self.vusession, vid, ckey.replace("\n", "&"))
                }
        proxy_http_headers = {
            "referer": "https://v.qq.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/86.0.4240.198 Safari/537.36",
        }
        proxy_http_res = requests.post(url=proxy_http_url, json=data, headers=proxy_http_headers)
        data = json.loads(proxy_http_res.content.decode("utf-8"))
        vinfo = json.loads(data["vinfo"])
        video = vinfo["vl"]["vi"][0]
        # 视频标题
        title = video["ti"]
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
    def tv_custom_download(self, tv_name, video_url_list):
        tv_dir = video_download_path + tv_name
        create_direction(tv_dir)

        for video_url in video_url_list:
            video_info = self.get_m3u8(video_url)
            print('{} 开始下载'.format(video_info['title']))
            video_path = tv_dir + '/' + video_info['title'] + '.mp4'
            remove_file(video_path)
            url_prefix_list = video_info['url_prefix_list']
            ts_list = video_info['ts_list']
            with open(video_path, 'ab') as video:
                for ts in tqdm(ts_list):
                    try:
                        res = requests.get(url=url_prefix_list[0] + ts, timeout=3)
                        video.write(res.content)
                        time.sleep(0.5)
                    except:
                        video_info = self.get_m3u8(video_url)
                        url_prefix_list = video_info['url_prefix_list']

                        print(url_prefix_list[0] + ts)
                        res = requests.get(url=url_prefix_list[0] + ts, timeout=3)
                        video.write(res.content)
                video.close()

    # 完整电视剧下载
    def tv_download(self, cover_id):
        tv_info = self.get_chapter_list(cover_id)
        video_id_list = tv_info['video_id_list']
        tv_dir = video_download_path + tv_info['title']
        os.makedirs(tv_dir)

        for video_id in video_id_list:
            video_info = self.get_m3u8('https://v.qq.com/x/cover/{}/{}.html'.format(cover_id, video_id))
            video = open(tv_dir + '/' + video_info['title'], 'a', encoding='utf-8')
            url_prefix_list = video_info['url_prefix_list']
            ts_list = video_info['ts_list']
            for ts in ts_list:
                ts_content = requests.get(url=url_prefix_list[0] + ts).content
                video.write(ts_content)
            video.close()

