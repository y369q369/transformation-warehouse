""""""
import requests
import parsel
import re

'''
    目标网址   ->    腾讯视频 ：https://v.qq.com/
    功能      ->    根据 地址 下载视频
'''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36',
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

    # 根据电视剧编号下载视频
    def get(self, video_id):
        print(1234)
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

