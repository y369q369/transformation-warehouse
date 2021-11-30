""""""
import pymysql
import uuid
import configparser
'''
    数据库连接示例
'''


class Mysql:
    conn = None
    cursor = None
    cf = None

    def __init__(self):
        # 读取配置文件
        self.cf = configparser.ConfigParser()
        self.cf.read('./config.ini', encoding='utf-8')
        user = self.cf.get("mysql", "user")
        pwd = self.cf.get("mysql", "password")
        host = self.cf.get("mysql", "host")
        database = self.cf.get("mysql", "database")
        # 创建数据库连接
        temp_conn = pymysql.connect(user=user, password=pwd, host=host, database=database)
        self.conn = temp_conn
        self.cursor = temp_conn.cursor()

    def execute(self, sql):
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
        except Exception as e:
            print(e.args)
            # 如果发生错误则回滚
            self.conn.rollback()

    def close(self):
        self.conn.close()
        self.cursor.close()


class Novel(Mysql):
    insertSql = "insert into monthly_ticket_list(id, img_url, nove_url, name, author, novel_type, status, " \
                "description, latest_chapter, update_time) " \
                "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    # 建表
    def create_table(self):
        try:
            create_table_sql = self.cf.get("sql", "create_table_sql")
            self.cursor.execute(create_table_sql)
            self.conn.commit()
        except Exception as e:
            print(e.args)
            # 如果发生错误则回滚
            self.conn.rollback()

    # 插入单条（完整sql）
    def insert_full_sql(self):
        try:
            uid = uuid.uuid1().hex
            insert_full_sql = "insert into monthly_ticket_list(id, img_url, nove_url, name, author, novel_type, " \
                              "status, description, latest_chapter, update_time) " \
                              "values('{0}', 'book.qidian.com/info/1024868626/', " \
                              "'bookcover.yuewen.com/qdbimg/349573/1024868626/150', " \
                              "'从红月开始', '黑山老鬼', '科幻', '连载'," \
                              "'红月亮出现在天上的那一刻开始，全世界的人都成了疯子。除了我！','第八百四十四章 温馨的家庭（三更）','2021-11-22 13:04')" \
                .format(uid)
            self.cursor.execute(insert_full_sql)
            self.conn.commit()
        except Exception as e:
            print(e.args)
            # 如果发生错误则回滚
            self.conn.rollback()

    # 插入单条（动态参数）
    def insert_one(self):
        try:
            param = [uuid.uuid1().hex, 'book.qidian.com/info/1027669580/',
                     'bookcover.yuewen.com/qdbimg/349573/1027669580/150', '星门', '老鹰吃小鸡', '玄幻',
                     '连载',
                     '传说，在那古老的星空深处，伫立着一道血与火侵染的红色之门。传奇与神话，黑暗与光明，无尽传说皆在这古老的门户中流淌。俯瞰星门，热血照耀天地，黑暗终将离去！',
                     '第305章 新道首战（求订阅月票）', '2021-11-22 21:31']
            self.cursor.execute(self.insertSql, param)
            self.conn.commit()
        except Exception as e:
            print(e.args)
            # 如果发生错误则回滚
            self.conn.rollback()

    # 批量插入（动态参数）
    def insert_many(self):
        try:
            params = [
                [uuid.uuid1().hex, 'book.qidian.com/info/1021617576/',
                 'bookcover.yuewen.com/qdbimg/349573/1021617576/150', '夜的命名术',
                 '会说话的肘子', '都市', '连载',
                 '蓝与紫的霓虹中，浓密的钢铁苍穹下，数据洪流的前端，是科技革命之后的世界，也是现实与虚幻的分界。钢铁与身体，过去与未来。这里，'
                 '表世界与里世界并存，面前的一切，像是时间之墙近在眼前。黑暗逐渐笼罩。可你要明白啊我的朋友，我们不能用温柔去应对黑暗，要用火。',
                 '489、违约者', '2021-11-22 22:32'],
                [uuid.uuid1().hex, 'book.qidian.com/info/1025901449/',
                 'bookcover.yuewen.com/qdbimg/349573/1025901449/150', '我的治愈系游戏',
                 '我会修空调', '悬疑', '连载',
                 '警察同志，如果我说这是一款休闲治愈系游戏，你们信吗？', '第522章 我来帮你把世界染红（6000求月票）', '2021-11-22 23:38']]
            size = self.cursor.executemany(self.insertSql, params)
            print('批量插入：插入成功 {0} 条'.format(size))
            self.conn.commit()
        except Exception as e:
            print(e.args)
            # 如果发生错误则回滚
            self.conn.rollback()

    # 根据书名和作者查询
    def select_by_name_author(self, name, author):
        try:
            param = [name, author]
            select_sql = "select * from monthly_ticket_list where name = %s and author = %s"
            self.cursor.execute(select_sql, param)
            result = self.cursor.fetchone()
            if result:
                print('书名：{0}, 作者：{1}, 地址：{2}'.format(result[3], result[4], result[1]))
            else:
                print('书名：{0} 未找到'.format(name))

        except Exception as e:
            print(e.args)

    # 根据书名和作者更新
    def update_by_name_author(self, status, latestchapter, updatetime, name, author):
        try:
            param = [status, latestchapter, updatetime, name, author]
            update_sql = "update monthly_ticket_list set status = %s, latest_chapter = %s, update_time = %s " \
                         "where name = %s and author = %s"
            self.cursor.execute(update_sql, param)
            print('【{0}】 更新成功'.format(name))
        except Exception as e:
            print(e.args)
            # 如果发生错误则回滚
            self.conn.rollback()


if __name__ == '__main__':
    novel = Novel()
    novel.create_table()
    novel.insert_full_sql()
    novel.insert_one()
    novel.insert_many()
    novel.select_by_name_author('从红月开始', '黑山老鬼')
    novel.select_by_name_author('从红月开2始', '黑山老鬼')
    novel.update_by_name_author('完结', '205章', '2021-11-23 14:17', '从红月开始', '黑山老鬼')
