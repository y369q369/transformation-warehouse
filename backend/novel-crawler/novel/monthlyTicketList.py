""""""
import configparser
import pymysql
import requests
import parsel
import uuid
import time

'''
    1. 爬取 起点中文网 月票排行榜
    2. 存储小说信息并入库
'''


class MonthlyTicketList:
    conn = None
    cursor = None

    def __init__(self):
        # 读取配置文件
        cf = configparser.ConfigParser()
        cf.read('./config.ini', encoding='utf-8')
        user = cf.get("mysql", "user")
        pwd = cf.get("mysql", "password")
        host = cf.get("mysql", "host")
        database = cf.get("mysql", "database")
        # 创建数据库连接
        temp_conn = pymysql.connect(user=user, password=pwd, host=host, database=database)
        self.conn = temp_conn
        self.cursor = temp_conn.cursor()
        # 建表
        create_table_sql = cf.get("sql", "create_table_sql")
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def get_monthly_ticket_list(self):
        novel_list = []
        for page in range(1, 6):
            url = f"https://www.qidian.com/rank/yuepiao/page{page}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/96.0.4664.45 Safari/537.36',
            }
            response = requests.get(url=url, headers=headers)
            # 把 response.text 文本数据转换成 selector 对象
            selector = parsel.Selector(response.text)
            lis = selector.css('#rank-view-list li')

            for li in lis:
                # 获取 img标签 src 属性值
                img_url = li.css(".book-img-box img::attr(src)").get()[2:]
                # 获取 a标签 href 属性值， 截取字符串：从第三个字符到结尾
                novel_url = li.css(".book-img-box a::attr(href)").get()[2:]
                # 获取 a标签 内容
                name = li.css(".book-mid-info h4 a::text").get()
                author = li.css(".book-mid-info .author .name::text").get()
                # 获取 第二个 a标签 内容
                novel_type = li.css(".book-mid-info .author a:nth-of-type(2)::text").get()
                status = li.css(".book-mid-info .author span::text").get()
                # 去除首尾空格：strip(), 替换\r 为 空
                description = li.css(".book-mid-info .intro::text").get().replace("\r", "").strip()
                latest_chapter = li.css(".book-mid-info .update a::text").get()[5:]
                update_time = li.css(".book-mid-info .update span::text").get()

                # 图片url、 章节url、 名称、 作者、 类型、 连载状态、 简介、 最新章节、 最近更新时间
                novel = [img_url, novel_url, name, author, novel_type, status, description, latest_chapter, update_time]
                novel_list.append(novel)
        return novel_list

    def save_info(self, novel_list):
        insert_list = []
        for novel in novel_list:
            if len(novel[8]) == 11:
                novel[8] = '2021-' + novel[8]
            param = [novel[2], novel[3]]
            select_sql = "select * from monthly_ticket_list where name = %s and author = %s"
            self.cursor.execute(select_sql, param)
            result = self.cursor.fetchone()
            if result:
                param = [novel[5], novel[7], novel[8], novel[2], novel[3]]
                update_sql = "update monthly_ticket_list set status = %s, latest_chapter = %s, update_time = %s " \
                             "where name = %s and author = %s"
                self.cursor.execute(update_sql, param)
                self.conn.commit()
            else:
                insert_list.append([uuid.uuid1().hex] + novel)

        if len(insert_list) > 0:
            insert_many_sql = "insert into monthly_ticket_list(id, img_url, nove_url, name, author, novel_type, status, " \
                              "description, latest_chapter, update_time) " \
                              "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.executemany(insert_many_sql, insert_list)
            self.conn.commit()
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 更新完成")


if __name__ == '__main__':
    monthly_ticket = MonthlyTicketList()
    novel_list = monthly_ticket.get_monthly_ticket_list()
    monthly_ticket.save_info(novel_list)
