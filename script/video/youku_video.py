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
    url = 'https://valipl10.cp31.ott.cibntv.net/65731D34B763671755732370E/03000900006299ACCC8BB780000000726D6C89-58A4-4C09-BEF6-3D5C3CBC1A73-11-54247245.m3u8?ccode=0502&duration=2721&expire=18000&psid=0234e02b87701ed20969e4b8acf2337941346&ups_client_netip=2471915a&ups_ts=1661926416&ups_userid=999830345&utid=gAXaGUK%2B3w8CAXAUXTWZcdbb&vid=XNTg1MjcwNjQwNA%3D%3D&vkey=Bd4e75e70fbed600cf783b52c26ee85ed&s=bbfdcd5525264a2eb8fd&iv=1&eo=0&t=8cb8d34768c724b&cug=1&fms=ce0126c0343c302c&tr=2706&le=958e1be54f19b23c5c4541e95c6e2412&ckt=5&m_onoff=0&rid=20000000CD33CFD64E89FBA1E4026417683056A402000000&type=mp4hd3v3&bc=2&dre=u151&si=573&dst=1&sm=1&operate_type=1&hotvt=1'
    res = requests.get(url)
    video_list = re.findall('\nhttp(.*)\n', res.content.decode("utf-8"))
    for index in range(len(video_list)):
        video_list[index] = 'http' + video_list[index]
    print(video_list)
    # with open('test.mp4', 'ab') as video:
    #     res = requests.get(url)
    #     video.write(res.content)
    # video.close()
