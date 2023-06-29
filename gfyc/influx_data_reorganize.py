import argparse
import datetime

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pymysql
import pytz

'''
    功能      ->    influxDB数据整理（添加电表类型）
'''

parser = argparse.ArgumentParser(description='influxDB数据整理（添加电表类型）')
parser.add_argument('--startDate', type=str, help='开始日期')
parser.add_argument('--endDate', type=str, help='结束日期')

conn = pymysql.connect(user='root', password='123456789', host='172.16.130.188', database='gfyc')
cursor = conn.cursor()

client = influxdb_client.InfluxDBClient(url='http://172.16.130.205:8092/',
                                        token='LRdIIW17oir2cDvCsrjZn1qvUOF5fFNwlqeqHGvg5LAv7pw-g_efZNbp7hhvV1aZwBecmMNgeE8dO9yPIPdLqA==',
                                        org='nari',
                                        timeout=200_000)
query_api = client.query_api()

client2 = influxdb_client.InfluxDBClient(url='http://172.16.130.188:8092/',
                                         token='3aOD_2CRhOmb0QN4qG4FXLAqmq_fQMp-wje54rzGHehYQYaTInT7_yZTwIUM-plyrSbolVO2aaB5reuugcoeUg==',
                                         org='nari',
                                         timeout=200_000)
write_api = client2.write_api(write_options=SYNCHRONOUS)
bucket_api = client2.buckets_api()

county_code_list = []
device_dict = {}
abnormal_power_list = []


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


# 获取电表数据
def get_old_data(county_code, st, et):
    device_query = 'from(bucket: "{}")\n' \
                   '  |> range(start: {}, stop: {})\n' \
                   '  |> map(fn: (r) => ({{ _value: r._value, _time: r._time, device_id: r.device_id }})) ' \
        .format(county_code, local_utc(st), local_utc(et))
    print(device_query)

    old_data = []
    abnormal_power_result = query_api.query(query=device_query)
    for item in abnormal_power_result:
        for info in item.records:
            device_type = -1
            if info['device_id'] in device_dict:
                device_type = device_dict[info['device_id']]
            old_data.append({
                'device_id': info['device_id'],
                'power': info['_value'],
                'time': datetime.datetime.strftime(info['_time'], '%Y-%m-%dT%H:%M:%SZ'),
                'type': device_type
            })
    return old_data


# 写入数据到influxDB
def write_record(county_code, old_data):
    if len(old_data) > 0:
        point_list = []
        point_type1_list = []
        point_type2_list = []
        for item in old_data:
            record = influxdb_client.Point("power_monitor") \
                .tag("type", item['type']) \
                .tag("device_id", item['device_id']) \
                .field("TotW", item['power']) \
                .time(item['time'])
            point_list.append(record)

            type_record = influxdb_client.Point("power_monitor") \
                .tag("device_id", item['device_id']) \
                .field("TotW", item['power']) \
                .time(item['time'])
            point_list.append(record)
            if item['type'] == 1:
                point_type1_list.append(type_record)
            else:
                point_type2_list.append(type_record)

        # 异常数据新增到异常表
        print('写入 {}'.format(county_code))
        write_api.write(bucket=county_code, record=point_list)
        print('写入 {}'.format(county_code + '_fifteen'))
        write_api.write(bucket=county_code + '_fifteen', record=point_type1_list)
        print('写入 {} \n'.format(county_code + "_hour"))
        write_api.write(bucket=county_code + "_hour", record=point_type2_list)


# 重储数据
def reorganize_data(county_code, date_str):
    old_data = get_old_data(county_code, date_str + ' 00:00:00', date_str + ' 23:59:59')
    write_record(county_code, old_data)
    # print(old_data)


if __name__ == '__main__':
    init_county_code()
    # delete_bucket()
    create_bucket()

    # 处理日期
    date_list = []
    args = parser.parse_args()
    if args.startDate is None or args.endDate is None:
        date_list.append(datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=-1), '%Y-%m-%d'))
    else:
        startDate = datetime.datetime.strptime(args.startDate, '%Y-%m-%d')
        endDate = datetime.datetime.strptime(args.endDate, '%Y-%m-%d')
        while endDate >= startDate:
            date_list.append(datetime.datetime.strftime(startDate, '%Y-%m-%d'))
            startDate = startDate + datetime.timedelta(days=1)

    # 数据重新存储
    for date_str in date_list:
        print('【数据处理】 {} \n'.format(date_str))
        for county_code in county_code_list:
            reorganize_data(county_code, date_str)
