import re
import time
import pandas as pd
import requests
from datetime import datetime

import config

cookie = config.weibo_config().cookie  # 微博 cookie
allData = []
pdData = pd.DataFrame()
names = "weibo_comment"


def crawler(url):
    global allData
    id = url.split('/')[-1]
    mid = id
    allData, comment_num = getCommentInfo(id, mid)
    writeToExcel()


def getCommentInfo(id, mid):
    global cookie
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36",
        "cookie": cookie
    }
    microblog = []
    url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'.format(id, mid)
    comment_num = 0
    page = 1
    while True:
        res = requests.get(url, headers=headers)
        data = res.json()['data']
        max_id = data['max_id']
        user_info = data['data']
        for single_info in user_info:
            Retext = single_info['text']  # 评论
            user_id = single_info['user']['id']  # 用户id
            user_name = single_info['user']['screen_name']  # 用户名
            user_messagetime = single_info['created_at']  # 评论时间
            user_messagetime = getStandardTime(user_messagetime)
            if Retext is not None and Retext.strip():
                user_comment = [user_id, user_name, Retext, user_messagetime]
                microblog.append(user_comment)
                comment_num += 1
                print(f"正在爬取第{comment_num}条评论内容")
        time.sleep(1)
        if max_id != 0 or page > config.weibo_config().page:
            url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type=0'.format(id, mid, max_id)
        else:
            break
    return microblog, comment_num


def cleanData(df):
    comment = []
    for item in df['Comment_Content']:
        scriptRegex = "<script[^>]*?>[\\s\\S]*?<\\/script>"
        styleRegex = "<style[^>]*?>[\\s\\S]*?<\\/style>"
        htmlRegex = "<[^>]+>"
        spaceRegex = "\\s*|\t|\r|\n"
        item = re.sub(scriptRegex, '', str(item))  # 去除网址
        item = re.sub(styleRegex, '', str(item))
        item = re.sub(htmlRegex, '', str(item))
        item = re.sub(spaceRegex, '', str(item))
        item = re.sub('网页链接', '', str(item))
        comment.append(item)
    df['Comment_Content'] = comment


def getStandardTime(time):
    GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
    time = str(datetime.strptime(time, GMT_FORMAT)).split()
    simpleDate = time[0].split("-")
    year = simpleDate[0]
    month = simpleDate[1]
    day = simpleDate[2]
    return "{}-{}-{}".format(year, month, day)


def writeToExcel():
    print("爬取完成，正在写入Excel")
    global names
    global allData
    global pdData
    pdData = pd.DataFrame(allData)
    pdData.columns = ['Comment_ID', 'Comment_Name', 'Comment_Content', 'Comment_Time']
    cleanData(pdData)
    writer = pd.ExcelWriter('./crawledData/{}.xlsx'.format(names))
    pdData.to_excel(writer, sheet_name='cx', index=False)
    writer.save()
    writer.close()
    print("写入Excel成功")


def WeiboCrawler(url):
    crawler(url)
    return pdData

# WeiboCrawler("https://m.weibo.cn/detail/5143362977924156")
