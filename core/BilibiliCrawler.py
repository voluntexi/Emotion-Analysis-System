import time
import xlwt
import requests
import re
import json

from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip

'''
功能：爬取B站ID、用户名、用户评论
使用方法：
在def BilibiliCrawler(Old_url)函数中 输入爬取的网站链接 即可实现信息的爬取和视频的下载，下载路径为video/Bvideo.mp4
在爬取完毕后会将数据以EXCEL表的形式存入当前目录，命名为：BilibiliComment.xls
'''
com=[]
def require(url):
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'cookie': "buvid3=E2E2C851-EDAB-C924-53D0-50743CC4687D59102infoc; b_nut=1680785359; i-wanna-go-back=-1; _uuid=ED84EF4F-7C7A-11B1-1F44-9A109C58D883865842infoc; CURRENT_PID=718c9290-d47a-11ed-9e38-0d2efb842159; rpdid=|(um|)mY~Y~Y0J'uY)|~)l~)); header_theme_version=CLOSE; nostalgia_conf=-1; FEED_LIVE_VERSION=V8; buvid_fp_plain=undefined; SESSDATA=47221def,1696857033,8621b*42; bili_jct=e23dbe33f46514b69c24d75729b28814; DedeUserID=397563377; DedeUserID__ckMd5=47ff0a8a3c14924a; b_ut=5; CURRENT_QUALITY=80; CURRENT_FNVAL=16; bp_article_offset_397563377=781455104870973400; LIVE_BUVID=AUTO1216844191034632; fingerprint=d66651272fecfb18425de2886215198e; buvid_fp=c4c484ba303535a990061726b5662582; bp_video_offset_397563377=798858483922370600; b_lsid=D7E1672A_1884BB1954E; home_feed_column=4; browser_resolution=1042-929; sid=6r1sesfu; innersign=1; buvid4=4BD16C3F-7BB1-F74C-DDE0-267A56CF337561141-023040620-Z3wd+s28v3UcpokzmdN1hA=="   }
    try:
        r=requests.get(url,headers=headers)
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
    s=json.loads(html)
    for i in range(len(s['data']['replies'])):
        comment=s['data']['replies'][i]
        floor = comment['member']['mid']
        sex=comment['member']['sex']
        ctime = time.strftime("%Y-%m-%d",time.localtime(comment['ctime']))
        content = comment['content']['message']
        likes = comment['like']
        rcounts = comment['rcount']
        username=comment['member']['uname']
        content=comment['content']['message']
        list=[]
        print(floor)
        list.append(floor)
        list.append(username)
        list.append(content)
        list.append(ctime)
        com.append(list)
def save_afile(alls,filename):
    """将一个评论数据保存在一个excle"""
    f=xlwt.Workbook()
    sheet1=f.add_sheet(u'sheet1',cell_overwrite_ok=True)
    sheet1.write(0,0,'Comment_ID')
    sheet1.write(0,1,'Comment_Name')
    sheet1.write(0,2,'Comment_Content')
    sheet1.write(0,3,'Comment_Time')
    i=1
    for data in alls:
        for j in range(len(data)):
            sheet1.write(i,j,data[j])
            # print(i,j,data[j])
        i=i+1
    f.save(filename+'.xls')
def biliVideo(url):
    headers = {
        'Referer': 'https://www.bilibili.com/video/BV1pm4y1t7SD/?spm_id_from=333.1007.tianma.1-1-1.click&vd_source=cda06a7ce9ff4de05dc61087d1875a03',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42'
    }
    url=url.partition('?')[0]
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
        'cookie': "buvid3=E2E2C851-EDAB-C924-53D0-50743CC4687D59102infoc; b_nut=1680785359; i-wanna-go-back=-1; _uuid=ED84EF4F-7C7A-11B1-1F44-9A109C58D883865842infoc; CURRENT_PID=718c9290-d47a-11ed-9e38-0d2efb842159; rpdid=|(um|)mY~Y~Y0J'uY)|~)l~)); header_theme_version=CLOSE; nostalgia_conf=-1; FEED_LIVE_VERSION=V8; buvid_fp_plain=undefined; SESSDATA=47221def,1696857033,8621b*42; bili_jct=e23dbe33f46514b69c24d75729b28814; DedeUserID=397563377; DedeUserID__ckMd5=47ff0a8a3c14924a; b_ut=5; CURRENT_QUALITY=80; CURRENT_FNVAL=16; bp_article_offset_397563377=781455104870973400; LIVE_BUVID=AUTO1216844191034632; fingerprint=d66651272fecfb18425de2886215198e; buvid_fp=c4c484ba303535a990061726b5662582; bp_video_offset_397563377=798858483922370600; b_lsid=D7E1672A_1884BB1954E; home_feed_column=4; browser_resolution=1042-929; sid=6r1sesfu; innersign=1; buvid4=4BD16C3F-7BB1-F74C-DDE0-267A56CF337561141-023040620-Z3wd+s28v3UcpokzmdN1hA==",
        'referer': 'https://www.bilibili.com/v/dance/?spm_id_from=333.851.b_7072696d6172794368616e6e656c4d656e75.18'
    }
    video_param = {
        'accept_description': '360P 流畅',
        'accept_quality': 60,
    }
    print("视频url："+video_url)
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
    resp = requests.get("https://www.bilibili.com/video/" + bv)
    obj = re.compile(f'"aid":(?P<id>.*?),"bvid":"{bv}"')  # 在网页源代码里可以找到id，用正则获取到
    oid = obj.search(resp.text).group('id')
    return oid
def BilibiliCrawler(url):
    # videoName=biliVideo(url)
    oid=getOid(url)
    print(oid)
    Old_url = 'https://api.bilibili.com/x/v2/reply?type=1&sort=1&oid=' + str(oid) + '&pn='
    e=0
    page=1
    while e == 0 :
        url = Old_url+str(page)
        try:
            html=require(url)
            Html(html)
            page=page+1
            time.sleep(3)
            if page>30:
                break
        except:
            e=1
    save_afile(com,"bilibili_comment")
    # return videoName
# BilibiliCrawler("https://www.bilibili.com/video/BV1ag4y1F7x4/?spm_id_from=333.1007.tianma.1-2-2.click")
