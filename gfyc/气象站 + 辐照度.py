import warnings

warnings.filterwarnings("ignore")
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta, timezone
from urllib.parse import quote_plus as urlquote

pwd = '1qaz@WSX'
mysql_url = f"mysql+pymysql://root:{urlquote(pwd)}@127.0.0.1:3306/gfyc?charset=utf8"
engine = create_engine(mysql_url)
from influxdb_client import InfluxDBClient

influxdb_url = "http://192.168.110.130:8086/"
influxdb_token = "VsE9zz62qm_DZKB6eib-hTSk1Ml-e8uF82Sqdbe5xnUJwOKshHFZCdMaiMa7Fqx_KD2iKmWCjg2u6XHTABcaSA=="

county_code = 3241106


def load_his(day, device_id, client):
    query_api = client.query_api()
    query_str = f'''
    from(bucket: "3241106")  
        |> range(start: {day}T00:00:00Z,stop: {day}T09:00:00Z)   
        |> filter(fn: (r) => r["device_id"] == "{device_id}") 
        |> drop(columns: ["_start", "_stop","_field","_measurement","device_id","meter_id","platform_id"])
    ''' + '|> map(fn:(r) => ({ r with _time: uint(v:r._time) })) '
    tmp = query_api.query_data_frame(query_str)
    if len(tmp) > 0:
        tmp = tmp[['_time', '_value']]
        tmp['_time'] = pd.to_datetime(tmp._time, utc=True)
        tmp['_value'] = abs(tmp['_value']) * 1000
        beijing = timezone(timedelta(hours=8))
        time_format = '%Y-%m-%d %H:%M:%S'
        tmp['time'] = [datetime.strptime(obj.astimezone(beijing).strftime(time_format), time_format) for obj in
                       tmp['_time']]
    return tmp


def load_forecast(day):
    forecast = pd.read_sql(
        f"select forecast,time from gfyc_shortforecast_qx_radiation where  id =3241106 and time between '{day} 00:00:00' and '{day} 23:59:00' ",
        engine, index_col="time")
    return forecast


from math import pow, sqrt
import numpy as np
from tqdm import tqdm

client = InfluxDBClient(url=influxdb_url, token=influxdb_token, timeout=100_00, enable_gzip=True, org="gs")


def calculate(day, device, forecast):
    dev_no = device['dev_no']
    inst_cap = float(device['inst_cap'])
    his = load_his(day, dev_no, client)
    per = float(device['per'])
    length1 = 0
    if len(his) == 0:
        rmse1 = 0
    else:
        try:
            vs = pd.merge(his, forecast, on='time')
            errors = []
            if len(vs) > 0:
                for i in range(len(vs)):
                    obj = vs.iloc[i]
                    v_actual = obj['_value']
                    v_forecast = obj['forecast'] * per
                    error = pow((v_forecast - v_actual) / (inst_cap * 1000), 2)
                    errors.append(error)
                rmse1 = 1 - sqrt(np.sum(errors) / len(errors))
            else:
                rmse1 = 0
        except Exception as e:
            print(e)
            print(forecast)
        length1 = len(errors)
    return dev_no, length1, rmse1


st = datetime(2023, 1, 1)
daybetween = [(st + timedelta(i)).strftime('%Y-%m-%d') for i in range(46)]
if __name__ == '__main__':
    for day in daybetween:
        ratio = pd.read_sql(
            f'select a.county_code,a.dev_no,a.resrc_supl_code,a.inst_cap,a.weather_grid_id,b.per from dwd_inst_cap a join pv_device_per_full b on a.dev_no=b.dev_no where a.county_code ={county_code} and a.inst_cap>0  and a.weather_grid_id>0',
            engine)
        dev_nos = []
        length = []
        rmses = []
        forecast = load_forecast(day)
        for j in tqdm(range(len(ratio))):
            device = ratio.iloc[j]
            forecast_curve = forecast
            dev_no1, length1, rmse1 = calculate(day, device, forecast_curve)
            dev_nos.append(dev_no1)
            length.append(length1)
            rmses.append(rmse1)
        pd.DataFrame({'dev_nos': dev_nos, 'length': length, 'rmses': rmses}).to_csv(
            f'qx_radion_{day}_{county_code}.csv')
