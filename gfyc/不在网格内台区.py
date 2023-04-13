import argparse
import datetime
import json
import math
from decimal import *

import influxdb_client
import pymysql
import pytz
import openpyxl
from openpyxl.styles import PatternFill, Font, Border, Side

'''
    功能      ->    查询不在网格内的台区
'''

conn = pymysql.connect(user='root', password='123456789', host='172.16.130.188', database='gfyc')
cursor = conn.cursor()

all_platform_list = []
grid_platform_sql_list = []


# 获取所有台区
def all_platform():
    all_platform_sql = 'select distinct d.resrc_supl_code from dwd_cst_dygfyhsb_df d'
    print('【获取所有台区】 \n' + all_platform_sql + '\n')
    cursor.execute(all_platform_sql)
    result = cursor.fetchall()

    for item in result:
        all_platform_list.append(item[0])


# 获取网格内台区
def grid_platform():
    grid_platform_sql = 'select distinct d.resrc_supl_code from dwd_cst_dygfyhsb_df d, grid_platform_relation g where d.resrc_supl_code = g.id'
    print('【获取网格内台区】 \n' + grid_platform_sql + '\n')
    cursor.execute(grid_platform_sql)
    result = cursor.fetchall()

    for item in result:
        grid_platform_sql_list.append(item[0])


# 获取不在网格内台区
def get_not_grid_platform():
    not_grid_platform_list = list(set(all_platform_list) - set(grid_platform_sql_list))
    with open("不在网格内台区.txt", 'w', encoding='utf-8') as target_file:
        target_file.write(str(not_grid_platform_list))
        target_file.close()
    not_grid_platform_sql = 'select d.resrc_supl_code, d.lng, d.lat from dwd_cst_dygfyhsb_df d where d.resrc_supl_code in ({})'.format(
        str(not_grid_platform_list)[1:-1])
    print('【获取不在网格内台区】 \n' + not_grid_platform_sql + '\n')
    cursor.execute(not_grid_platform_sql)
    result = cursor.fetchall()
    not_grid_platform_dict = {}
    for item in result:
        not_grid_platform_dict[item[0]] = {
            'lng': item[1],
            'lat': item[2]
        }
    with open("不在网格内台区.json", 'w', encoding='utf-8') as target_file:
        json.dump(not_grid_platform_dict, target_file, indent=4, ensure_ascii=False)
    target_file.close()


if __name__ == '__main__':
    all_platform()
    grid_platform()
    get_not_grid_platform()
