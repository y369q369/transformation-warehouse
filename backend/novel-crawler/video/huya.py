import os
import requests
import parsel
import re  # 正则表达式模块 内置模块
from tqdm import tqdm

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36',
}

def create_direction(direction):
    if not os.path.exists(direction):
        os.makedirs(direction)

direction = 'huya/'
create_direction(direction)


def search_download(content, order = 'general'):
    """
    根据 关键词 搜索并下载
    :param content: 关键词
    :param order: 排序分类    general-综合排序  play-最多播放  news-最近更新
    """
    search_url = f'https://v.huya.com/search?w={content}&type=video&order={order}'
    response = requests.get(url=search_url, headers=headers)
    selector = parsel.Selector(response.text)
    search_result = selector.css('.search-result')
    if search_result:
        search_list = []
        pages = search_result.css('.pagination a')
        if pages:
            last_page = search_result.css('.pagination a:nth-last-of-type(2)::text').get()
            for i in range(2, int(last_page) + 1):
                search_page_url = f'{search_url}&p={i}'
                response = requests.get(url=search_page_url, headers=headers)
                selector = parsel.Selector(response.text)
                items = selector.css('.search-result .vhy-video-search-list li')
                for item in items:
                    search_list.append(handle_search_result(item))
        items = search_result.css('.vhy-video-search-list li')
        for item in items:
            search_list.append(handle_search_result(item))
        download_search_result(search_list)
    else:
        print(f'未查询到 {content} 相关信息')


def handle_search_result(item):
    """
    处理搜素结果
    :param item: 搜素结果
    """
    # 视频标题
    video_title = item.css('.video-wrap .video-title ::text').getall()
    # 视频地址
    video_url = 'https:' + item.css('.video-wrap::attr(href)').get()
    # 视频播放次数
    video_pnum = item.css('.video-wrap .video-info .video-times::text').get()
    # 视频时长
    video_duration = item.css('.video-wrap .video-info .video-duration::text').get()
    # 视频发布时间
    video_time = item.css('.video-meta .video-meta-time::text').get()
    # 视频作者
    video_user = item.css('.video-meta .video-meta-user::text').get()
    # 视频作者链接
    user_url = 'https:' + item.css('.video-meta .video-meta-user::attr(href)').get()

    return {
        'videoTitle': ''.join(video_title),
        'videoUrl': video_url,
        'videoPnum': video_pnum,
        'videoDuration': video_duration,
        'videoTime': video_time,
        'videoUser': video_user,
        'userUrl': user_url
    }


def download_search_result(search_list):
    """
    根据 搜索搜索结果 下载视频到本地
    :param search_list: 搜索结果集合
    """
    for info in tqdm(search_list):
        video_number = re.findall('https://v\.huya\.com/play/(.*?)\.html', info['videoUrl'])[0]
        print('    ' + info['videoTitle'])
        search_url = f'https://liveapi.huya.com/moment/getMomentContent?videoId={video_number}&_=1637824401148'
        response = requests.get(url=search_url, headers=headers)
        result = response.json()
        real_url = result['data']['moment']['videoInfo']['definitions'][0]['url']
        video_content = requests.get(url=real_url, headers=headers).content  # 获取二进制数据内容
        with open( direction + info['videoTitle'] + ' - ' + video_number + '.mp4', mode='wb') as f:
            f.write(video_content)
            f.close()


def download_one(video_number):
    """
    根据 视频编号 下载视频到本地
    :param video_number: 视频编号
    """
    search_url = f'https://liveapi.huya.com/moment/getMomentContent?videoId={video_number}&_=1637824401148'
    response = requests.get(url=search_url, headers=headers)
    result = response.json()
    real_url = result['data']['moment']['videoInfo']['definitions'][0]['url']
    video_title = result['data']['moment']['videoInfo']['videoTitle']
    video_content = requests.get(url=real_url, headers=headers).content  # 获取二进制数据内容
    with open( direction + video_title + ' - ' + video_number + '.mp4', mode='wb') as f:
        f.write(video_content)
        f.close()
    print(f'    {video_title} 下载完成')

if __name__ == '__main__':
    # 根据 关键词 搜索并下载
    # search_download('晴小兔')
    #
    # # 根据 视频编号 下载， 如： https://v.huya.com/play/598701523.html 对应的视频编号为 598701523
    # download_one('598701523')
    print("{\"adList\":{\"IsNeedTime\":\"0\",\"has_scene_info\":\"0\",\"item\":[{\"clickReportUrlOther\":{\"reportitem\":[]},\"display_code\":\"Empty\",\"duration\":\"\",\"image\":[{\"height\":\"0\",\"index\":\"0\",\"url\":\"\",\"vid\":\"\",\"width\":\"0\"}],\"is_empty\":1,\"link\":\"\",\"order_id\":\"1\",\"reportUrl\":\"https://rpt.gdt.qq.com/livemsg?chid=0&r90=1&pf=in&adtype=LD&lcount=1&dft_empty=1\",\"reportUrlOther\":{\"reportitem\":[]},\"reportUrlSDK\":{\"reportitem\":[]},\"reportUrlView\":{\"reportitem\":[]},\"shareable\":\"0\",\"type\":\"LD\",\"url\":\"\"},{\"clickReportUrlOther\":{\"reportitem\":[]},\"display_code\":\"Empty\",\"duration\":\"\",\"image\":[{\"height\":\"0\",\"index\":\"0\",\"url\":\"\",\"vid\":\"\",\"width\":\"0\"}],\"is_empty\":1,\"link\":\"\",\"order_id\":\"1\",\"reportUrl\":\"https://rpt.gdt.qq.com/livemsg?chid=0&r90=1&pf=in&adtype=KB&lcount=1&dft_empty=1\",\"reportUrlOther\":{\"reportitem\":[]},\"reportUrlSDK\":{\"reportitem\":[]},\"reportUrlView\":{\"reportitem\":[]},\"shareable\":\"0\",\"type\":\"KB\",\"url\":\"\"},{\"clickReportUrlOther\":{\"reportitem\":[]},\"display_code\":\"Empty\",\"duration\":\"\",\"image\":[{\"height\":\"0\",\"index\":\"0\",\"url\":\"\",\"vid\":\"\",\"width\":\"0\"}],\"is_empty\":1,\"link\":\"\",\"order_id\":\"1\",\"reportUrl\":\"https://rpt.gdt.qq.com/livemsg?chid=0&r90=1&pf=in&adtype=PVL&lcount=1&dft_empty=1\",\"reportUrlOther\":{\"reportitem\":[]},\"reportUrlSDK\":{\"reportitem\":[]},\"reportUrlView\":{\"reportitem\":[]},\"shareable\":\"0\",\"type\":\"PVL\",\"url\":\"\"}]},\"adLoc\":{\"adFlag\":0,\"add\":0,\"aid\":\"9\",\"aidInAdtype\":[{\"adid\":\"9\",\"adtype\":\"KB\"},{\"adid\":\"9\",\"adtype\":\"LD\"},{\"adid\":\"9\",\"adtype\":\"PVL\"}],\"breakTime\":null,\"duration\":141,\"iCheckLogin\":2,\"iCheckUser\":2,\"iUserTypeReq\":2,\"iVipInfoRsp\":2,\"isvip\":1,\"mult\":null,\"oaid\":\"9\",\"rfid\":\"03981228d83410ac5c93a51419bf79f9_1637895907\",\"tm\":1637895907,\"tpid\":3,\"tvAdFreeFlag\":0,\"vad\":null,\"vid\":\"u004004zfug\"}}\n")