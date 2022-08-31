import json
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


class Youku:
    # 获取电视剧每集视频的编号
    def get_video_info(self, url):
        response = requests.get(url=url, headers=headers)
        selector = parsel.Selector(response.text)
        title = selector.css(".thesis-wrap a::text").get()
        page_size = len(selector.css(".top-wrap a"))
        print(title)
        print(page_size)

    def get_video_list(self, url):
        headers[
            'Cookie'] = 'ysuid=16382606358438Gu; _m_h5_tk=b9705532cc90afc18db27cc79429d908_1661543843164; _m_h5_tk_enc=d192bcb713d1a587ec3188b91e2226bb;'
        response = requests.get(url=url, headers=headers)
        print(response.text)

    def get_sign(self):
        text = "node {} {} {} {}".format(tencent_tx_path, vid, self.guid, tencent_ckey_path)
        p = subprocess.run(text, shell=True, stdout=subprocess.PIPE)
        return p.stdout.decode("utf-8")


y = Youku()
if __name__ == '__main__':
    itemStartStage = 31
    itemEndStage = 60
    videoId = 'XNDIzMjcyNjc0MA=='
    showId = 'a30c20bd26244a46b191'

    data = "{\"ms_codes\":\"2019030100\",\"params\":\"{\\\"biz\\\":true,\\\"scene\\\":\\\"component\\\"," \
           "\\\"componentVersion\\\":\\\"3\\\",\\\"ip\\\":\\\"112.20.94.90\\\",\\\"debug\\\":0," \
           "\\\"utdid\\\":\\\"gAXaGUK+3w8CAXAUXTWZcdbb\\\",\\\"userId\\\":\\\"\\\",\\\"platform\\\":\\\"pc\\\"," \
           "\\\"gray\\\":0,\\\"nextSession\\\":\\\"{\\\\\\\"componentIndex\\\\\\\":\\\\\\\"3\\\\\\\"," \
           "\\\\\\\"componentId\\\\\\\":\\\\\\\"61518\\\\\\\",\\\\\\\"level\\\\\\\":\\\\\\\"2\\\\\\\"," \
           "\\\\\\\"itemPageNo\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"lastItemIndex\\\\\\\":\\\\\\\"0\\\\\\\"," \
           "\\\\\\\"pageKey\\\\\\\":\\\\\\\"LOGICSHOW_LOGICTV_DEFAULT\\\\\\\"," \
           "\\\\\\\"dataSourceType\\\\\\\":\\\\\\\"episode\\\\\\\",\\\\\\\"group\\\\\\\":\\\\\\\"0\\\\\\\"," \
           "\\\\\\\"itemStartStage\\\\\\\":%d,\\\\\\\"itemEndStage\\\\\\\":%d}\\\"," \
           "\\\"videoId\\\":\\\"%s\\\",\\\"showId\\\":\\\"%s\\\"}\"," \
           "\"system_info\":\"{\\\"os\\\":\\\"pc\\\",\\\"device\\\":\\\"pc\\\",\\\"ver\\\":\\\"1.0.0\\\"," \
           "\\\"appPackageKey\\\":\\\"pcweb\\\",\\\"appPackageId\\\":\\\"pcweb\\\"}\"}" % (
           itemStartStage, itemEndStage, videoId, showId)

    sign = 'de443a653d4676f1269dfc1aef8cb74d'
    t = '1661572822708'
    # t = int(round(time.time() * 1000))

    param = 'jsv=2.6.2&appKey=24679788&t={}&sign={}&api=mtop.youku.columbus.gateway.new.execute&type=originaljson&v' \
            '=1.0&ecode=1&dataType=json&data={}'.format(t, sign, urllib.parse.quote(data))

    headers[
        'Cookie'] = 'ysuid=16382606358438Gu; _m_h5_tk=0c0f262c67368be94abda72f2e749e9e_1661576774302; _m_h5_tk_enc=6f3e4a62b6354c4a82e05b336c221c90;'

    # url = 'https://acs.youku.com/h5/mtop.youku.columbus.gateway.new.execute/1.0/?{}'.format(param)
    # response = requests.get(url, headers=headers)
    # print(response.text)
    # print(response.url)

    headers[
        'Cookie'] = 'ysuid=16382606358438Gu; _m_h5_tk=585b1bd1629fa765a7fbfa6f829d1b50_1661577718594; _m_h5_tk_enc=670b583961abad4452fa39aef610f266;'

    url = 'https://acs.youku.com/h5/mtop.youku.columbus.gateway.new.execute/1.0/?jsv=2.6.2&appKey=24679788&t=1661573577217&sign=5b5c388627b79ca0d0c09b6da8f9c7e9&api=mtop.youku.columbus.gateway.new.execute&type=originaljson&v=1.0&ecode=1&dataType=json&data=%7B%22ms_codes%22%3A%222019030100%22%2C%22params%22%3A%22%7B%5C%22biz%5C%22%3Atrue%2C%5C%22scene%5C%22%3A%5C%22component%5C%22%2C%5C%22componentVersion%5C%22%3A%5C%223%5C%22%2C%5C%22ip%5C%22%3A%5C%22112.20.94.90%5C%22%2C%5C%22debug%5C%22%3A0%2C%5C%22utdid%5C%22%3A%5C%22gAXaGUK%2B3w8CAXAUXTWZcdbb%5C%22%2C%5C%22userId%5C%22%3A%5C%22%5C%22%2C%5C%22platform%5C%22%3A%5C%22pc%5C%22%2C%5C%22gray%5C%22%3A0%2C%5C%22nextSession%5C%22%3A%5C%22%7B%5C%5C%5C%22componentIndex%5C%5C%5C%22%3A%5C%5C%5C%223%5C%5C%5C%22%2C%5C%5C%5C%22componentId%5C%5C%5C%22%3A%5C%5C%5C%2261518%5C%5C%5C%22%2C%5C%5C%5C%22level%5C%5C%5C%22%3A%5C%5C%5C%222%5C%5C%5C%22%2C%5C%5C%5C%22itemPageNo%5C%5C%5C%22%3A%5C%5C%5C%220%5C%5C%5C%22%2C%5C%5C%5C%22lastItemIndex%5C%5C%5C%22%3A%5C%5C%5C%220%5C%5C%5C%22%2C%5C%5C%5C%22pageKey%5C%5C%5C%22%3A%5C%5C%5C%22LOGICSHOW_LOGICTV_DEFAULT%5C%5C%5C%22%2C%5C%5C%5C%22dataSourceType%5C%5C%5C%22%3A%5C%5C%5C%22episode%5C%5C%5C%22%2C%5C%5C%5C%22group%5C%5C%5C%22%3A%5C%5C%5C%220%5C%5C%5C%22%2C%5C%5C%5C%22itemStartStage%5C%5C%5C%22%3A1%2C%5C%5C%5C%22itemEndStage%5C%5C%5C%22%3A30%7D%5C%22%2C%5C%22videoId%5C%22%3A%5C%22XNTg4NDExNDIyMA%3D%3D%5C%22%2C%5C%22showId%5C%22%3A%5C%22efbfbd1e204e0fefbfbd%5C%22%7D%22%2C%22system_info%22%3A%22%7B%5C%22os%5C%22%3A%5C%22pc%5C%22%2C%5C%22device%5C%22%3A%5C%22pc%5C%22%2C%5C%22ver%5C%22%3A%5C%221.0.0%5C%22%2C%5C%22appPackageKey%5C%22%3A%5C%22pcweb%5C%22%2C%5C%22appPackageId%5C%22%3A%5C%22pcweb%5C%22%7D%22%7D'
    response = requests.get(url, headers=headers)
    print(response.text)
    print(response.url)

    # param = {
    #     'ms_codes': '2019030100',
    #      'params': '{"biz":true,"scene":"component","componentVersion":"3","ip":"112.20.94.90","debug":0,"utdid":"gAXaGUK+3w8CAXAUXTWZcdbb","userId":"","platform":"pc","gray":0,"nextSession":"{\\"componentIndex\\":\\"3\\",\\"componentId\\":\\"61518\\",\\"level\\":\\"2\\",\\"itemPageNo\\":\\"0\\",\\"lastItemIndex\\":\\"0\\",\\"pageKey\\":\\"LOGICSHOW_LOGICTV_DEFAULT\\",\\"dataSourceType\\":\\"episode\\",\\"group\\":\\"0\\",\\"itemStartStage\\":31,\\"itemEndStage\\":60}","videoId":"XNDIzMjcyNjc0MA==","showId":"a30c20bd26244a46b191"}',
    #      'system_info': '{"os":"pc","device":"pc","ver":"1.0.0","appPackageKey":"pcweb","appPackageId":"pcweb"}'
    # }
    # param_str = json.dumps(param, separators=(',',':'))
    # request_param = urllib.parse.quote(param_str)
    # print(param_str)
    # print(request_param)
