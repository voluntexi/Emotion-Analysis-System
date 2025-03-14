import time

import pandas as pd
import requests
import re
import json
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip

import config

'''
功能：爬取B站ID、用户名、用户评论
使用方法：
在def BilibiliCrawler(Old_url)函数中 输入爬取的网站链接 即可实现信息的爬取和视频的下载，下载路径为video/Bvideo.mp4
在爬取完毕后会将数据存入EXCEL表
'''
com = []
pdData = pd.DataFrame()

headers = {
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/134.0.0.0',
    'Accept': '*/*',
    'Content-Type': 'text/plain',
    'cookie': config.bilibili_config().cookie
}


def require(url):
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        print(url)
        return r.text
    except requests.HTTPError as e:
        print(e)
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknow error")


def Html(html):
    #     获取所需内容
    s = json.loads(html)
    for i in range(len(s['data']['replies'])):
        comment = s['data']['replies'][i]
        floor = comment['member']['mid']
        sex = comment['member']['sex']
        ctime = time.strftime("%Y-%m-%d", time.localtime(comment['ctime']))
        content = comment['content']['message']
        likes = comment['like']
        rcounts = comment['rcount']
        username = comment['member']['uname']
        content = comment['content']['message']
        list = []
        print(floor)
        list.append(floor)
        list.append(username)
        list.append(content)
        list.append(ctime)
        com.append(list)


def save_afile(alls, filename):
    """将一个评论数据保存在一个Excel文件中"""
    global pdData

    columns = ['Comment_ID', 'Comment_Name', 'Comment_Content', 'Comment_Time']
    df = pd.DataFrame(alls, columns=columns)
    excel_path = r'./crawledData/' + filename + '.xlsx'
    df.to_excel(excel_path, index=False)
    pdData = pd.read_excel(excel_path)


def biliVideo(url):
    headers = {
        'Referer': 'https://www.bilibili.com/video/BV1pm4y1t7SD/?spm_id_from=333.1007.tianma.1-1-1.click&vd_source=cda06a7ce9ff4de05dc61087d1875a03',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42'
    }
    url = url.partition('?')[0]
    print(url)
    print('获取中')
    response = requests.get(url, headers).text
    pattern = '<script>window\.__playinfo__=(.*?)</script>'
    list = re.findall(pattern, response, re.S)
    list_json = json.loads(list[0])
    title_pattern = '<span class="tit">(.*?)</span>'
    try:
        title = re.findall(title_pattern, response, re.S)[0]
    except:
        title = 'B站未知视频'
    video_url = list_json['data']['dash']['video'][0]['baseUrl']
    volume_url = list_json['data']['dash']['audio'][0]['baseUrl']
    print(title[0:6] + '获取成功，准备下载')
    video_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42',
        'cookie': config.bilibili_config().cookie,
        'referer': 'https://www.bilibili.com/v/dance/?spm_id_from=333.851.b_7072696d6172794368616e6e656c4d656e75.18'
    }
    video_param = {
        'accept_description': '360P 流畅',
        'accept_quality': 60,
    }
    print("视频url：" + video_url)
    print('-----开始下载-----')
    video = requests.get(url=video_url, headers=video_headers, params=video_param).content
    # with open('../video/'+r'.\B站{}.mp4'.format(title), 'wb') as f:
    with open('../video/BVideo.mp4', 'wb') as f:
        f.write(video)
        print('视频下载中')
    audio = requests.get(url=volume_url, headers=video_headers).content
    with open('./audio.mp3', 'wb') as f:
        f.write(audio)
    # print('-----视频合成中-----')
    # print('-----请耐心等候-----')
    # video_path = './B站视频.mp4'
    # videoclip = VideoFileClip(video_path)
    # audio_path = './audio.mp3'
    # audio = AudioFileClip(audio_path)
    # videoclip_3 = videoclip.set_audio(audio)
    # path = r'.\B站{}.mp4'.format(title[0:6])
    # videoclip_3.write_videofile(path)
    # import os
    # if os.path.exists(video_path):
    #     os.remove(video_path)
    # else:
    #     pass
    # if os.path.exists(audio_path):
    #     os.remove(audio_path)
    #     print('success!!!')
    # else:
    #     pass
    return title


def getOid(url):
    bv = re.findall('https://www.bilibili.com/video/(.*?)\/\?', url, re.S)[0]
    print(bv)
    resp = requests.get("https://www.bilibili.com/video/" + bv, headers=headers)
    obj = re.compile(r'"aid":(\d+).*?"bvid":"{bv}"'.format(bv=bv))
    oid = obj.search(resp.text).group(1)
    return oid


def BilibiliCrawler(url):
    # videoName=biliVideo(url)
    oid = getOid(url)
    print(oid)
    Old_url = 'https://api.bilibili.com/x/v2/reply?type=1&sort=1&oid=' + str(oid) + '&pn='
    e = 0
    page = 1
    while e == 0:
        url = Old_url + str(page)
        try:
            html = require(url)
            Html(html)
            page = page + 1
            time.sleep(3)
            if page > config.bilibili_config().page:
                break
        except:
            e = 1
    save_afile(com, "bilibili_comment")
    return pdData
# BilibiliCrawler("https://www.bilibili.com/video/BV1ag4y1F7x4/?spm_id_from=333.1007.tianma.1-2-2.click")
