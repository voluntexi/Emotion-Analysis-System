import os
import re
import sys
import time
from datetime import timedelta, datetime

import requests
import xlwt
import you_get
from selenium import webdriver
from selenium.webdriver.common.by import By
from you_get import common

'''
功能：爬取抖音ID、用户名、用户评论、视频、抖音标题
使用方法：
在def DouyinCrawler(url)函数中 输入爬取的网站url 即可实现信息的爬取
在爬取完毕后会将数据以EXCEL表的形式存入当前目录，命名为：DouyinComment.xls
视频会存放在video文件夹中
'''
# def require(url):
#     headers={
#         'path': '/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7083293845496073510&cursor=80&count=20&item_type=0&rcFT=&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=99.0.4844.51&browser_online=true&engine_name=Blink&engine_version=99.0.4844.51&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=0&webid=7082249047388145183&msToken=QWSrXp1LBsAJx5ebu3Xk7Ngwx3nHhQVsOCDXXYdq3e_pA-zZ9fJQjIUvVtcXRt1QsuhdrP-F47kapoadK_ZlMkYZbtgFHK6gO7Yvg5_FOLbVyvxugb_Azp-WjXGZ4w9q&X-Bogus=DFSzswVL9c0ANr98SlqafGUClL9E&_signature=_02B4Z6wo00001OaWiIgAAIDBzRzTTsCKJKzmlowAAFvuTAqjP5WE9ZlERwOQJsQRqw5IfPL3OR3ay.tAxct-hAEFfBTSSxfJPx4JOtmjEkqpbIbXVBKVk9.Q5JXAJ9XdKE.-VfGi5xy9Lrxg23',
#         'referer': 'https://www.douyin.com/search/%E6%88%90%E9%83%BD%E7%96%AB%E6%83%85%E6%9C%80%E6%96%B0%E6%B6%88%E6%81%AF?source=recom_search&aid=3e537954-a78f-4f98-8bd9-0c8b01cd977b&enter_from=search_result',
#         'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
#         'sec-fetch-mode': 'cors',
#         'sec-fetch-site': 'same-origin',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
#         'cookie': 'ttwid=1|3io6PeRHfVVAUN6jLN1TXOFMVh65YdBtttV1qoqxEng|1648964616|eac543ab7eea1375686ab59473ee6754c1ef3bc7411b26ae33a92c86aa002cc3; _tea_utm_cache_6383=undefined; home_can_add_dy_2_desktop=0; passport_csrf_token=93e4c5e474347189b777170b1ccc64dd; passport_csrf_token_default=93e4c5e474347189b777170b1ccc64dd; AB_LOGIN_GUIDE_TIMESTAMP=1648964616819; _tea_utm_cache_1300=undefined; ttcid=8af5c82ed80c4a968221424b5f80914439; _tea_utm_cache_2018=undefined; d_ticket=8ddc58068f79de4352e3d4746c998639f2c9d; n_mh=jh7oPlpGH3_DxYv2V0bXs9NyISDrORg0eWZZZCormJM; passport_auth_status=b822b5c6908a089fb594e86b928e8653,; passport_auth_status_ss=b822b5c6908a089fb594e86b928e8653,; sso_auth_status=300ee4c1042c535975d524908a93b2a5; sso_auth_status_ss=300ee4c1042c535975d524908a93b2a5; sso_uid_tt=894cd3b45425849eaf0c2b958cf81c05; sso_uid_tt_ss=894cd3b45425849eaf0c2b958cf81c05; toutiao_sso_user=5ecfe57eec37bd47206a241495d3ce01; toutiao_sso_user_ss=5ecfe57eec37bd47206a241495d3ce01; sid_ucp_sso_v1=1.0.0-KDZiZmJlMGZkYmYyOWI4ZTk2NDhkYmI5ZjU5M2ZjZjM0MDgxYzM4NGQKHwjYteDKvvXaBRCl6KSSBhjvMSAMMPir-u0FOAJA8QcaAmxmIiA1ZWNmZTU3ZWVjMzdiZDQ3MjA2YTI0MTQ5NWQzY2UwMQ; ssid_ucp_sso_v1=1.0.0-KDZiZmJlMGZkYmYyOWI4ZTk2NDhkYmI5ZjU5M2ZjZjM0MDgxYzM4NGQKHwjYteDKvvXaBRCl6KSSBhjvMSAMMPir-u0FOAJA8QcaAmxmIiA1ZWNmZTU3ZWVjMzdiZDQ3MjA2YTI0MTQ5NWQzY2UwMQ; odin_tt=27b3404a8fa9cd5fb1095f380da39fe97a3eeeb9174b45156afd9505b5009a7f7331b03da8573e1c00acb626c65866b917d54a64fd9e7501c27bb54a4c67e1d2; sid_guard=5ecfe57eec37bd47206a241495d3ce01|1648964646|5184000|Thu,+02-Jun-2022+05:44:06+GMT; uid_tt=894cd3b45425849eaf0c2b958cf81c05; uid_tt_ss=894cd3b45425849eaf0c2b958cf81c05; sid_tt=5ecfe57eec37bd47206a241495d3ce01; sessionid=5ecfe57eec37bd47206a241495d3ce01; sessionid_ss=5ecfe57eec37bd47206a241495d3ce01; sid_ucp_v1=1.0.0-KDdmNzliODI1MDExNDEzZTRhZDA5NzQ5NmM3Y2RiYTMyMTNmMzNjMGUKHwjYteDKvvXaBRCm6KSSBhjvMSAMMPir-u0FOAJA8QcaAmxxIiA1ZWNmZTU3ZWVjMzdiZDQ3MjA2YTI0MTQ5NWQzY2UwMQ; ssid_ucp_v1=1.0.0-KDdmNzliODI1MDExNDEzZTRhZDA5NzQ5NmM3Y2RiYTMyMTNmMzNjMGUKHwjYteDKvvXaBRCm6KSSBhjvMSAMMPir-u0FOAJA8QcaAmxxIiA1ZWNmZTU3ZWVjMzdiZDQ3MjA2YTI0MTQ5NWQzY2UwMQ; _tea_utm_cache_2285=undefined; _tea_utm_cache_1243=undefined; MONITOR_WEB_ID=8d20cb13-f4fc-4a22-9dab-85a7b93493e8; THEME_STAY_TIME=299514; IS_HIDE_THEME_CHANGE=1; douyin.com; strategyABtestKey=1649225120.677; s_v_web_id=verify_l1n620lp_YRNU3Odn_wVtD_4Ws3_8lD7_RwdRcTRwYZWg; pwa_guide_count=3; NEW_HOME_VIDEO_CONSUMPTION_COUNT=4; msToken=wkPUW3u6KKDxYGuVaK-AEAEJfl3wXAa0c8ePwrE4nWV32M1bQ5dKb-YkDaQR1m5yEGrEIr4P6POv7HG-PhgUQpJr9nx4DSij08Ittq8rlP3-AmN6vkAMEDbFBz6qgkKp2A==; __ac_nonce=0624d3d1a00953cd8ab53; __ac_signature=_02B4Z6wo00f01DXNH7AAAIDBHkdEdGD.S9A17RsAAG9F8GrCQr2PLClNqygxHbyS3AemvEq7dZy32SLuObmFxQW4zjFeYfypvfWg1KziDkynny5F-VXtoi4sOdXSPlb.yeLIy15yy6I9Yi2Zf2; msToken=tTcNHwBsSp7mOzEbcYQfcOZzjhHtDiXsxoYv9PpOH7v_-0cgLuYlqoAt1Be7-faktjiXBqKbhHTesLU7tmvANe0EFn-rHlP2C6IfjjtS71K7ULaisPbwrdO6OpmqDkm8; tt_scid=ngzzUNOfZJdMRly0Eo8LZTGyd1vsDShAMvb1cdgCn74v4IRd1mzrxmda3WX3wXSQ2523'
#     }
#
#     try:
#         r = requests.get(url, headers=headers)
#         r.raise_for_status()
#         print(url)
#         return r.text
#     except requests.HTTPError as e:
#         print(e)
#     except requests.RequestException as e:
#         print(e)
#     except:
#         print("Unknow error")
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
# def Html(html):
#     #     获取所需内容
#     s=json.loads(html)
#     comment=s['comments']
#     for i in comment:
#         floor = i['aweme_id']
#         ctime = time.strftime("%Y-%m-%d",time.localtime(i['create_time']))
#         username=i['user']['nickname']
#         content=i['text']
#         list=[]
#         list.append(floor)
#         list.append(username)
#         list.append(content)
#         list.append(ctime)
#         com.append(list)
def download(url):
    # word = input('请输入链接： ')
    # url = 'https://www.douyin.com/video/6967296943450066214?previous_page=main_page'
    directory = r'../video'
    filepath ='../video/DouyinVideo.mp4'
    if (os.path.exists(filepath)):
        os.remove(filepath)
    headers = {
        'path': '/aweme/v1/web/social/count?device_platform=webapp&aid=6383&channel=channel_pc_web&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Edge&browser_version=113.0.1774.42&browser_online=true&engine_name=Blink&engine_version=113.0.0.0&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100&webid=7236590732105041441&msToken=7AEOK668FP_u93H2HkVvcrY8vE2ChCJopqsluNCQy0Qwoo6sgNn-Tl_EjY_WzjZnwscrmsLqBwnj0uJND6Oy31TRoUVk_TxQdQ9kkd9qRdGEHAJE0DpmGU_mn32aU2g=&X-Bogus=DFSzswVOoVGAN9O9ttb0DbVX-1FV',
        'referer': 'https://www.douyin.com/search/%E6%88%90%E9%83%BD%E7%96%AB%E6%83%85%E6%9C%80%E6%96%B0%E6%B6%88%E6%81%AF?source=recom_search&aid=3e537954-a78f-4f98-8bd9-0c8b01cd977b&enter_from=search_result',
        'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42',
        'cookie': '__ac_nonce=0646d88fd00dbc3ae4fb; __ac_signature=_02B4Z6wo00f01FrzNpgAAIDCVNUhhXI3EMRa0zIAAHLY23; ttwid=1|EZCdW9T0wLCczheUSP2pCFu0lPHkPmHDxCOD5dM2oSo|1684900094|45d56ae09e318166d857cacc217ae40b6b1c8113fb5068ef9845b4c03aa0486d; strategyABtestKey="1684900097.426"; passport_csrf_token=49d350bbe3ace617ebc25452dec683d1; passport_csrf_token_default=49d350bbe3ace617ebc25452dec683d1; s_v_web_id=verify_li160l4d_W1dqLCwt_8czq_4OjM_B2YY_FjO88rMmBbqF; ttcid=beb652d31b89449a99d42b58e119ddaf37; d_ticket=0c2edb584f4daf7ada1fafbed7d7727d667c4; passport_assist_user=CkHy-mA0lMmmQy9EjquuuFS69q5EXTgmC92WmVgJZjR1PjNXRW_6Z89wdfnzOZi8gg-JRPkSorpo8-RoUyZNP092rxpICjyNdPRTDqlfWu7Equ6iUzyH-MVYDilemRDREgDRsr-nRXYjl0Zv_AhchBOGIWOLEDs92P-Aen1mdlrVsycQrPuxDRiJr9ZUIgEDdRc32A==; n_mh=jh7oPlpGH3_DxYv2V0bXs9NyISDrORg0eWZZZCormJM; sso_auth_status=6377494f29d353234bd120e12acb8cbc; sso_auth_status_ss=6377494f29d353234bd120e12acb8cbc; sso_uid_tt=2fe1164e8848b765d475b8801033b7e7; sso_uid_tt_ss=2fe1164e8848b765d475b8801033b7e7; toutiao_sso_user=b66839e7c6ace872f540aa7ca79a6560; toutiao_sso_user_ss=b66839e7c6ace872f540aa7ca79a6560; sid_ucp_sso_v1=1.0.0-KGRkMmM0M2Y2ZDk5MWM3NWUxNzkwODhjZDY2ZGFjZGM0MzkyYzljZGMKHwjYteDKvvXaBRCjkrajBhjvMSAMMPir-u0FOAJA8QcaAmhsIiBiNjY4MzllN2M2YWNlODcyZjU0MGFhN2NhNzlhNjU2MA; ssid_ucp_sso_v1=1.0.0-KGRkMmM0M2Y2ZDk5MWM3NWUxNzkwODhjZDY2ZGFjZGM0MzkyYzljZGMKHwjYteDKvvXaBRCjkrajBhjvMSAMMPir-u0FOAJA8QcaAmhsIiBiNjY4MzllN2M2YWNlODcyZjU0MGFhN2NhNzlhNjU2MA; odin_tt=6e0c59beb70a888ecd261a4d3279be40616063fa9735af30036b72febe702e1839754f4106effd8198d12cedf2848e4ea95163d5fe3fc4ceb52f394c3b070006; passport_auth_status=46e1264207b09ef99195b2e41bd995b1,e09d18b97649b7a97dc55ebb110d7eb5; passport_auth_status_ss=46e1264207b09ef99195b2e41bd995b1,e09d18b97649b7a97dc55ebb110d7eb5; uid_tt=90605064976429df2464c48a492e256e; uid_tt_ss=90605064976429df2464c48a492e256e; sid_tt=8553014024b46a5a89d52fbc9743be92; sessionid=8553014024b46a5a89d52fbc9743be92; sessionid_ss=8553014024b46a5a89d52fbc9743be92; publish_badge_show_info="0,0,0,1684900135352"; LOGIN_STATUS=1; msToken=9vP3hcJZ39kNSaexXLIUNxcuAi9QZZnW-VnxxRSsNOe_aP1NMTz2AehzNfc_6BOPLG7YGszBSeFBXOTsQZs9-Q07ZSn0xSnGL2eb7XGbpDqa4M1YwN9i91f6tscKBUc=; sid_guard=8553014024b46a5a89d52fbc9743be92|1684900136|5183998|Sun,+23-Jul-2023+03:48:54+GMT; sid_ucp_v1=1.0.0-KDQxYzVhZTlhMGUwNzI3ZmJjOWQxMzFjOTU0ODQ4N2NhOGZmZDUzNTUKGwjYteDKvvXaBRCokrajBhjvMSAMOAJA8QdIBBoCbGYiIDg1NTMwMTQwMjRiNDZhNWE4OWQ1MmZiYzk3NDNiZTky; ssid_ucp_v1=1.0.0-KDQxYzVhZTlhMGUwNzI3ZmJjOWQxMzFjOTU0ODQ4N2NhOGZmZDUzNTUKGwjYteDKvvXaBRCokrajBhjvMSAMOAJA8QdIBBoCbGYiIDg1NTMwMTQwMjRiNDZhNWE4OWQ1MmZiYzk3NDNiZTky; csrf_session_id=c8f006195b9b1ea7b0af23b32395f724; msToken=7AEOK668FP_u93H2HkVvcrY8vE2ChCJopqsluNCQy0Qwoo6sgNn-Tl_EjY_WzjZnwscrmsLqBwnj0uJND6Oy31TRoUVk_TxQdQ9kkd9qRdGEHAJE0DpmGU_mn32aU2g=; bd_ticket_guard_server_data=; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtY2xpZW50LWNlcnQiOiItLS0tLUJFR0lOIENFUlRJRklDQVRFLS0tLS1cbk1JSUNGRENDQWJxZ0F3SUJBZ0lVZmhxeWJWcHpIOENXMUNpeEYySDN2a0hGMDZBd0NnWUlLb1pJemowRUF3SXdcbk1URUxNQWtHQTFVRUJoTUNRMDR4SWpBZ0JnTlZCQU1NR1hScFkydGxkRjluZFdGeVpGOWpZVjlsWTJSellWOHlcbk5UWXdIaGNOTWpNd05USTBNRE0wT0RVeVdoY05Nek13TlRJME1URTBPRFV5V2pBbk1Rc3dDUVlEVlFRR0V3SkRcblRqRVlNQllHQTFVRUF3d1BZbVJmZEdsamEyVjBYMmQxWVhKa01Ga3dFd1lIS29aSXpqMENBUVlJS29aSXpqMERcbkFRY0RRZ0FFVUdaRHhlZ051UmhkMFFWWXVTZ1UydWV1UFlkdU0xOXUvYzkzTjgwUGdzWEpCZS9tOHRUc1J5WUNcbmpOZStRMVV2MTNaVzBUcW5wSmZuSHB4elIxWTRES09CdVRDQnRqQU9CZ05WSFE4QkFmOEVCQU1DQmFBd01RWURcblZSMGxCQ293S0FZSUt3WUJCUVVIQXdFR0NDc0dBUVVGQndNQ0JnZ3JCZ0VGQlFjREF3WUlLd1lCQlFVSEF3UXdcbktRWURWUjBPQkNJRUlNd055b2VtMEg4dVZvUnczVE50TzhQTzU4MTBrTFRwczRhMU5uQVRoSVhUTUNzR0ExVWRcbkl3UWtNQ0tBSURLbForcU9aRWdTamN4T1RVQjdjeFNiUjIxVGVxVFJnTmQ1bEpkN0lrZURNQmtHQTFVZEVRUVNcbk1CQ0NEbmQzZHk1a2IzVjVhVzR1WTI5dE1Bb0dDQ3FHU000OUJBTUNBMGdBTUVVQ0lGWStvVXFOZlNUV1c2Z0xcbm9vYlJyb2lKMFdZWFZHNTB5cUpiV2pHNWZJT0FBaUVBZ2FuL3d0TzQ1c21DeDZ3RWl1Q3AweDdvWlloTzVuUGZcblQ1QmZKVnMzemRnPVxuLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLVxuIn0=; store-region=cn-sn; store-region-src=uid; home_can_add_dy_2_desktop="1"; tt_scid=sr1z.Nhoj63H3AR2MPfh4TpiSkDtyP3XVgQeCwokIyU-K1qUHwy54j583ItdeIEr0b23; passport_fe_beating_status=false'    }
    response = requests.get(url=url, headers=headers)
    html_data = re.findall('src(.*?)%253D%2', response.text)[0]
    dem = requests.utils.unquote(html_data)
    video_url = html_data.replace('%2F', '/').replace('%22%3A%22', 'https:').replace('%3F', '?').replace('%26', '&')
    video_url = re.sub(r'.*https', 'https', video_url)
    video_url = video_url.replace('%3A',':')
    sys.argv = ['you-get','-o',directory,'-O','DouyinVideo','--no-caption',video_url]
    common.any_download(url=video_url, stream_id='mp4', info_only=False, output_dir=directory, merge=True)
    you_get.main()
