import json
import math
import os
import re
import subprocess
import time
import urllib
import base64
from hashlib import md5

import parsel
import requests

'''
    目标网址   ->    腾讯视频 ：https://www.youku.com/
    功能      ->    根据 地址 下载优酷视频
'''

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
}

# 获取当前目录绝对路径
current_path = os.path.dirname(os.path.abspath(__file__))
youKu_cookie_path = "{}/youKu/youKu_cookie.txt".format(current_path)
youKu_sign_path = "{}/youKu/sign.js".format(current_path)
video_download_path = "E:/video/"


class Youku:
    ysuid = '16382606358438Gu'
    _m_h5_tk = ''
    _m_h5_tk_enc = ''
    token = ''
    # 过期时间一年
    cna = 'gAXaGUK+3w8CAXAUXTWZcdbb'
    appKey = 24679788

    def __init__(self):
        self.flush_token()

    # 刷新token
    def flush_token(self):
        # 随便 找个接口刷新token，token在响应头的Set-Cookie属性中
        url = 'https://acs.youku.com/h5/mtop.youku.columbus.gateway.new.execute/1.0/?jsv=2.6.2&appKey=24679788'
        response = requests.get(url=url)
        response_headers = response.headers
        token_str = response_headers.get('Set-Cookie')
        token_list = re.findall(
            '_m_h5_tk=(.*);Path=/;Domain=youku.com;Max-Age=86400, _m_h5_tk_enc=(.*);Path=/;Domain=youku.com;Max-Age=86400',
            token_str)[0]
        self._m_h5_tk = token_list[0]
        self._m_h5_tk_enc = token_list[1]
        self.token = token_list[0].split('_')[0]

        with open(youKu_cookie_path, "w", encoding="utf-8") as f:
            f.write(token_str)

    # 获取电视剧信息
    def get_video_info(self, url):
        header = {
            'cookie': self.cna
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

    # 获取电视剧每集视频的编号
    def get_video_list(self, show_id, video_id, end_stage=100):
        start_stage = 1

        data = "\"{\\\"ms_codes\\\":\\\"2019030100\\\",\\\"params\\\":\\\"{\\\\\\\"biz\\\\\\\":true," \
               "\\\\\\\"scene\\\\\\\":\\\\\\\"component\\\\\\\",\\\\\\\"componentVersion\\\\\\\":\\\\\\\"3\\\\\\\"," \
               "\\\\\\\"ip\\\\\\\":\\\\\\\"36.113.145.90\\\\\\\",\\\\\\\"debug\\\\\\\":0," \
               "\\\\\\\"utdid\\\\\\\":\\\\\\\"gAXaGUK+3w8CAXAUXTWZcdbb\\\\\\\"," \
               "\\\\\\\"userId\\\\\\\":\\\\\\\"999830345\\\\\\\",\\\\\\\"platform\\\\\\\":\\\\\\\"pc\\\\\\\"," \
               "\\\\\\\"gray\\\\\\\":0,\\\\\\\"nextSession\\\\\\\":\\\\\\\"{" \
               "\\\\\\\\\\\\\\\"componentIndex\\\\\\\\\\\\\\\":\\\\\\\\\\\\\\\"3\\\\\\\\\\\\\\\"," \
               "\\\\\\\\\\\\\\\"componentId\\\\\\\\\\\\\\\":\\\\\\\\\\\\\\\"61518\\\\\\\\\\\\\\\"," \
               "\\\\\\\\\\\\\\\"level\\\\\\\\\\\\\\\":\\\\\\\\\\\\\\\"2\\\\\\\\\\\\\\\"," \
               "\\\\\\\\\\\\\\\"itemPageNo\\\\\\\\\\\\\\\":\\\\\\\\\\\\\\\"0\\\\\\\\\\\\\\\"," \
               "\\\\\\\\\\\\\\\"lastItemIndex\\\\\\\\\\\\\\\":\\\\\\\\\\\\\\\"0\\\\\\\\\\\\\\\"," \
               "\\\\\\\\\\\\\\\"pageKey\\\\\\\\\\\\\\\":\\\\\\\\\\\\\\\"LOGICSHOW_LOGICTV_DEFAULT\\\\\\\\\\\\\\\"," \
               "\\\\\\\\\\\\\\\"dataSourceType\\\\\\\\\\\\\\\":\\\\\\\\\\\\\\\"episode\\\\\\\\\\\\\\\"," \
               "\\\\\\\\\\\\\\\"group\\\\\\\\\\\\\\\":\\\\\\\\\\\\\\\"0\\\\\\\\\\\\\\\"," \
               "\\\\\\\\\\\\\\\"itemStartStage\\\\\\\\\\\\\\\":%d," \
               "\\\\\\\\\\\\\\\"itemEndStage\\\\\\\\\\\\\\\":%d}\\\\\\\"," \
               "\\\\\\\"videoId\\\\\\\":\\\\\\\"%s\\\\\\\"," \
               "\\\\\\\"showId\\\\\\\":\\\\\\\"%s\\\\\\\"}\\\",\\\"system_info\\\":\\\"{" \
               "\\\\\\\"os\\\\\\\":\\\\\\\"pc\\\\\\\",\\\\\\\"device\\\\\\\":\\\\\\\"pc\\\\\\\"," \
               "\\\\\\\"ver\\\\\\\":\\\\\\\"1.0.0\\\\\\\",\\\\\\\"appPackageKey\\\\\\\":\\\\\\\"pcweb\\\\\\\"," \
               "\\\\\\\"appPackageId\\\\\\\":\\\\\\\"pcweb\\\\\\\"}\\\"}\"" % (
               start_stage, end_stage, video_id, show_id)

        datetime = math.ceil(time.time() * 1000)
        sign = self.get_sign(datetime, data, self.token, self.appKey)
        param = 'jsv=2.6.2&appKey=24679788&t={}&sign={}&api=mtop.youku.columbus.gateway.new.execute&type=originaljson&v' \
                '=1.0&ecode=1&dataType=json&data={}'.format(datetime, sign, urllib.parse.quote(json.loads(data)))
        header = {
            'Cookie': '_m_h5_tk={}; _m_h5_tk_enc={};'.format(self._m_h5_tk, self._m_h5_tk_enc)
        }
        url = 'https://acs.youku.com/h5/mtop.youku.columbus.gateway.new.execute/1.0/?{}'.format(param)

        response = requests.get(url=url, headers=header)
        result = json.loads(response.text)
        info_list = result['data']['2019030100']['data']['nodes']
        video_list = []
        for item in info_list:
            # spm_index = 30
            # if item['data']['stage'] % 30 > 0:
            #     spm_index = item['data']['stage'] % 30
            video_list.append({
                'title': item['data']['stage'],
                'imageUrl': item['data']['img'],
                'url': 'https://v.youku.com/v_show/id_{}.html?s={}'.format(item['data']['action']['value'],
                                                                           item['data']['action']['extra']['showId'])
                # 'url': 'https://v.youku.com/v_show/id_{}.html?spm=a2hbt.13141534.1_3.{}&s={}'.format(item['data']['action']['value'], spm_index, item['data']['action']['extra']['showId'])
            })
        return video_list

    def get_sign(self, datetime, data, token, appKey=24679788):
        text = "node {} {} {} {} {}".format(youKu_sign_path, datetime, data, token, appKey)
        p = subprocess.run(text, shell=True, stdout=subprocess.PIPE)
        return p.stdout.decode("utf-8").replace('\n', '')

    def youku_sign(self, t, data, token):
        appKey = '24679788'  # 固定值
        '''token值在cookie中'''
        sign = token + '&' + t + '&' + appKey + '&' + data
        md = md5()
        md.update(sign.encode('UTF-8'))
        sign = md.hexdigest()
        return sign

    def m3u8_url(self, video_id, videoId, show_id):
        url = "https://acs.youku.com/h5/mtop.youku.play.ups.appinfo.get/1.1/"

        # t = str(int(time.time() * 1000))
        t = '1662362817046'
        emb = base64.b64encode(("%swww.youku.com/" % videoId).encode('utf-8')).decode('utf-8')
        # emb = ''
        params_data = r'''{"steal_params":"{\"ccode\":\"0502\",\"client_ip\":\"192.168.1.1\",\"utid\":\"%s\",\"client_ts\":%s,\"version\":\"2.1.69\",\"ckey\":\"DIl58SLFxFNndSV1GFNnMQVYkx1PP5tKe1siZu/86PR1u/Wh1Ptd+WOZsHHWxysSfAOhNJpdVWsdVJNsfJ8Sxd8WKVvNfAS8aS8fAOzYARzPyPc3JvtnPHjTdKfESTdnuTW6ZPvk2pNDh4uFzotgdMEFkzQ5wZVXl2Pf1/Y6hLK0OnCNxBj3+nb0v72gZ6b0td+WOZsHHWxysSo/0y9D2K42SaB8Y/+aD2K42SaB8Y/+ahU+WOZsHcrxysooUeND\"}","biz_params":"{\"vid\":\"%s\",\"play_ability\":16782592,\"current_showid\":\"%s\",\"preferClarity\":99,\"extag\":\"EXT-X-PRIVINF\",\"master_m3u8\":1,\"media_type\":\"standard,subtitle\",\"app_ver\":\"2.1.69\",\"h265\":1}","ad_params":"{\"vs\":\"1.0\",\"pver\":\"2.1.69\",\"sver\":\"2.0\",\"site\":1,\"aw\":\"w\",\"fu\":0,\"d\":\"0\",\"bt\":\"pc\",\"os\":\"win\",\"osv\":\"10\",\"dq\":\"auto\",\"atm\":\"\",\"partnerid\":\"null\",\"wintype\":\"interior\",\"isvert\":0,\"vip\":1,\"emb\":\"%s\",\"p\":1,\"rst\":\"mp4\",\"needbf\":2,\"avs\":\"1.0\"}"}''' % (
        self.cna, t[:10], video_id, show_id, emb)
        sign = self.youku_sign(t, params_data, self.token)
        # sign = self.youku_sign(t, params_data, 'f652db9443d8cea26d9642e417f1dd85')

        params = {
            "jsv": "2.5.8",
            "appKey": "24679788",
            "t": t,
            "sign": sign,
            "api": "mtop.youku.play.ups.appinfo.get",
            "v": "1.1",
            "timeout": "20000",
            "YKPid": "20160317PLF000211",
            "YKLoginRequest": "true",
            "AntiFlood": "true",
            "AntiCreep": "true",
            "type": "jsonp",
            "dataType": "jsonp",
            "callback": "mtopjsonp1",
            "data": params_data,
        }

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cookie": '_m_h5_tk={}; _m_h5_tk_enc={};'.format(self._m_h5_tk, self._m_h5_tk_enc),
            "Host": "acs.youku.com",
            "Referer": "https://v.youku.com/v_show/id_XNTA1MTYwMzU0OA==.html?spm=a2h0c.8166622.PhoneSokuUgc_3.dscreenshot",
            "Sec-Fetch-Dest": "script",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }

        resp = requests.get(url=url, params=params, headers=headers)
        result = resp.text
        # print(result)
        data = json.loads(result[12:-1])
        # print(data)
        ret = data["ret"]
        video_lists = []
        if ret == ["SUCCESS::调用成功"]:
            stream = data["data"]["data"]["stream"]
            title = data["data"]["data"]["video"]["title"]
            print("解析成功:")
            for video in stream:
                m3u8_url = video["m3u8_url"]
                width = video["width"]
                height = video["height"]
                size = video["size"]
                size = '{:.1f}'.format(float(size) / 1048576)
                video_lists.append([size, width, height, title, m3u8_url])
                print(f">>>  {title} 分辨率:{width}x{height} 视频大小:{size}M \tm3u8播放地址:{m3u8_url}")

            # video_lists.sort(key=self.takeOne)
            # for video_list in video_lists:
            #     print(f">>>  {title} 分辨率:{video_list[1]}x{video_list[2]} 视频大小:{video_list[0]}M \tm3u8播放地址:{video_list[4]}")
            # self.play(video_lists[-1][4])    # 选择播放列表最后一个视频（经过sort排序后，最后一个即为清晰度最高的一个）
        elif ret == ["FAIL_SYS_ILLEGAL_ACCESS::非法请求"]:
            print("请求参数错误")
        elif ret == ["FAIL_SYS_TOKEN_EXOIRED::令牌过期"]:
            print("Cookie过期")
        else:
            print(ret[0])

    def get_download_list(self):
        url = 'https://valipl10.cp31.ott.cibntv.net/65731D34B763671755732370E/03000900006299ACCC8BB780000000726D6C89-58A4-4C09-BEF6-3D5C3CBC1A73-11-54247245.m3u8?ccode=0502&duration=2721&expire=18000&psid=0234e02b87701ed20969e4b8acf2337941346&ups_client_netip=2471915a&ups_ts=1661926416&ups_userid=999830345&utid=gAXaGUK%2B3w8CAXAUXTWZcdbb&vid=XNTg1MjcwNjQwNA%3D%3D&vkey=Bd4e75e70fbed600cf783b52c26ee85ed&s=bbfdcd5525264a2eb8fd&iv=1&eo=0&t=8cb8d34768c724b&cug=1&fms=ce0126c0343c302c&tr=2706&le=958e1be54f19b23c5c4541e95c6e2412&ckt=5&m_onoff=0&rid=20000000CD33CFD64E89FBA1E4026417683056A402000000&type=mp4hd3v3&bc=2&dre=u151&si=573&dst=1&sm=1&operate_type=1&hotvt=1'
        res = requests.get(url)
        download_url_list = re.findall('\nhttp(.*)\n', res.content.decode("utf-8"))
        for index in range(len(download_url_list)):
            download_url_list[index] = 'http' + download_url_list[index]
        return download_url_list


