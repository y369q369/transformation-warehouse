""""""
import json
import requests
import csv

'''
    目标网址   ->    运单上报 ：https://bs.jilutong.com.cn/report/waybillreport
    功能      ->    获取 运单上报 轨迹数据
'''

headers = {
    'authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjZlMDEwNzc2LWY4ZTYtNGY3MC1iOWFmLTllMGFiZWNkMGJkMyJ9.fvCXiiXmSPgHxEa8XBUjF1yckdEM5u7Njd1En3xjkI4TAZEFy1L8RCb_nq_pkD8rQ9AJJXXnRuuihtWeae0FTw'
}
encodings = 'gbk'


# 获取所有订单
def waybill_list(param):
    param['pageNum'] = 1
    param['pageSize'] = 100
    url = "https://bs.jilutong.com.cn/prod-api/tms/waybill/list"
    print('获取订单列表：页码 ' + str(param['pageNum']))
    response = requests.post(url=url, json=param, headers=headers)
    response.encoding = encodings
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
            response.encoding = encodings
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
    response.encoding = encodings
    data = json.loads(response.content)
    if data['code'] == 200:
        waybill['gpsTrackList'] = [
            {k: v for k, v in item.items() if k in ['longitude', 'latitude', 'province', 'city', 'address', 'addTime']}
            for item in data['data']['gpsTrackList']]
        waybill['trackList'] = [
            {k: v for k, v in item.items() if k in ['waybillId', 'lat', 'lng', 'spd', 'drc', 'addTime']} for item in
            data['data']['trackList']]


# 将json转成csv文件
def json2csv(data):
    result_order = []
    result_vehicle = []
    result_driver = []
    result_order.append(['订单编号', '建单人', '托运方', '收货人', '司机姓名', '司机手机号', '车牌号', '发运地', '收货地', '行驶里程(公里)', '预计时间（分钟）', '货物', '重量（KG）', '装货吨数', '卸货吨数', '建单时间', '发货时间', '到达时间', '支付时间', '应付', '应收', '服务费', '预付', '押金'])
    result_vehicle.append(['订单编号', '建单人', '托运方', '收货人', '司机姓名', '司机手机号', '车牌号', '发运地', '收货地', '行驶里程(公里)', '预计时间（分钟）', '货物', '重量（KG）', '装货吨数', '卸货吨数', '建单时间', '发货时间', '到达时间', '支付时间', '应付', '应收', '服务费', '预付', '押金', '精度-车辆轨迹点', '纬度-车辆轨迹点', '速度-车辆轨迹点', '方向-车辆轨迹点', '定位时间-车辆轨迹点'])
    result_driver.append(['订单编号', '建单人', '托运方', '收货人', '司机姓名', '司机手机号', '车牌号', '发运地', '收货地', '行驶里程(公里)', '预计时间（分钟）', '货物', '重量（KG）', '装货吨数', '卸货吨数', '建单时间', '发货时间', '到达时间', '支付时间', '应付', '应收', '服务费', '预付', '押金', '精度-司机轨迹点', '纬度-司机轨迹点', '定位时间-司机轨迹点'])
    for item in data:
        order = [item['waybillSn'], item['partyaName'], item['updateBy'], item['thrCompany'], item['driverName'], item['driverPhone'], item['carNo'], item['startCity'], item['endCity'], item['distance'], item['duration'], item['goodsName'], item['goodsWeight'], item['sendWeight'], item['loadWeight'], item['addTime'], item['sendTime'], item['arrivedTime'], item['payTime'], item['freightCharge'], item['acctualAmount'], '0.00', 0, 0]
        for vehicle in item['trackList']:
            temp = [vehicle['lng'], vehicle['lat'], vehicle['spd'], vehicle['drc'], vehicle['addTime']]
            order_vehicle = []
            order_vehicle.extend(order)
            order_vehicle.extend(temp)
            result_vehicle.append(order_vehicle)
        for driver in item['gpsTrackList']:
            temp = [driver['longitude'], driver['latitude'], driver['addTime']]
            order_driver = []
            order_driver.extend(order)
            order_driver.extend(temp)
            result_driver.append(order_driver)
        result_order.append(order)
    with open('上报订单.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in result_order:
            writer.writerow(row)
        csvfile.close()
    with open('上报订单-司机轨迹点.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in result_driver:
            writer.writerow(row)
        csvfile.close()
    with open('上报订单-车辆轨迹点.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in result_vehicle:
            writer.writerow(row)
        csvfile.close()


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
        json_file.close()

    # with open('上报订单.json', 'r', encoding='utf-8') as json_file:
    #     data = json.load(json_file)
    #     json_file.close()
    # json2csv(data)

    # waybill = {
    #     'waybillId': '10ad9c5606c5470db59ad179d0362a26'
    # }
    # waybill_location(waybill)
    # with open('上报订单.json', 'w') as json_file:
    #     json.dump(waybill, json_file, default=default_for_none)