def Douyinselenium(url):
    userData=[]
    driver = webdriver.Edge(executable_path=r'E:\毕业设计\soulstation-flask-master\msedgedriver.exe')
    driver.get(url)
    time.sleep(5)
    try:
        click = driver.find_element(by=By.XPATH,value='//*[@id="login-pannel"]/div[2]')
        click.click()
        time.sleep(0.5)
    except:
        print("没有该元素，正常爬取中")
    try:
        click2=driver.find_element(by=By.XPATH,value='/html/body/div[3]/div/div/div/div[2]')
        click2.click()
    except:
        print("没有该元素，正常爬取中")
    topic=driver.find_element(by=By.XPATH,value='/html/body/div[2]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div/div[1]/div/h1/span/span[2]/span/span/span/span/span').text
    driver.execute_script('window.scrollBy(0,2000)')

    for count in range(1, 21):
        id = str(count)
        comment = driver.find_element(by=By.XPATH,value=
            ' html / body / div[2] / div[1] / div[2] / div[2] / div / div[1] / div[5] / div / div / div[3] / div['+str(count)+'] / div / div[2] / \
                              div / p / span / span / span / span / span / span / span').text

        username = driver.find_element(by=By.XPATH,value=
            '/ html / body / div[2] / div[1] / div[2] / div[2] / div / div[1] / div[5] / div / div / div[3] /div[' + str(
                count) + ']/div / div[2] / div / div[1] / div[1] / div / a / span / span / span / span / span / span').text
        datetime1 = driver.find_element(by=By.XPATH,value=
            '/ html / body / div[2] / div[1] / div[2] / div[2] / div / div[1] / div[5] / div / div / div[3]/div[' + str(
                count) + ']/div / div[2] / div[1] / div[2] / span').text[:1]
        current_time = datetime.now()
        # 将当前时间格式化为"20xx-xx-xx"
        formatted_time = current_time.strftime("%Y-%m-%d")
        new_time = current_time - timedelta(days=int(datetime1))
        datetime1 = new_time.strftime("%Y-%m-%d")
        time.sleep(0.5)
        if len(username)==0:
            count-=1
        else:
            if len(comment)==0:
                comment="空"
            datetime1 = datetime1.replace('.', '-')
            single=[id, username ,comment ,datetime1]
            userData.append(single)
        driver.execute_script('window.scrollBy(0,150)')
    driver.quit()
    return userData,topic
def DouyinCrawler(url):
    # download(url)
    data,topic=Douyinselenium(url)
    save_afile(data,"douyin_comment")
    return topic
# DouyinCrawler("https://www.douyin.com/video/7235660321577356603")
