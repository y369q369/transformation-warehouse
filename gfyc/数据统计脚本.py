# %%
import pandas as pd
import numpy as np

np.set_printoptions(suppress=True)
from statsmodels.formula.api import ols
from influxdb_client import InfluxDBClient
from multiprocessing import Pool
from sqlalchemy import create_engine
from datetime import datetime, timedelta, timezone
import warnings
from tqdm import tqdm

warnings.filterwarnings("ignore")
from urllib.parse import quote_plus as urlquote

influxdb_token = "VsE9zz62qm_DZKB6eib-hTSk1Ml-e8uF82Sqdbe5xnUJwOKshHFZCdMaiMa7Fqx_KD2iKmWCjg2u6XHTABcaSA=="
influxdb_url = "http://192.168.110.130:8086"
client = InfluxDBClient(url=influxdb_url, enable_gzip=True, token=influxdb_token, timeout=1000000, org="gs")
query_api = client.query_api()

pwd = '1qaz@WSX'
mysql_url = f"mysql+pymysql://root:{urlquote(pwd)}@127.0.0.1:3306/gfyc?charset=utf8"
init_engine = create_engine(mysql_url)
county_codes = [3241106]
time_format = '%Y-%m-%d %H:%M:%S'


# %%
def loadData(county_code, device_id):
    query_str = f'''
    from(bucket: "{county_code}")  
    |> range(start: -30d) 
    |> filter(fn: (r) => r["device_id"] == "{device_id}")
    |> drop(columns: ["_start", "_stop","_field","_measurement","device_id","meter_id","platform_id"])
    ''' + '|> map(fn:(r) => ({ r with _time: uint(v:r._time) })) '
    tmp = query_api.query_data_frame(query_str)
    count = len(tmp)
    if count > 0:
        tmp = tmp[['_time']]
        tmp['_time'] = pd.to_datetime(tmp._time, utc=True)
        beijing = timezone(timedelta(hours=8))
        time_format = '%Y-%m-%d %H:%M:%S'
        tmp['time'] = [datetime.strptime(obj.astimezone(beijing).strftime(time_format), time_format) for obj in
                       tmp['_time']]
        tmp['time_day'] = [str(obj)[0:10] for obj in tmp['time']]
        summary_df = tmp.groupby('time_day').count()
    t = [device_id for i in range(len(summary_df))], summary_df.index.values, summary_df['time'].values, [county_code
                                                                                                          for i in
                                                                                                          range(
                                                                                                              len(summary_df))]
    return t


def calculate(county_code):
    device_csv = pd.read_sql(f"select dev_no from dwd_cst_dygfyhsb_df where dev_no !='' and county_code={county_code} ",
                             init_engine)
    device_ids = list(device_csv['dev_no'].values)
    result = []
    for device_id in tqdm(device_ids):
        col_device_id, col_time_day, col_time_value, col_county_code = loadData(county_code, device_id, )
        a = pd.DataFrame(
            {'dev_no': col_device_id, 'time': col_time_day, 'value': col_time_value, 'county_code': col_county_code})
        result.append(a)
    pd.concat(result).to_sql('summary', init_engine, if_exists='append', index=False)


if __name__ == '__main__':
    for county_code in county_codes:
        calculate(str(county_code))
