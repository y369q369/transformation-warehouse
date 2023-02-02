import uuid
import pandas as pd
import pymysql

user_input = pd.read_excel('test.xlsx')
print(user_input)

create_user_sql = 'CREATE TABLE IF NOT EXISTS `user` ( ' \
                  '`id` varchar(32) NOT NULL, ' \
                  '`name` varchar(32) DEFAULT NULL, ' \
                  '`age` int DEFAULT NULL, ' \
                  '`sex` int DEFAULT NULL, ' \
                  'PRIMARY KEY (`id`) ' \
                  ') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT=\'用户\';'
print(create_user_sql)

insert_user_sql = 'insert into user(id, name, age, sex) values '
for user in user_input.values:
    insert_user_sql += f'\n    (\'{uuid.uuid1().hex}\', \'{user[0]}\', \'{user[1]}\', \'{user[2]}\'),'
insert_user_sql = insert_user_sql[:-1] + ';'
print(insert_user_sql)

temp_conn = pymysql.connect(user='root', password='1qaz@WSX', host='116.205.137.178', database='test')
cursor = temp_conn.cursor()
cursor.execute(create_user_sql)
cursor.execute(insert_user_sql)
temp_conn.commit()
