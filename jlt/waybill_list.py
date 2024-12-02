""""""
import json
import requests

'''
    目标网址   ->    运单上报 ：https://bs.jilutong.com.cn/report/waybillreport
    功能      ->    获取 运单上报 轨迹数据
'''

headers = {
    'authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjcxYWUyOTljLWQ5MDItNDQyMy1hYmQ4LWJmZjM0N2IwZDFjZiJ9.IW0u0rR16npI7HvQrsZUHJHZ3B4iMOzmLpbESfYmXpbfSW0UqWDT0pGQgEtmZCnqpW4yXf718zdNcLzUEx2Wbw'}
encodings = 'gbk'


# 获取所有订单
def waybill_list(param):
    param['pageNum'] = 1
    param['pageSize'] = 100
    url = "https://bs.jilutong.com.cn/prod-api/tms/waybill/list"
    print('获取订单列表：页码 ' + str(param['pageNum']))
    response = requests.post(url=url, json=param, headers=headers)
    data = json.loads(response.content)
    waybill_data = []
    if data['code'] == 200:
        total = data['total']
        times = total // param['pageSize']
        if total % param['pageSize'] > 0:
            times += 1
        temp_list = data['rows']
        waybill_data.extend(temp_list)

        for i in range(times):
            param['pageNum'] = param['pageNum'] + 1
            print('获取订单列表：页码 ' + str(param['pageNum']))
            response = requests.post(url=url, json=param, headers=headers)
            data2 = json.loads(response.content)
            if data2['code'] == 200:
                temp_list2 = data2['rows']
                waybill_data.extend(temp_list2)
    return waybill_data


# 获取订单轨迹
def waybill_location(waybill):
    url = "https://bs.jilutong.com.cn/prod-api/tms/waybill/showTravelLocation"
    params = {
        'waybillId': waybill['waybillId']
    }
    response = requests.get(url=url, params=params, headers=headers)
    data = json.loads(response.content)
    if data['code'] == 200:
        waybill['gpsTrackList'] = [
            {k: v for k, v in item.items() if k in ['longitude', 'latitude', 'province', 'city', 'address', 'addTime']}
            for item in data['data']['gpsTrackList']]
        waybill['trackList'] = [
            {k: v for k, v in item.items() if k in ['waybillId', 'lat', 'lng', 'spd', 'drc', 'addTime']} for item in
            data['data']['trackList']]


# 导出为none转成"
def default_for_none(obj):
    if isinstance(obj, type(None)):
        return ""
    raise TypeError("Not serializable")


if __name__ == '__main__':
    waybill_param = {
        "waybillType": 0,
        "sendStatusJtb": 1
    }
    waybill_data = waybill_list(waybill_param)
    for index, waybill in enumerate(waybill_data):
        print(str(index + 1) + '\t-> 获取订单轨迹：' + waybill['waybillId'])
        waybill_location(waybill)
    with open('上报订单.json', 'w') as json_file:
        json.dump(waybill_data, json_file)

    # waybill = {
    #     'waybillId': '10ad9c5606c5470db59ad179d0362a26'
    # }
    # waybill_location(waybill)
    # with open('上报订单.json', 'w') as json_file:
    #     json.dump(waybill, json_file, default=default_for_none)
