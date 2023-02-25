import argparse
import datetime

import influxdb_client
import pymysql
import pytz

parser = argparse.ArgumentParser(description='统计某日无数据的电表编号')
parser.add_argument('--date', type=str, help='查询日期')

# 初始化参数
args = parser.parse_args()
queryDate = args.date
if queryDate is None:
    queryDate = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=-1), '%Y-%m-%d')
# queryDate = '2023-02-10'
print('【查询日期】 ' + queryDate + '\n')

client = influxdb_client.InfluxDBClient(url='http://192.168.110.130:8086/',
                                        token='VsE9zz62qm_DZKB6eib-hTSk1Ml-e8uF82Sqdbe5xnUJwOKshHFZCdMaiMa7Fqx_KD2iKmWCjg2u6XHTABcaSA==',
                                        org='gs')

conn = pymysql.connect(user='root', password='1qaz@WSX', host='127.0.0.1', database='gfyc')
cursor = conn.cursor()


# 本地时间转utc时间
def local_utc(datetime_str):
    local_time = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    utc_time = local_time.astimezone(pytz.timezone('UTC'))
    utc_time_str = datetime.datetime.strftime(utc_time, '%Y-%m-%dT%H:%M:%SZ')
    return utc_time_str


# 获取电表
device_sql = 'select distinct meter_id from dwd_cst_dygfyhsb_df'
print('【获取电表】 \n' + device_sql + '\n')
cursor.execute(device_sql)
device_result = cursor.fetchall()
device_list = []
for device in device_result:
    device_list.append(device[0])

# 获取所有区县
county_sql = 'select distinct county_code from dwd_cst_dygfyhsb_df'
print('【获取所有区县】 \n' + county_sql + '\n')
cursor.execute(county_sql)
county_result = cursor.fetchall()
county_list = []
for county in county_result:
    county_list.append(county[0])

# 获取实际有数据电表
has_data_device_list = []
query_api = client.query_api()
print('【有数据电表获取】\n')
for county_code in county_result:
    infludb_device_query = 'from(bucket: "{}")\n  |> range(start: {}, stop: {})\n' \
                           '  |> group(columns: ["meter_id"])\n' \
                           '  |> count()\n' \
                           '  |> map(fn: (r) => ({{ actual: r._value, meter_id: r.meter_id, time: r._time }}))' \
        .format(county_code[0], local_utc(queryDate + ' 00:00:00'), local_utc(queryDate + ' 23:59:59'))
    print(infludb_device_query + '\n')
    device_result = query_api.query(org='gs', query=infludb_device_query)
    for item in device_result:
        for device_info in item.records:
            has_data_device_list.append(device_info['meter_id'])

print('【获取无数据电表】\n')
no_data_device_list = list(set(device_list) - set(has_data_device_list))
print('【处理完成】\n')
# print(str(no_data_device_list))


target_file_name = '无数据电表（' + queryDate + '）.txt'
# 导出数据
with open(target_file_name, 'w', encoding='utf-8') as target_file:
    target_file.write(str(no_data_device_list))
    target_file.close()
