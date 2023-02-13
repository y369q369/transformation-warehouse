import datetime
import json
import os
import threading
import time

import influxdb_client
import pymysql
import pytz


# 本地时间转utc时间
def local_utc(local_time):
    utc_time = local_time.astimezone(pytz.timezone('UTC'))
    utc_time_str = datetime.datetime.strftime(utc_time, '%Y-%m-%dT%H:%M:%SZ')
    return utc_time_str


# 统计采集成功率
def get_supply_acquisition(statistics_time_str, times):
    # influxdb连接
    client = influxdb_client.InfluxDBClient(url='http://172.16.130.205:8092/',
                                            token='LRdIIW17oir2cDvCsrjZn1qvUOF5fFNwlqeqHGvg5LAv7pw-g_efZNbp7hhvV1aZwBecmMNgeE8dO9yPIPdLqA==',
                                            org='nari')
    query_api = client.query_api()

    # mysql连接
    conn = pymysql.connect(user='root', password='123456789', host='172.16.130.188', database='gfyc')
    cursor = conn.cursor()

    # 电表总数量
    device_num_sql = 'SELECT count(0) FROM dwd_cst_dygfyhsb_df'
    cursor.execute(device_num_sql)
    device_num = cursor.fetchone()[0]

    # 区县编码集合
    county_code_sql = 'SELECT distinct county_code FROM dwd_cst_dygfyhsb_df'
    cursor.execute(county_code_sql)
    county_code_result = cursor.fetchall()

    # 获取数据
    target_file_name = 'supply_acquisition.json'
    if os.path.exists(target_file_name):
        with open(target_file_name, encoding='utf8') as fp:
            json_data = json.load(fp)
            fp.close()
    else:
        json_data = {
            statistics_time_str: {}
        }

    start_time = datetime.datetime.strptime(statistics_time_str, '%Y-%m-%d %H:%M:%S')
    # 结束时间为开始时间+1minute
    utc_start_time_str = local_utc(start_time)
    end_time = start_time + datetime.timedelta(minutes=1)
    utc_end_time_str = local_utc(end_time)

    total_num = 0  # 采集总数
    for county_code in county_code_result:
        acquisition_influx_query = 'from(bucket: "{}")\n  ' \
                                   '|> range(start: {}, stop: {})\n  ' \
                                   '|> group(columns: ["bucket"])\n  ' \
                                   '|> count()\n  ' \
                                   '|> map(fn: (r) => ({{ num: r._value }}))'.format(county_code[0], utc_start_time_str,
                                                                                     utc_end_time_str)
        # print(acquisition_influx_query)
        num_result = query_api.query(org='nari', query=acquisition_influx_query)
        for item in num_result:
            for num_item in item.records:
                total_num = total_num + num_item['num']

    total_percent = (total_num / device_num) * 100
    total_percent = ("%.2f" % total_percent) + '%'

    time_str = datetime.datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')
    if time_str not in json_data:
        json_data[time_str] = {
            '第' + str(times) + '次': total_percent
        }
    else:
        json_data[time_str]['第' + str(times) + '次'] = total_percent

    print(datetime.datetime.now(), json_data)

    # 导出数据
    with open(target_file_name, 'w', encoding='utf-8') as target_file:
        json.dump(json_data, target_file, indent=4, ensure_ascii=False)
        target_file.close()


class StatisticsThread(threading.Thread):

    def __init__(self, statistics_time_str, times):
        threading.Thread.__init__(self)
        self.statistics_time_str = statistics_time_str
        self.times = times

    def run(self):
        time.sleep((self.times - 1) * 60 * 15)
        get_supply_acquisition(self.statistics_time_str, self.times)


if __name__ == '__main__':
    statistics_time_str = '2023-02-06 12:00:00'
    for times in range(1, 5):
        thread = StatisticsThread(statistics_time_str, times)
        thread.start()