y = Youku()
if __name__ == '__main__':
    # 电视剧
    # url = 'https://v.youku.com/v_show/id_XNTg4NDExNDE2OA==.html?s=efbfbd1e204e0fefbfbd'
    # 电影
    # url = 'https://v.youku.com/v_show/id_XMjk3NjA4Mzg4MA==.html?spm=a2ha1.14919748_WEBHOME_GRAY.drawer5.d_zj1_4&s=e0010534bb4711e5b2ad&scm=20140719.rcmd.7182.show_e0010534bb4711e5b2ad'
    # 综艺
    # url = 'https://v.youku.com/v_show/id_XNTg4NDExMzIxNg==.html?scm=20140719.manual.15319.video_XNTg4NDExMzIxNg%3D%3D&spm=a2ha1.14919748_WEBHOME_GRAY.drawer2.d_zj1_3'
    # info = y.get_video_info(url)
    # print(info)

    # url = 'https://valipl10.cp31.ott.cibntv.net/67756D6080932713CFC02204E/030009000062A006366821FFC9AE75266AAAAD-0EE4-47D8-932E-336DBF7DB14D-00008.ts?ccode=0502&duration=1681&expire=18000&psid=eeb146567d3865bf92c12af8a551853d41346&ups_client_netip=2471915a&ups_ts=1661925477&ups_userid=999830345&utid=gAXaGUK%2B3w8CAXAUXTWZcdbb&vid=XNTE5ODA1NDkyNA%3D%3D&s=cc17b508962411de83b1&iv=1&eo=0&t=87417b3ca3e2430&cug=1&fms=309ca5c10457cbfe&tr=1681&le=2de1b7a525f51593c14dba097ca95e74&ckt=5&m_onoff=0&rid=2000000059F4F950185280A4CE955E72D76E72B402000000&type=mp4hd3v3&bc=2&dre=u151&si=573&dst=1&sm=1&operate_type=1&vkey=B71088f3031d4e53375245dfa23bd7e7e'
    # url = 'https://valipl10.cp31.ott.cibntv.net/65731D34B763671755732370E/03000900006299ACCC8BB780000000726D6C89-58A4-4C09-BEF6-3D5C3CBC1A73-11-54247245.m3u8?ccode=0502&duration=2721&expire=18000&psid=0234e02b87701ed20969e4b8acf2337941346&ups_client_netip=2471915a&ups_ts=1661926416&ups_userid=999830345&utid=gAXaGUK%2B3w8CAXAUXTWZcdbb&vid=XNTg1MjcwNjQwNA%3D%3D&vkey=Bd4e75e70fbed600cf783b52c26ee85ed&s=bbfdcd5525264a2eb8fd&iv=1&eo=0&t=8cb8d34768c724b&cug=1&fms=ce0126c0343c302c&tr=2706&le=958e1be54f19b23c5c4541e95c6e2412&ckt=5&m_onoff=0&rid=20000000CD33CFD64E89FBA1E4026417683056A402000000&type=mp4hd3v3&bc=2&dre=u151&si=573&dst=1&sm=1&operate_type=1&hotvt=1'
    # res = requests.get(url)
    # video_list = re.findall('\nhttp(.*)\n', res.content.decode("utf-8"))
    # for index in range(len(video_list)):
    #     video_list[index] = 'http' + video_list[index]
    # print(video_list)
    # with open('test.mp4', 'ab') as video:
    #     res = requests.get(url)
    #     video.write(res.content)
    # video.close()

    # y.m3u8_url('XNTE5ODA1NDkyNA==', 'cc17b508962411de83b1')
    # y.m3u8_url('XNTE5ODA1NDkyNA==', '1299513731', '55781')
    # y.m3u8_url('XNTg4NDExMjUyOA==', '1471028132', '316409')
    y.m3u8_url('XNTg4NDExNDE2NA==', '1471028541', '316409')
