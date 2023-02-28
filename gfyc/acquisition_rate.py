import datetime
import json
import os

import influxdb_client
import pymysql
import pytz

'''
    功能      ->    统计全省指定日期采集成功率
'''

# influxdb连接
client = influxdb_client.InfluxDBClient(url='http://192.168.110.130:8086/',
                                        token='VsE9zz62qm_DZKB6eib-hTSk1Ml-e8uF82Sqdbe5xnUJwOKshHFZCdMaiMa7Fqx_KD2iKmWCjg2u6XHTABcaSA==',
                                        org='gs',
                                        timeout=50_000)
query_api = client.query_api()

conn = pymysql.connect(user='root', password='1qaz@WSX', host='127.0.0.1', database='gfyc')
cursor = conn.cursor()

date_str = '2023-02-06'

#  从文件获取查询语句
with open('acquisition_influx_query.txt', encoding='utf-8') as file:
    acquisition_influx_query_format = file.read()
    file.close()


# 本地时间转utc时间
def local_utc(datetime_str):
    local_time = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    utc_time = local_time.astimezone(pytz.timezone('UTC'))
    utc_time_str = datetime.datetime.strftime(utc_time, '%Y-%m-%dT%H:%M:%SZ')
    return utc_time_str


# 电表总数量
device_num_sql = 'SELECT count(0) FROM dwd_cst_dygfyhsb_df'
cursor.execute(device_num_sql)
device_num = cursor.fetchone()[0]

# 区县编码集合
county_code_sql = 'SELECT distinct county_code FROM dwd_cst_dygfyhsb_df'
cursor.execute(county_code_sql)
county_code_result = cursor.fetchall()

total_num = 0  # 采集总数
percent90 = 0  # 电表采集成功率 > 90%
percent70 = 0  # 电表采集成功率  70% ~ 89%
percent_hour = 0  # 电表采集成功数量 > 24
num10 = 0  # 电表采集成功数量 > 9
percent100 = 0  # 电表采集成功数量 = 96
percent0 = 0  # 采集到数据的电表数

for county_code in county_code_result:
    print('查询县： {}'.format(county_code[0]))
    acquisition_influx_query = acquisition_influx_query_format.format(county_code[0], local_utc(date_str + ' 00:00:00'),
                                                                      local_utc(date_str + ' 23:59:00'))
    print(acquisition_influx_query)
    num_result = query_api.query(query=acquisition_influx_query)
    for item in num_result:
        for num_item in item.records:
            key = num_item['result']
            if key == 'v1':
                total_num += num_item['num']
            elif key == 'v2':
                percent90 += num_item['num']
            elif key == 'v3':
                percent70 += num_item['num']
            elif key == 'v4':
                percent_hour += num_item['num']
            elif key == 'v5':
                num10 += num_item['num']
            elif key == 'v6':
                percent100 += num_item['num']
            elif key == 'v7':
                percent0 += num_item['num']

total_percent = (total_num / (device_num * 96)) * 100
total_percent = ("%.2f" % total_percent) + '%'

target_file_name = 'acquisition.json'
if os.path.exists(target_file_name):
    with open(target_file_name, encoding='utf8') as fp:
        target = json.load(fp)
        fp.close()
else:
    target = {
        date_str: {}
    }

target[date_str] = {
    '夜里补采成功率': total_percent,
    '采集成功率：100%': percent100,
    '采集成功率：90%': percent90,
    '采集成功率：70%-89%': percent70,
    '低于25条数据': device_num - percent_hour,
    '低于10条数据': device_num - num10,
    '采集成功率：0%': device_num - percent0
}
print(target)

# 导出数据

with open(target_file_name, 'w', encoding='utf-8') as target_file:
    json.dump(target, target_file, indent=4, ensure_ascii=False)
    target_file.close()
