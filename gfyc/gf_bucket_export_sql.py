import requests
import datetime

url = '172.16.130.205:8092'
token = 'LRdIIW17oir2cDvCsrjZn1qvUOF5fFNwlqeqHGvg5LAv7pw-g_efZNbp7hhvV1aZwBecmMNgeE8dO9yPIPdLqA=='

headers = {
    'Accept': 'application/json',
    'Authorization': 'Token ' + token,
    'Content-Type': 'application/json'
}

bucket_list = []


def get_bucket_list(bucket_list_url):
    print(bucket_list_url)
    response = requests.get(bucket_list_url, headers=headers)
    result = response.json()
    for item in result['buckets']:
        if item['type'] == 'user' and item['name'].startswith("32"):
            bucket = {
                'id': item['id'],
                'name': item['name']
            }
            bucket_list.append(bucket)
            if 'labels' in item and len(item['labels']) > 0:
                bucket['label'] = item['labels'][0]['name']
    if 'next' in result['links']:
        next_url = 'http://{}{}'.format(url, result['links']['next'])
        get_bucket_list(next_url)


def genenrate_scirpt():
    start_time = datetime.datetime.now() + datetime.timedelta(days=-4)
    date_str = datetime.datetime.strftime(start_time, '%Y-%m-%d')
    if len(bucket_list) > 0:
        with open('influxdb_export.sh', mode='a') as f:
            for item in bucket_list:
                f.write(
                    '/usr/bin/influxd inspect export-lp --bucket-id {} --engine-path /influxdb/engine --output-path /tmp/export/{}.zip --start {}T00:00:00Z --compress\n'
                    .format(item['id'], item['name'], date_str))
        f.close()


if __name__ == "__main__":
    bucket_list_url = 'http://{}/api/v2/buckets?limit=100'.format(url)
    get_bucket_list(bucket_list_url)
    genenrate_scirpt()
