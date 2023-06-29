import datetime
import json

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pymysql
import pytz

'''
    功能      ->    光伏电表采集异常数据处理
'''

conn = pymysql.connect(user='root', password='123456789', host='172.16.130.188', database='gfyc')
cursor = conn.cursor()

client = influxdb_client.InfluxDBClient(url='http://172.16.130.205:8092/',
                                        token='LRdIIW17oir2cDvCsrjZn1qvUOF5fFNwlqeqHGvg5LAv7pw-g_efZNbp7hhvV1aZwBecmMNgeE8dO9yPIPdLqA==',
                                        org='nari',
                                        timeout=50_000)
query_api = client.query_api()
write_api = client.write_api(write_options=SYNCHRONOUS)

start_time = '2023-03-01 00:00:00'
end_time = '2023-05-09 23:59:59'
county_code_list = []
abnormal_power_list = []


# 本地时间转utc时间
def local_utc(datetime_str):
    local_time = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    utc_time = local_time.astimezone(pytz.timezone('UTC'))
    utc_time_str = datetime.datetime.strftime(utc_time, '%Y-%m-%dT%H:%M:%SZ')
    return utc_time_str


# 获取区县编码
def init_county_code():
    # 获取档案信息
    county_code_sql = 'SELECT distinct county_code FROM dwd_cst_dygfyhsb_df'
    print('【获取区县编码】 \n' + county_code_sql + '\n')
    cursor.execute(county_code_sql)
    county_code_result = cursor.fetchall()
    for item in county_code_result:
        county_code_list.append(item[0])
    return county_code_list


# 获取异常功率电表数据
def get_abnormal_power_record():
    for county_code in county_code_list:
        abnormal_power_query = 'from(bucket: "{}")\n' \
                               '  |> range(start: {}, stop: {})\n' \
                               '  |> filter(fn:(r) => r["_value"] > 10000 or r["_value"] < -10) \n' \
            .format(county_code, local_utc(start_time), local_utc(end_time))
        print(abnormal_power_query + '\n')
        abnormal_power_result = query_api.query(query=abnormal_power_query)
        for item in abnormal_power_result:
            for info in item.records:
                abnormal_power_list.append({
                    'device_id': info['device_id'],
                    'meter_id': info['meter_id'],
                    'platform_id': info['platform_id'],
                    'county_code': county_code,
                    'power': info['_value'],
                    'time': datetime.datetime.strftime(info['_time'], '%Y-%m-%dT%H:%M:%SZ'),
                })
    print(abnormal_power_list)


# 写入数据到influxDB
def write_abnormal_power_record():
    # with open("C:/Users/gs/Desktop/test.json", 'r', encoding='utf-8') as load_f:
    #     abnormal_power_list = json.load(load_f)
    # print(abnormal_power_list)

    if len(abnormal_power_list) > 0:
        abnormal_record_list = []
        record_dict = {}
        for item in abnormal_power_list:
            record = influxdb_client.Point("power_monitor") \
                .tag("platform_id", item['platform_id']).tag("meter_id", item['meter_id']).tag("device_id",
                                                                                               item['device_id']) \
                .field("TotW", 0.0) \
                .time(item['time'])
            if item['county_code'] not in record_dict:
                record_dict[item['county_code']] = []
            record_dict[item['county_code']].append(record)

            record2 = influxdb_client.Point("power_monitor") \
                .tag("county_code", item['county_code']).tag("platform_id", item['platform_id']).tag("meter_id", item[
                'meter_id']).tag("device_id", item['device_id']) \
                .field("TotW", item['power']) \
                .time(item['time'])
            abnormal_record_list.append(record2)

        # 原 bucket 异常数据那一条置为0
        for item in record_dict.keys():
            write_api.write(bucket=item, record=record_dict[item])
        # 异常数据新增到异常表
        write_api.write(bucket='abnormal_power_record', record=abnormal_record_list)


if __name__ == '__main__':
    init_county_code()
    get_abnormal_power_record()
    write_abnormal_power_record()
