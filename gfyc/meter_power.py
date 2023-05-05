import datetime
import json

import influxdb_client
import pytz

county_code = '3241106'
dev_no = '1541674232'

st = '2023-03-01'
et = '2023-04-20'


# 本地时间转utc时间
def local_utc(local_time):
    utc_time = local_time.astimezone(pytz.timezone('UTC'))
    utc_time_str = datetime.datetime.strftime(utc_time, '%Y-%m-%dT%H:%M:%SZ')
    return utc_time_str


# utc时间转本地时间
def utc_local(utc_time):
    local_time = utc_time.astimezone(pytz.timezone('Asia/Shanghai'))
    local_time_str = datetime.datetime.strftime(local_time, '%Y-%m-%d %H:%M:%S')
    return local_time_str


def get_data():
    target = []
    start_time = datetime.datetime.strptime(st, '%Y-%m-%d')
    end_time = datetime.datetime.strptime(et, '%Y-%m-%d')

    client = influxdb_client.InfluxDBClient(url='http://172.16.130.205:8092/',
                                            token='LRdIIW17oir2cDvCsrjZn1qvUOF5fFNwlqeqHGvg5LAv7pw-g_efZNbp7hhvV1aZwBecmMNgeE8dO9yPIPdLqA==',
                                            org='nari')
    query_api = client.query_api()
    query = 'from(bucket: "{}")\n  ' \
            '|> range(start: {}, stop: {})\n  ' \
            '|> filter(fn: (r) => r["device_id"] == "{}")' \
        .format(county_code, local_utc(start_time), local_utc(end_time), dev_no)
    print(query)
    result = query_api.query(org='nari', query=query)
    value_dict = {}
    for item in result:
        for info in item.records:
            utc_time = info['_time']
            local_time = utc_local(utc_time)
            value = info['_value']
            value_dict[local_time] = value
    print('\n\n')
    print(value_dict)

    temp_time = start_time
    while end_time > temp_time:
        time_value = []
        temp_time2 = temp_time
        for i in range(16):
            time_str = datetime.datetime.strftime(temp_time2, '%Y-%m-%d %H:%M:%S')
            if time_str in value_dict:
                time_value.append(value_dict[time_str])
            else:
                time_value.append(None)
            temp_time2 = temp_time2 + datetime.timedelta(minutes=15)
        target.append({
            'time': datetime.datetime.strftime(temp_time, '%Y-%m-%d %H:%M:%S'),
            'values': time_value
        })
        temp_time = temp_time + datetime.timedelta(minutes=15)

    with open('meter_power.json', 'w', encoding='utf-8') as target_file:
        json.dump(target, target_file, indent=4, ensure_ascii=False)
    target_file.close()


if __name__ == '__main__':
    get_data()
