""""""
import pprint
import requests
import parsel
import csv
'''
参考：https://blog.csdn.net/m0_48405781/article/details/113055904
1、明确需求:
    爬取豆瓣Top250排行电影信息
        电影名字
        导演、主演
        年份、国家、类型
        评分、评价人数
        电影简介
'''
# csv模块保存数据到Excel： 从页面爬取的文件编码格式为utf8
f = open('F:\豆瓣电影数据.csv', mode='w', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=['电影名字', '参演人员', '上映时间', '拍摄国家', '电影类型',
                                           '电影评分', '评价人数', '电影概述'])

csv_writer.writeheader()    # 写入表头

# 模拟浏览器发送请求
for page in range(0, 251, 25):
    url = f'https://movie.douban.com/top250?start={page}&filter='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    # 把 response.text 文本数据转换成 selector 对象
    selector = parsel.Selector(response.text)
    # 获取所有li标签
    lis = selector.css('.grid_view li')
    # 遍历出每个li标签内容
    for li in lis:
        # 获取电影标题 hd 类属性 下面的 a 标签下面的 第一个span标签里面的文本数据 get()输出形式是 字符串获取一个  getall() 输出形式是列表获取所有
        title = li.css('.hd a span:nth-child(1)::text').get()   # get()输出形式是 字符串
        movie_list = li.css('.bd p:nth-child(1)::text').getall()     # getall() 输出形式是列表
        star = movie_list[0].strip().replace('\xa0\xa0\xa0', '').replace('/...', '')
        movie_info = movie_list[1].strip().split('\xa0/\xa0')   # ['1994', '美国', '犯罪 剧情']
        movie_time = movie_info[0]  # 电影上映时间
        movie_country = movie_info[1]   # 哪个国家的电影
        movie_type = movie_info[2]     # 什么类型的电影
        rating_num = li.css('.rating_num::text').get()   # 电影评分
        people = li.css('.star span:nth-child(4)::text').get()   # 评价人数
        summary = li.css('.inq::text').get()   # 一句话概述

        dit = {
            '电影名字': title,
            '参演人员': star,
            '上映时间': movie_time,
            '拍摄国家': movie_country,
            '电影类型': movie_type,
            '电影评分': rating_num,
            '评价人数': people,
            '电影概述': summary,
        }
        pprint.pprint(dit)
        print()
        csv_writer.writerow(dit)