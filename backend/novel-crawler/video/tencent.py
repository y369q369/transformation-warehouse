import requests
import parsel

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36',
}
url = 'https://v.qq.com/x/cover/mzc00200prv7r23.html'

response = requests.get(url=url, headers=headers)
headers = response.headers
text = response.text
selector = parsel.Selector(response.text)
s = selector.css('head script')
for m in s:
    template = m.css('::attr(r-notemplate)').get()
    type = m.css('::attr(type)').get()
    if template == 'true' and type == 'text/javascript':
        o = m.css('::text').get()
        print(o)
t = selector.attrib

content = response.content
# print(response.text)
