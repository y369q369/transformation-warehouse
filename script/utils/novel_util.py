import json
import os
import random
from multiprocessing import Process, Manager

import requests
import urllib3
from fake_useragent import UserAgent

ip_pool_file = 'ipPool.json'
request_header = {'User-Agent': UserAgent().random}


def get_proxies():
    """
        获取ip代理池
    """
    ip_pool = [None]
    if os.path.exists(ip_pool_file):
        with open(ip_pool_file, 'r', encoding='utf-8') as load_f:
            available_proxy = json.load(load_f)
            if len(available_proxy['verification']) > 0:
                for proxy in available_proxy['verification']:
                    ip_pool.append({
                        'http': 'http://{}'.format(proxy),
                        'https': 'https://{}'.format(proxy),
                    })
    return ip_pool


ip_pool_proxies = get_proxies()


def save_file(direction, file_name, detail_list):
    """
        保存文件

        Parameters
        -----------
        direction
            目录
        file_name
          文件名
        detail_list
          章节内容列表
    """
    if not os.path.exists(direction):
        os.makedirs(direction)
    file = direction + "/" + file_name + ".txt"
    with open(file, 'w', encoding='utf-8') as novel:
        title = "{} \n\n\n\n".format(file_name)
        novel.write(title)
        for detail in detail_list:
            novel.write(detail)
        novel.close()


def split_process_download(process_num, chapter_list, encoding='gbk', headers=request_header):
    """
        多线程获取小说章节内容

        Parameters
        -----------
        process_num
            进程数量
        chapter_list
          下载章节列表
        encoding
          编码格式
        headers
            请求头
    """
    process_list = []
    piece_size = len(chapter_list) // process_num
    manager = Manager()
    manager_list = manager.list()
    if len(chapter_list) % process_num > 0:
        piece_size = piece_size + 1
    for i in range(process_num):
        if i == process_num - 1:
            temp_chapter_list = chapter_list[i * piece_size:]
        else:
            temp_chapter_list = chapter_list[i * piece_size:(i + 1) * piece_size]
        manager_list.append([])
        temp_process = Process(target=batch_download_content,
                               args=(manager_list, i, temp_chapter_list, encoding, headers))
        process_list.append(temp_process)
        temp_process.start()

    for item in process_list:
        item.join()
    print("多线程获取小说章节结束")
    content_list = []
    for item in manager_list:
        content_list.extend(item)
    return content_list


def batch_download_content(manager_list, index, chapter_list, encoding='gbk', headers=request_header):
    """
    获取小说章节内容

    Parameters
    -----------
    manager_list
      进程通信列表
    index
      列表索引
    chapter_list
      下载章节列表
    encoding
      网页编码
    headers
        请求头
"""
    temp_content_list = []
    for chapter in chapter_list:
        print("{} 开始获取".format(chapter['name']))
        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            res = requests.get(chapter['url'], headers=headers, proxies=random.choice(ip_pool_proxies), verify=False,
                               timeout=10)
            res.encoding = encoding
            temp_content_list.append({
                'name': chapter['name'],
                'text': res.text
            })
        except:
            print("\033[31;48m {}   {} 章节获取异常 \033[0m".format(chapter['name'], chapter['url']))
            # traceback.print_exc()
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            res = requests.get(chapter['url'], headers=headers, proxies=random.choice(ip_pool_proxies), verify=False,
                               timeout=30)
            res.encoding = encoding
            temp_content_list.append({
                'name': chapter['name'],
                'text': res.text
            })
    manager_list[index] = temp_content_list
