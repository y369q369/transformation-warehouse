# 建立属于自己的开放代理IP池
import json
import os

import requests
from fake_useragent import UserAgent
from lxml import etree

headers = {'User-Agent': UserAgent().random}
# 导出文件
export_file = 'ipPool.json'
# 可用代理集合
available_proxy = {
    'verification': [],
    'temporary': []
}
# 代理列表
proxy_list = []
next_proxy_index = 0


# 生成代理：代理池 + 本机 顺序循环获取
def generate_proxy():
    global available_proxy
    global proxy_list
    global next_proxy_index
    if len(proxy_list) == 0:
        proxy_list.append(None)
        read_proxy()
        if len(available_proxy['verification']) > 0:
            for proxy in available_proxy['verification']:
                proxy_list.append({
                    'http': 'http://{}'.format(proxy),
                    'https': 'https://{}'.format(proxy),
                })
    else:
        if next_proxy_index + 1 >= len(proxy_list):
            next_proxy_index = 0
        else:
            next_proxy_index = next_proxy_index + 1
    return proxy_list[next_proxy_index]


def read_proxy():
    global available_proxy
    if os.path.exists(export_file):
        with open(export_file, 'r', encoding='utf-8') as load_f:
            available_proxy = json.load(load_f)
            print(available_proxy)


def save_proxy():
    with open(export_file, 'w', encoding='utf-8') as target_file:
        json.dump(available_proxy, target_file, indent=4, ensure_ascii=False)
        target_file.close()


def test_proxy(proxy):
    """
        测试代理IP是否可用
    """
    proxies = {
        'http': 'http://{}'.format(proxy),
        'https': 'https://{}'.format(proxy),
    }
    try:
        resp = requests.get(url='http://httpbin.org/get', proxies=proxies, headers=headers, timeout=5)
        # 获取 状态码为200
        if resp.status_code == 200:
            print(proxy, '\033[31m可用\033[0m')
            available_proxy['temporary'].append(proxy)
        else:
            print(proxy, '不可用')
    except Exception as e:
        print(proxy, '不可用')


def get_89ip_proxy():
    """
        89ip
    """
    url = 'https://www.89ip.cn/index_{}.html'
    for i in range(1, 10):
        html = requests.get(url=url.format(i), headers=headers).text
        elemt = etree.HTML(html)
        ips_list = elemt.xpath('//table/tbody/tr/td[1]/text()')
        ports_list = elemt.xpath('//table/tbody/tr/td[2]/text()')

        for ip, port in zip(ips_list, ports_list):
            # 拼接ip与port
            proxy = ip.strip() + ":" + port.strip()
            test_proxy(proxy)


if __name__ == '__main__':
    # read_proxy()
    # get_89ip_proxy()
    # save_proxy()
    # test_proxy('8.140.52.240:8945')
    for i in range(30):
        print(generate_proxy())
