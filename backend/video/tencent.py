""""""
import json

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

tencent_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36',
    'Cookie': 'vqq_access_token=CB92B3C04AB6498E0E971BE4D8B17E62; vqq_appid=101483052; vqq_openid=2A643EEE51D87B77946C7CFE3481E097; '
}


class Tencent:
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
        video_key_response = requests.get(url=video_key_url, headers=tencent_headers)
        video_key = json.loads(video_key_response.content[len('QZOutputJson='):-1])
        key = video_key['key']
        video_real_url = '{}{}?vkey={}'.format(url_prefix, filename, key)
        print(video_real_url)
        video_real_response = requests.get(url=video_real_url, headers=headers)
        content = video_real_response.content
        print(content)

    def t(self):
        url = 'https://vd.l.qq.com/proxyhttp'
        body = {"buid":"vinfoad","adparam":"pf=in&ad_type=LD%7CKB%7CPVL&pf_ex=pc&url=https%3A%2F%2Fv.qq.com%2Fx%2Fcover%2Fmzc0020020cyvqh%2Fo00415fhnh5.html&refer=https%3A%2F%2Fv.qq.com%2F&ty=web&plugin=1.0.0&v=3.5.57&coverid=mzc0020020cyvqh&vid=o00415fhnh5&pt=&flowid=623ad73120a1dcd1f0f0a97a86651406_10201&vptag=&pu=-1&chid=0&adaptor=2&dtype=1&live=0&resp_type=json&guid=6a86c1085fecc298fc5c2f14aa73a295&req_type=1&from=0&appversion=1.0.171&uid=424467340&tkn=S5MvfAi9cfiHThFvxjrDBw..&lt=qq&platform=10201&opid=2A643EEE51D87B77946C7CFE3481E097&atkn=CB92B3C04AB6498E0E971BE4D8B17E62&appid=101483052&tpid=2&rfid=291edee9ab286866c4933d88fc54dde5_1642489760","vinfoparam":"spsrt=1&charge=1&defaultfmt=auto&otype=ojson&guid=6a86c1085fecc298fc5c2f14aa73a295&flowid=623ad73120a1dcd1f0f0a97a86651406_10201&platform=10201&sdtfrom=v1010&defnpayver=1&appVer=3.5.57&host=v.qq.com&ehost=https%3A%2F%2Fv.qq.com%2Fx%2Fcover%2Fmzc0020020cyvqh%2Fo00415fhnh5.html&refer=v.qq.com&sphttps=1&tm=1642491449&spwm=4&logintoken=%7B%22main_login%22%3A%22qq%22%2C%22openid%22%3A%222A643EEE51D87B77946C7CFE3481E097%22%2C%22appid%22%3A%22101483052%22%2C%22access_token%22%3A%22CB92B3C04AB6498E0E971BE4D8B17E62%22%2C%22vuserid%22%3A%22424467340%22%2C%22vusession%22%3A%22S5MvfAi9cfiHThFvxjrDBw..%22%7D&vid=o00415fhnh5&defn=fhd&fhdswitch=0&show1080p=1&isHLS=1&dtype=3&sphls=2&spgzip=1&dlver=2&drm=32&hdcp=1&spau=1&spaudio=15&defsrc=2&encryptVer=9.1&cKey=JOVOW9a6AkF7xJEItZs_lpJX5WB4a2CdS8kEpbFiVaqtHEZQ1c_W6myJ8hQCnmDFHMV4E8uTbzvK2vPBr-xE-uhvZyEMY131vUh1H4pgCXe2Op8F_DerfPItmUhl5793oHwrEERQEN-fluNDEH6IC8EOljLQ2VfW2sTdospNPlD9535CNT9iSo3cLRH93ogtX_OJeYNVWrDYS8b5t1pjAAuGkoYGNScB_8lMahr0SD1lJfkplb5LtU1mpdrzcMbY1XniNzyOKljQ8AICTCwy2R1qtnIc3xhUGd_iUVDdFfA62IA6f9OFm0T6Hj92NS6XQ6XmEfIUBlrveoG1jSsl2hxBSAUFBQUFNR71zA&fp2p=1&spadseg=3"}
        response = requests.post(url=url, json=body, headers=headers)
        print(response.text)

# 根据电视剧编号下载视频
    # def get(self, video_id):
    #     print(1234)
    # https://v.qq.com/x/cover/vmpd6t5ipaw0xvr/m003318s4ru.html
    # http://vv.video.qq.com/getinfo?otype=json&appver=3.2.19.333&platform=4100201&defnpayver=1&defn=shd&vid=m003318s4ru
    # http://vv.video.qq.com/getkey?otype=json&platform=11&format=10201&vid=m003318s4ru&filename=r0035yqfdb9.p201.1.mp4&appver=3.2.19.333
    # http://36.155.24.151/vlive.qqvideo.tc.qq.com/AVAWp0JMH_VzoIlhMhr4XUTeJmkki75i-LXZ-6YFiA-o/uwMROfz2r5zAoaQXGdGnC2dfKb2qtt4sTnwxCNWPphaQoC-Y/r0035yqfdb9.p201.1.mp4?vkey=060C3F582FD6807FA3D90B16A42FD178E1D6DB89F4FFB735FB7C16282A5AE311FDD2D710F470A2F7074459689F45A536BCAA20D099BFF90F37F68F3F81627F5D0BB6C9A4F17CBB32C3744A531FB07DA05706D51F2E291AE85628F22EA68541515CF2286751522AC5C3EA99F44399B919290B78621BB7949F
    #
    #
    #
    # https://v.qq.com/x/cover/mzc00200i4a0cg2.html
    # http://vv.video.qq.com/getinfo?otype=json&appver=3.2.19.333&platform=4100201&defnpayver=1&defn=shd&vid=v0041065f7h
    # http://vv.video.qq.com/getkey?otype=json&platform=11&format=10217&vid=v0041065f7h&filename=gzc_1000102_0b53p4absaaacyaga5wamfq4a76ddfzqahka.f10217.mp4&appver=3.2.19.333
    # http://223.113.137.141/vlive.qqvideo.tc.qq.com/AbfR_PvX-u4gwUTY9SMyr5lJfImAxIU-NrvhtBd1HUqk/uwMROfz2r57AoaQXGdGnC2deKY1IscDfyxf57MohrStqeuf2/gzc_1000102_0b53p4absaaacyaga5wamfq4a76ddfzqahka.f10217.mp4?vkey=E1D9709D65B236F18E50D9016B24FB234F564C63A6DAD336F2E8E396D0FA0AD3AB113453AEC34B90D04927F281887868983A6EA436A277EE0184A96B67589DAD7AE6ABFEC40E7A2D5C7F1E1FA4DA70E81C9C21DC451C23E789D7AD443260E9CF24A981BC21546280CEEAFD8202E8596E4F0332F2430F50DA


t = Tencent()
t.t()
