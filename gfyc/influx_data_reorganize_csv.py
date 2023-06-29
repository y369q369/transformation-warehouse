import argparse
import datetime

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pymysql
import os
import pytz

import pandas as pd

'''
    功能      ->    数据从csv读取转存influxDB（添加电表类型）
'''

parser = argparse.ArgumentParser(description='influxDB数据整理（添加电表类型）')
parser.add_argument('--countyCode', type=str, help='区县列表', default='3240101')

data_direction = 'C:/Users/gs/Desktop/data'

conn = pymysql.connect(user='root', password='123456789', host='172.16.130.188', database='gfyc')
cursor = conn.cursor()

client2 = influxdb_client.InfluxDBClient(url='http://172.16.130.188:8092/',
                                         token='3aOD_2CRhOmb0QN4qG4FXLAqmq_fQMp-wje54rzGHehYQYaTInT7_yZTwIUM-plyrSbolVO2aaB5reuugcoeUg==',
                                         org='nari',
                                         timeout=200_000)
write_api = client2.write_api(write_options=SYNCHRONOUS)
bucket_api = client2.buckets_api()

county_code_list = []
device_dict = {}


# 本地时间转utc时间
def local_utc(datetime_str):
    local_time = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    utc_time = local_time.astimezone(pytz.timezone('UTC'))
    utc_time_str = datetime.datetime.strftime(utc_time, '%Y-%m-%dT%H:%M:%SZ')
    return utc_time_str


# 获取数据
def init_county_code():
    global county_code_list
    global device_dict
    # 获取档案信息
    county_code_sql = 'SELECT county_code, dev_no, type FROM dwd_cst_dygfyhsb_df'
    print('【获取区县编码】 \n' + county_code_sql + '\n')
    cursor.execute(county_code_sql)
    county_code_result = cursor.fetchall()
    for item in county_code_result:
        if item[0] not in county_code_list:
            county_code_list.append(item[0])
        device_dict[item[1]] = item[2]


# 删除bucket
def delete_bucket():
    for county_code in county_code_list:
        bucket = bucket_api.find_bucket_by_name(county_code)
        if bucket is not None:
            bucket_api.delete_bucket(bucket=bucket.id)
        bucket_fifteen = bucket_api.find_bucket_by_name(county_code + '_fifteen')
        if bucket_fifteen is not None:
            bucket_api.delete_bucket(bucket=bucket_fifteen.id)
        bucket_hour = bucket_api.find_bucket_by_name(county_code + '_hour')
        if bucket_hour is not None:
            bucket_api.delete_bucket(bucket=bucket_hour.id)


# 创建bucket
def create_bucket():
    bucket_list = []
    limit = 100
    offset = 0
    current_num = 1
    while current_num > 0:
        current_buckets = bucket_api.find_buckets(offset=offset, limit=100)
        current_num = len(current_buckets.buckets)
        if current_num > 0:
            offset += limit
            for bucket in current_buckets.buckets:
                bucket_list.append(bucket.name)

    for county_code in county_code_list:
        if county_code not in bucket_list:
            bucket_api.create_bucket(bucket_name=county_code)
            print('新增 bucket: ' + county_code)
        if county_code + '_hour' not in bucket_list:
            bucket_api.create_bucket(bucket_name=county_code + '_hour')
            print('新增 bucket: ' + county_code + '_hour')
        if county_code + '_fifteen' not in bucket_list:
            bucket_api.create_bucket(bucket_name=county_code + '_fifteen')
            print('新增 bucket: ' + county_code + '_fifteen')


# 重储电表数据
def reorganize_data(county_code):
    # 从本地csv文件读取
    county_direction = f'{data_direction}/{county_code}'
    if os.path.exists(county_direction):
        devices = os.listdir(county_direction)
        batch_devices = [devices[i:i + 10] for i in range(0, len(devices), 10)]
        for temp_devices in batch_devices:

            point_list = []
            point_type1_list = []
            point_type2_list = []

            for device_file in temp_devices:
                try:
                    df = pd.read_csv(f'{county_direction}/{device_file}')
                except Exception as e:
                    print(f'{county_direction}/{device_file} 文件异常')
                    continue

                dev_no = device_file.replace('.csv', '')
                device_type = -1
                if dev_no in device_dict:
                    device_type = device_dict[dev_no]

                for index, row in df.iterrows():
                    time = row['_time'] * 100000000000
                    utc_time = pd.to_datetime(time, utc=True)
                    utc_time_str = datetime.datetime.strftime(utc_time, '%Y-%m-%dT%H:%M:%SZ')

                    record = influxdb_client.Point("power_monitor") \
                        .tag("type", device_type) \
                        .tag("device_id", dev_no) \
                        .field("TotW", row['_value']) \
                        .time(utc_time_str)
                    point_list.append(record)

                    type_record = influxdb_client.Point("power_monitor") \
                        .tag("device_id", dev_no) \
                        .field("TotW", row['_value']) \
                        .time(utc_time_str)
                    point_list.append(record)
                    if device_type == 1:
                        point_type1_list.append(type_record)
                    else:
                        point_type2_list.append(type_record)

            print('写入 {} ( {}  )'.format(county_code, str(temp_devices)))
            write_api.write(bucket=county_code, record=point_list)
            write_api.write(bucket=county_code + '_fifteen', record=point_type1_list)
            write_api.write(bucket=county_code + '_hour', record=point_type2_list)


if __name__ == '__main__':
    init_county_code()
    # delete_bucket()
    # create_bucket()

    args = parser.parse_args()
    county_code_str = args.countyCode
    if county_code_str is not None:
        county_code_list = county_code_str.split(",")

    for county_code in county_code_list:
        st = datetime.datetime.now()
        print('【区县写入】 {} 开始'.format(county_code))
        reorganize_data(county_code)
        print('【区县写入】 {} 完成，耗时 {} 分钟'.format(county_code, (datetime.datetime.now() - st).seconds // 60))
