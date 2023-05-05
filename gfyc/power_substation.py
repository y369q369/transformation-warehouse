import datetime
import json

import influxdb_client
import requests
from influxdb_client.client.write_api import SYNCHRONOUS
import pymysql
import pytz

'''
    功能      ->    光伏厂站出力
'''

conn = pymysql.connect(user='root', password='123456789', host='172.16.130.188', database='gfyc')
cursor = conn.cursor()

client = influxdb_client.InfluxDBClient(url='http://172.16.130.205:8092/',
                                        token='LRdIIW17oir2cDvCsrjZn1qvUOF5fFNwlqeqHGvg5LAv7pw-g_efZNbp7hhvV1aZwBecmMNgeE8dO9yPIPdLqA==',
                                        org='nari',
                                        timeout=50_000)
write_api = client.write_api(write_options=SYNCHRONOUS)

start_time = '2023-01-01 00:00:00'
measure_url = 'http://10.134.157.86:30962/gfyc/getCalcpointMeasure'
headers = {
    "Content-Type": "application/json"
}
bucket_name = 'substation_measure'
substation_list = []
power_dict = {}


# 本地时间转utc时间
def local_utc(datetime_str):
    local_time = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    utc_time = local_time.astimezone(pytz.timezone('UTC'))
    utc_time_str = datetime.datetime.strftime(utc_time, '%Y-%m-%dT%H:%M:%SZ')
    return utc_time_str


# 获取台账信息
def init_substation_code():
    # 获取档案信息
    info_sql = 'SELECT distinct id FROM substation'
    print('【获取档案信息】 \n' + info_sql + '\n')
    cursor.execute(info_sql)
    substation_result = cursor.fetchall()
    for item in substation_result:
        substation_list.append(item[0])
    print('【光伏厂站测点台账】\n' + str(substation_list) + '\n')


# 获取异常功率电表数据
def get_power_data():
    if len(substation_list) > 0:
        for substation_id in substation_list:
            print('【获取光伏厂站测点数据】 ' + substation_id + '\n')
            params = {
                'id': substation_id,
                'startTime': start_time
            }
            response = requests.post(url=measure_url, json=params, headers=headers)
            data = json.loads(response.content)
            if data['code'] == 200:
                temp_list = []
                value_list = data['calcpointMeasure']
                for item in value_list:
                    temp_list.append({
                        'id': substation_id,
                        'time': item['occurTime'],
                        'value': item['cValue']
                    })
                if len(temp_list) > 0:
                    power_dict[substation_id] = temp_list
        # 保存功率数据
        with open('power_substation.json', 'w', encoding='utf-8') as target_file:
            json.dump(power_dict, target_file, indent=4, ensure_ascii=False)
        target_file.close()


# 写入数据到influxDB
def write_power_data():
    with open("power_substation_230401-230425.json", 'r', encoding='utf-8') as load_f:
        power_dict = json.load(load_f)
    # print(power_dict)

    if len(power_dict.keys()) > 0:
        for substation_id in power_dict.keys():
            print('【写入influxDB】 ' + substation_id + '\n')
            power_data = power_dict[substation_id]
            record_list = []
            for item in power_data:
                record = influxdb_client.Point("substation_power") \
                    .tag("id", substation_id) \
                    .field("power", item['value']) \
                    .time(local_utc(item['time']))
                record_list.append(record)
            # 写入数据
            write_api.write(bucket=bucket_name, record=record_list)


if __name__ == '__main__':
    init_substation_code()
    get_power_data()
    write_power_data()
