# coding: utf-8
import requests, time, json, subprocess, re


class TXSP:
    def __init__(self, cookie):
        try:
            self.cookie = self.auth_refresh()
        except:
            self.cookie = cookie

    def auth_refresh(self):
        url = 'https://access.video.qq.com/user/auth_refresh'
        params = {
            "vappid": "替换这里",   # 我的"1105**94"
            "vsecret": "替换这里",  # 我的 fdf61a6be0aad57132bc5c****ac30145b6cd2c1470b0cfe
            "type": "qq",
            "g_tk": "",
            "g_vstk": "替换这里",       # 我的 2034***571
            "g_actk": "替换这里",       # 16374***17
            "callback": "替换这里",     # jQuery1910682881450***4196_1625677067741
            "_": str(int(time.time() * 1000)),
        }
        with open("cookie.txt", "r") as fp:
            get_cookie = fp.read()
        headers = {
            "authority": "access.video.qq.com",
            "method": "GET",
            "path": "/user/auth_refresh",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": get_cookie,
            "referer": "https://v.qq.com/x/page/e3257kqj1la.html",
            "sec-fetch-dest": "script",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        resp = requests.get(url=url, params=params, headers=headers)
        text = resp.text
        text_temp = re.compile("(\{.*?\})")
        data = text_temp.findall(text)[0]
        info = json.loads(data)
        set_cookie = "main_login=qq; vqq_access_token={0}; vqq_appid=替换这里; vqq_openid=替换这里; vqq_vuserid={1}; vqq_vusession={2}; vqq_next_refresh_time={3};".format(
            info["access_token"], info["vuserid"], info["vusession"], info["next_refresh_time"])
        with open("cookie.txt", "w", encoding="utf-8") as f:
            f.write(set_cookie)
        return set_cookie

    # get_ckey()这个方法用到了 当前程序所在文件夹下的  txsp.js  该js文件调用了 ckey.wasm 密钥
    def get_ckey(self, vid):
        # refresh_js(vid)
        guid = ''   # 我的是 cb68b765165403f7***e102cfba61430
        text = "node tx.js {0} {1}".format(vid, guid)
        p = subprocess.run(text, shell=True, stdout=subprocess.PIPE)
        result = p.stdout.decode("utf-8")
        # print(result)
        return result

    def user_info(self, cookie):
        try:
            main_login = re.findall("main_login=(.*?);", cookie)[0]
            openid = re.findall("openid=(.*?);", cookie)[0]
            appid = re.findall("appid=(.*?);", cookie)[0]
            access_token = re.findall("access_token=(.*?);", cookie)[0]
            vuserid = re.findall("vuserid=(.*?);", cookie)[0]
            vusession = re.findall("vusession=(.*?);", cookie)[0]
            return {"main_login": main_login, "openid": openid, "appid": appid, "access_token": access_token,
                    "vuserid": vuserid, "vusession": vusession}
        except:
            return {"main_login": "", "openid": "", "appid": "", "access_token": "", "vuserid": "", "vusession": ""}

    def get_m3u8(self, video_url, vid, ckey):
        url = "https://vd.l.qq.com/proxyhttp"
        headers = {
            "authority": "vd.l.qq.com",
            "method": "POST",
            "path": "/proxyhttp",
            "scheme": "https",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-length": "2123",
            "content-type": "text/plain",
            "cookie": self.cookie,
            "origin": "https://v.qq.com",
            "referer": video_url,
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        t = str(int(time.time()))
        userinfo = self.user_info(self.cookie)
        # print(userinfo)
        if not userinfo["main_login"]:
            print("请重新尝试设置 cookie，只能解析出 高清 视频")
        #cb68b765165403f7c*****cfba61430   6ee0319a367079f6c****d166f0d97d_10201
        vinfoparam = 'spsrt=1&charge=0&defaultfmt=auto&otype=ojson&guid=&flowid=&platform=10201&sdtfrom=v1010&defnpayver=1&appVer=3.5.57&host=v.qq.com&ehost=%s&refer=v.qq.com&sphttps=1&tm=%s&spwm=4&logintoken={"main_login":"%s","openid":"%s","appid":"%s","access_token":"%s","vuserid":"%s","vusession":"%s"}&unid=2798fc67442611eb89cd6c92bf48bcb2&vid=%s&defn=fhd&fhdswitch=0&show1080p=1&isHLS=1&dtype=3&sphls=2&spgzip=1&dlver=2&drm=32&hdcp=0&spau=1&spaudio=15&defsrc=2&encryptVer=9.1&cKey=%s&fp2p=1&spadseg=3' % (
            video_url, t, userinfo["main_login"], userinfo["openid"], userinfo["appid"], userinfo["access_token"],
            userinfo["vuserid"], userinfo["vusession"], vid, ckey.replace("\n", "&"))
        data = {
            "adparam": "pf=in&ad_type=LD|KB|PVL&pf_ex=pc&url=%s" % video_url,
            "buid": "vinfoad",
            "vinfoparam": vinfoparam,
        }
        resp = requests.post(url=url, json=data, headers=headers)
        data = json.loads(resp.content.decode("utf-8"))
        vinfo = data["vinfo"]
        vinfo = json.loads(vinfo)
        video = vinfo["vl"]["vi"][0]
        title = video["ti"]
        video_url = video["ul"]["ui"][0]["url"]  # json数据中共四个url,这里选第一个，但实测 四个基本是一样的清晰度的。 第四个无法播放！！！ 昨天都还可以，今天凉了，不知原因
        print("解析成功 >>> 标题：{0}\tm3u8播放地址：{1}".format(title, video_url))
        return video_url

    def get_vid(self, url):
        vid = re.compile("https://.*/(.*?).html")
        vid = vid.findall(url)
        if vid:
            return vid[0]
        else:
            print("网址解析失败：请将视频完整链接复制后再粘贴！")
            return "-1"

    def play(self, x):
        text = 'ffplay -loglevel repeat+level+warning -i "%s"' % x
        subprocess.call(text, shell=True)

    def page_parser(self, url):
        headers = {
            "authority": "v.qq.com",
            "method": "GET",
            "path": url.replace("https://v.qq.com", ""),
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            "cookie": self.cookie,
            "referer": "https://v.qq.com/",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        resp = requests.get(url=url, headers=headers)
        # <link rel="canonical"  />     若电影有不同语言版本，网址可能不显示 真实 vid 需解析网页
        html = resp.content.decode("utf-8")
        callback_url = re.compile('<link rel="canonical" href="(.*?)" />', re.M | re.S)
        rel_url = callback_url.findall(html)
        if rel_url:
            return rel_url[0]
        else:
            return url

    def start(self):
        video_url = input("请将腾讯视频播放链接粘贴到这里：\n")
        rel_url = self.page_parser(video_url)
        vid = self.get_vid(rel_url)
        m3u8_url = self.get_m3u8(rel_url, vid, self.get_ckey(vid))
        self.play(m3u8_url)


if __name__ == '__main__':
    cookie = input("请先设置腾讯视频cookie: \n")
    txsp = TXSP(cookie)
    while True:
        txsp.start()