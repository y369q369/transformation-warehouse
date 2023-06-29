import requests
from fake_useragent import UserAgent

url = 'http://httpbin.org/get'
headers = {'User-Agent': UserAgent().random}

# 参数类型
# proxies
# proxies = {'协议': '协议://IP:端口号'}
proxies = {
    'http': 'http://{}'.format('8.140.52.240:8945'),
    'https': 'https://{}'.format('8.140.52.240:8945'),
}

html = requests.get(url=url, headers=headers, proxies=proxies, timeout=5).text
print(html)
"""
{
  "args": {},
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Host": "httpbin.org",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
    "X-Amzn-Trace-Id": "Root=1-5ff7a71d-10b181340f8dc04f7514dfba"
  },
  "origin": "8.129.28.247",
  "url": "http://httpbin.org/get"
}
"""
