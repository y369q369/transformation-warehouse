import uuid
from tqdm import tqdm
import requests
import pymysql

'''
    香蕉视频测试
    接口：           
        分类首页：
            https://jpszdosq8an3q548x151.guoguoapps.com/vod/listing-0-0-0-0-0-0-0-0-0-1
            listing-0-0-0-0-0-0-0-0-0-1 中 十个数字分别对应 categories（类型）- areas（地区）- years（年份）- definitions（清晰度）- durations（规格）- freetypes（是否免费） - mosaics（有无马赛克）- langvoices（字幕语言）- orders（排序）- page（页码）
            sample_params: $cateid:0-$areaid:0-$yearid:0-$definition:0-$duration:0-$freetype:0-$mosaic:0-$langvoice:0-$orderby:0-$page:1
        频道首页：
            https://jpszdosq8an3q548x151.guoguoapps.com/special/listing-0-0-1
            sample_params:$sptype:0-$orderby:0-$page:1
        作者级：
            https://jpszdosq8an3q548x151.guoguoapps.com/special/detail/{spid}
            例：https://jpszdosq8an3q548x151.guoguoapps.com/special/detail/455
        观看视频：
            https://jpszdosq8an3q548x151.guoguoapps.com/vod/reqplay/{vodid}
            例：https://jpszdosq8an3q548x151.guoguoapps.com/vod/reqplay/51242，需要设置Cookie:  Cookie: xxx_api_auth=6662356335376234373135633535306330303266373732336235333333653461
        下载视频：
            https://jpszdosq8an3q548x151.guoguoapps.com/vod/reqdown/{vodid}
            例：https://jpszdosq8an3q548x151.guoguoapps.com/vod/reqdown/51242，需要设置Cookie:  Cookie: xxx_api_auth=6662356335376234373135633535306330303266373732336235333333653461
        单元测试")
'''

db = pymysql.connect(host='localhost', user='root', password='1qaz@WSX', database='video')
cursor = db.cursor()

definition_dict = {
    '3': '720',
    '4': '1080',
    '0': '普清',
    '1': '普清',
    '2': '普清',
    '6': '普清',
}


# 同步视频信息到数据库
def sync_video_info(pages):
    insert_video = []
    print('数据获取\t')
    for page in tqdm(range(1, pages + 1)):
        url = f"https://jpszdosq8an3q548x151.guoguoapps.com/vod/listing-0-0-0-0-0-0-0-0-0-{page}"
        response = requests.get(url)
        result = response.json()
        vodrows = result['data']['vodrows']
        for video in vodrows:
            tag = ''
            for index, item in enumerate(video['tags']):
                if index > 0:
                    tag += '、'
                tag += item['tagname']
            query_sql = f"select * from video_info where title = '{video['title']}' and tag = '{tag}'"
            cursor.execute(query_sql)
            data = cursor.fetchone()
            if data is None:
                author_str = ''
                for index, item in enumerate(video['actor_tags']):
                    if index > 0:
                        author_str += '、'
                    author_str += item['tagname']
                video['tag'] = tag
                video['author_str'] = author_str
                insert_video.append(video)
                print(video['title'] + '  新增')
            else:
                print(video['title'] + '  已存在')
    # if len(insert_video) > 0:
    #     insert_sql = f"insert into video_info(id, title, author, cate_name, definition, tag, download_url, play_url, " \
    #                  f"duration, score_num, year, area_name, mosaic, is_vip, download_flag) values "
    #     for index, video in enumerate(insert_video):
    #         mosaic = '无码' if video['mosaic'] == '2' else '有码'
    #         if index > 0:
    #             insert_sql += ', '
    #         insert_sql += f"('{uuid.uuid1().hex}', '{video['title']}', '{video['author_str']}', '{video['catename']}', '{definition_dict[video['definition']]}', '{video['tag']}', " \
    #                       f"'https://jpszdosq8an3q548x151.guoguoapps.com{video['down_url']}', 'https://jpszdosq8an3q548x151.guoguoapps.com{video['play_url']}', " \
    #                       f"'{video['duration']}', '{video['scorenum']}', '{video['yearname']}', '{video['areaname']}', '{mosaic}', '{video['isvip']}', 0)"
    #     cursor.execute(insert_sql)
    #     db.commit()
    #     print('实际插入' + str(cursor.rowcount) + '条')
    # else:
    #     print('所有视频都已存档')


# 更新视频下载地址
def sync_download_url():
    # todo 待验证
    query_sql = 'select * from video_info where download_flag = 0 order by score_num desc limit 10'
    cursor.execute(query_sql)
    result = cursor.fetchall()

    cookies_dict = {
        'Cookie': 'xxx_api_auth=6662356335376234373135633535306330303266373732336235333333653461'
    }
    update_list = []
    print('真实下载地址获取\t')
    for video in tqdm(result):
        resoponse = requests.get(video['download_url'], cookies=cookies_dict)
        data = resoponse.json()
        if data['retcode'] == 0:
            update_sql = f"update video_info set download_url = '{data['data']['httpurl']}', download_flag = 1 where id = '{video['id']}' and title = '{video['title']}'"
            update_list.append(update_sql)
    print(update_list)
    # if len(update_list) > 0:
    #     for update_sql in update_list:
    #         cursor.execute(update_sql)


if __name__ == '__main__':
    sync_video_info(40)
