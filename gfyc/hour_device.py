import argparse
import datetime

import influxdb_client
import pymysql
import pytz

'''
    功能      ->    获取 采集点数小于24条的电表，小时级电表
'''

parser = argparse.ArgumentParser(description='每日电表级采集小于24条，默认查询昨天')
parser.add_argument('--startDate', type=str, help='开始日期')
parser.add_argument('--endDate', type=str, help='结束日期')
date_list = []

conn = pymysql.connect(user='root', password='123456789', host='172.16.130.188', database='gfyc')
cursor = conn.cursor()

# influxdb连接
client = influxdb_client.InfluxDBClient(url='http://172.16.130.205:8092/',
                                        token='LRdIIW17oir2cDvCsrjZn1qvUOF5fFNwlqeqHGvg5LAv7pw-g_efZNbp7hhvV1aZwBecmMNgeE8dO9yPIPdLqA==',
                                        org='nari',
                                        timeout=50_000)
query_api = client.query_api()


# 本地时间转utc时间
def local_utc(datetime_str):
    local_time = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    utc_time = local_time.astimezone(pytz.timezone('UTC'))
    utc_time_str = datetime.datetime.strftime(utc_time, '%Y-%m-%dT%H:%M:%SZ')
    return utc_time_str


county_list = []
data_dict = {}


# 获取所有区县
def get_country():
    county_sql = 'select distinct county_code from dwd_cst_dygfyhsb_df'
    print('【获取所有区县】 \n' + county_sql + '\n')
    cursor.execute(county_sql)
    county_result = cursor.fetchall()
    for county in county_result:
        county_list.append(county[0])


# 获取电表编号与时间
def get_data():
    print('【获取小时级电表编号】\n')
    for date_str in date_list:
        data_dict[date_str] = {}
        for country_code in county_list:
            device_query = 'import "date" \n\n' \
                           't1 = from(bucket: "{0}") \n' \
                           '  |> range(start: {1}, stop: {2}) \n\n' \
                           't2 = from(bucket: "{0}") \n' \
                           '  |> range(start: {1}, stop: {2}) \n' \
                           '  |> group(columns: ["meter_id"]) \n' \
                           '  |> count() \n' \
                           '  |> filter(fn: (r) => r._value < 25) \n' \
                           '  |> map(fn: (r) => ({{ meter_id: r.meter_id}})) \n\n' \
                           'join(tables: {{te: t1, ts: t2}}, on: ["meter_id"], method: "inner") \n' \
                           '  |> map(fn: (r) => ({{ meter_id: r.meter_id, time: r._time}})) \n' \
                           '  |> yield(name: "v3") \n' \
                           ''.format(country_code, local_utc(date_str + ' 00:00:00'), local_utc(date_str + ' 23:59:59'))
            print(device_query + '\n')
            device_result = query_api.query(query=device_query)
            for item in device_result:
                for info in item.records:
                    meterId = info['meter_id']
                    time = info['time'].astimezone(pytz.timezone('Asia/Shanghai'))
                    hour = time.hour
                    minute = time.minute

                    if meterId not in data_dict[date_str]:
                        data_dict[date_str][meterId] = {}

                    if hour not in data_dict[date_str][meterId]:
                        data_dict[date_str][meterId][hour] = [minute]
                    else:
                        data_dict[date_str][meterId][hour].append(minute)
    print("完成")


# 导出数据
def export():
    # 每日小于25个点的电表 多日取交集
    point_device = []
    for date_str in data_dict.keys():
        if len(point_device) == 0:
            point_device = list(data_dict[date_str].keys())
        else:
            point_device = list(set(point_device).intersection(set(data_dict[date_str].keys())))
    with open("每日小于25个点的电表.txt", 'w', encoding='utf-8') as target_file:
        target_file.write(str(point_device))
        target_file.close()

    hour_device = []
    for date_str in data_dict.keys():
        temp_device_list = []
        for device in data_dict[date_str].keys():
            flag = True
            for hour_str in data_dict[date_str][device]:
                if len(data_dict[date_str][device][hour_str]) != 1 or data_dict[date_str][device][hour_str][0] > 0:
                    flag = False
                    break
            if flag:
                temp_device_list.append(device)
        if len(hour_device) == 0:
            hour_device = temp_device_list
        else:
            hour_device = list(set(hour_device).intersection(set(temp_device_list)))
    with open("小时级电表.txt", 'w', encoding='utf-8') as target_file:
        target_file.write(str(hour_device))
        target_file.close()


if __name__ == '__main__':
    args = parser.parse_args()
    print(args)

    if args.startDate is None or args.endDate is None:
        date_list.append(datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=-1), '%Y-%m-%d'))
    else:
        startDate = datetime.datetime.strptime(args.startDate, '%Y-%m-%d')
        endDate = datetime.datetime.strptime(args.endDate, '%Y-%m-%d')
        while endDate >= startDate:
            date_list.append(datetime.datetime.strftime(startDate, '%Y-%m-%d'))
            startDate = startDate + datetime.timedelta(days=1)
    get_country()
    get_data()
    export()
