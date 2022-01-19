""""""
import json
import os
import subprocess
import time

import requests
import parsel
import re

'''
    目标网址   ->    腾讯视频 ：https://v.qq.com/
    功能      ->    根据 地址 下载视频
'''

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
}

# 获取当前目录绝对路径
dir_path = os.path.dirname(os.path.abspath(__file__))
tencent_cookie_path = "{}/../cookies/tencent_cookie.txt".format(dir_path)
tencent_tx_path = "{}/tencent/tx.js".format(dir_path)
tencent_ckey_path = "{}/tencent/ckey.wasm".format(dir_path)


class Tencent:
    main_login = 'qq'
    access_token = 'CB92B3C04AB6498E0E971BE4D8B17E62'
    vqq_openid = '2A643EEE51D87B77946C7CFE3481E097'
    vqq_appid = '101483052'
    vqq_vuserid = '424467340'
    vusession = 'v0GwHyeRMm-RwbB9aLZCog..'
    guid = '4583de6cef1c3803'

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

    # 获取电视剧每集视频的编号
    def get_chapter_list(self, cover_id):
        url = 'https://v.qq.com/x/cover/{}.html'.format(cover_id)
        response = requests.get(url=url, headers=headers)
        selector = parsel.Selector(response.text)
        scripts = selector.css('head script')
        video_id_list = []
        for script in scripts:
            template_flag = script.css('::attr(r-notemplate)').get()
            script_type = script.css('::attr(type)').get()
            if template_flag == 'true' and script_type == 'text/javascript':
                cover_info = script.css('::text').get()
                video_id_str = re.findall(r"video_ids\":\[\"(.+?)\"\],\"vertical_pic_url", cover_info)
                video_id_list = video_id_str[0].split('","')
        return video_id_list

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
        print(video_real_url)
        video_real_response = requests.get(url=video_real_url, headers=headers)
        content = video_real_response.content
        print(content)






    # 根据 ckey.wasm 获取ckey
    def get_ckey(self, vid):
        text = "node {} {} {} {}".format(tencent_tx_path, vid, self.guid, tencent_ckey_path)
        p = subprocess.run(text, shell=True, stdout=subprocess.PIPE)
        return p.stdout.decode("utf-8")


    def get_m3u8(self, video_url, vid, ckey):
        proxyhttp_url = 'https://vd.l.qq.com/proxyhttp'
        vinfoparam = 'spsrt=1&charge=0&defaultfmt=auto&otype=ojson&guid=&flowid=&platform=10201&sdtfrom=v1010' \
                     '&defnpayver=1&appVer=3.5.57&host=v.qq.com&ehost=%s&refer=v.qq.com&sphttps=1&tm=%s&spwm=4' \
                     '&logintoken={"main_login":"%s","openid":"%s","appid":"%s","access_token":"%s","vuserid":"%s",' \
                     '"vusession":"%s"}&unid=2798fc67442611eb89cd6c92bf48bcb2&vid=%s&defn=fhd&fhdswitch=0&show1080p=1' \
                     '&isHLS=1&dtype=3&sphls=2&spgzip=1&dlver=2&drm=32&hdcp=0&spau=1&spaudio=15&defsrc=2&encryptVer=9' \
                     '.1&cKey=%s&fp2p=1&spadseg=3' % (
            video_url, str(int(time.time())), self.main_login, self.vqq_appid, self.vqq_appid, self.access_token,
            self.vqq_vuserid, self.vusession, vid, ckey.replace("\n", "&"))
        body = {"buid": "vinfoad",
                "vinfoparam": vinfoparam}
        proxyhttp_headers = {
            "referer": "https://v.qq.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        resp = requests.post(url=proxyhttp_url, json=body, headers=proxyhttp_headers)
        data = json.loads(resp.content.decode("utf-8"))
        vinfo = data["vinfo"]
        vinfo = json.loads(vinfo)
        video = vinfo["vl"]["vi"][0]
        title = video["ti"]
        video_url = video["ul"]["ui"][0]["url"]  # json数据中共四个url,这里选第一个，但实测 四个基本是一样的清晰度的。 第四个无法播放！！！ 昨天都还可以，今天凉了，不知原因
        print("解析成功 >>> 标题：{0}\tm3u8播放地址：{1}".format(title, video_url))
        return video_url


tencent = Tencent()
# tencent.get_ckey('y004178oob9')
ckey = tencent.get_ckey('y004178oob9')
tencent.get_m3u8('https://v.qq.com/x/cover/mzc00200iyo8n07/y004178oob9.html', 'y004178oob9', ckey)