import time

import requests
import datetime
import pandas as pd
import config

names = "douyin_comment"
pdData = pd.DataFrame()

def get_data(id):
    nickname_list = []
    user_id_list = []
    comment_time_list = []
    content_list = []
    page = 0

    url = 'https://www.douyin.com/aweme/v1/web/comment/list/'
    headers = {
        'cookie': config.douyin_config().cookie,
        'referer': 'https://www.douyin.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/10',
    }

    while True:
        # 请求参数
        params = {
            "device_platform": "webapp",
            "aid": 6383,
            "channel": "channel_pc_web",
            "aweme_id": id,
            "cursor": page * 20,
            "count": 20,
            "item_type": 0,
            "insert_ids": "",
            "whale_cut_token": "",
            "cut_version": 1,
            "rcFT": "",
            "pc_client_type": 1,
            "version_code": 170400,
            "version_name": "17.4.0",
            "cookie_enabled": True,
            "screen_width": 1235,
            "screen_height": 823,
            "browser_language": "zh-CN",
            "browser_platform": "Win32",
            "browser_name": "Chrome",
            "browser_version": "109.0.0.0",
            "browser_online": True,
            "engine_name": "Blink",
            "engine_version": "109.0.0.0",
            "os_name": "Windows",
            "os_version": "10",
            "cpu_core_num": 16,
            "device_memory": 8,
            "platform": "PC",
            "downlink": 7.2,
            "effective_type": "4g",
            "round_trip_time": 150,
            "webid": "7208902085361960506",
            "msToken": "VjT914ox94y25sviLBEH1agIm_VfbCOKYwvc3jZjUgGoKdR7NdPAMefyNWXH7d29zI9HpiMG6eo2DK4tRM32Zg3fZByGIDn412Mg3cpF6FqSWhcdsZTvvtJmU8E1GGIF",
            "X-Bogus": "DFSzswVuGvUANndftbv0TBt/pLwG"
        }
        response = requests.get(url=url, params=params, headers=headers)
        json_data = response.json()
        comments = json_data['comments']
        if comments is None:
            data_save(nickname_list, user_id_list, comment_time_list, content_list)
            break

        print('正在爬取第 {} 页'.format(page))
        for comment in comments:
            list_append1(nickname_list, user_id_list, comment_time_list, content_list, comment)

        # 判断父级评论是否爬取完成
        if int(json_data['has_more']):
            page += 1
            if page >= config.douyin_config().page:
                data_save(nickname_list, user_id_list, comment_time_list, content_list)
                break
            continue
        else:
            data_save(nickname_list, user_id_list, comment_time_list, content_list)
            break
        time.sleep(1)


def list_append1(nickname_list, user_id_list, comment_time_list, content_list, comment):
    if comment['text'] is not None and comment['text'].strip():
        nickname_list.append(comment['user']['nickname'])
        user_id_list.append(comment['user']['uid'])
        content_list.append(comment['text'])
        comment_time_list.append(datetime.datetime.fromtimestamp(int(comment['create_time'])).strftime("%Y-%m-%d"))


def data_save(nickname_list, user_id_list, comment_time_list, content_list):
    global pdData
    pdData = pd.DataFrame(
        {
            'Comment_ID': user_id_list,
            'Comment_Name': nickname_list,
            'Comment_Content': content_list,
            'Comment_Time': comment_time_list,
        }
    )
    writer = pd.ExcelWriter('./crawledData/{}.xlsx'.format(names))
    pdData.to_excel(writer, sheet_name='cx', index=False)
    writer.save()
    writer.close()
    print("写入Excel成功")


def DouyinCrawler(url):
    id = url.split('/')[-1]
    get_data(id)
    return pdData

# DouyinCrawler("https://www.douyin.com/video/7235660321577356603")
