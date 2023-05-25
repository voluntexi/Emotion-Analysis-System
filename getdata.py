import pandas as pd
import streamlit as st
import sys
import os
module_path = os.path.abspath('./core')
sys.path.append(module_path)
import BilibiliCrawler
import DouyinCrawler
import WeiboCrawler
st.title("数据获取")
st.markdown(
'''
网址示例：
>  抖音：https://www.douyin.com/video/7235660321577356603 

>  哔哩哔哩：https://www.bilibili.com/video/BV1ag4y1F7x4/?spm_id_from=333.1007.tianma.1-2-2.click

>  微博：https://weibo.cn/comment/N237vrijo?uid=2803301701&rl=0&gid=10001#cmtfrm

'''
)
st.write("我们提供了从微博、B站、抖音三个社交网站中爬取数据的功能，只需要输入需要爬取的微博\视频的网址就可以进行爬取了")
st.write("接下来开始选择吧！")
st.title("数据爬取选择")
selected_platform = st.radio("选择数据爬取平台", ("(从下面三个按钮中开始选择）","新浪微博", "Bilibili", "抖音"))
choose=''
if selected_platform == "新浪微博":
    st.write("您选择了新浪微博")
    choose=1
elif selected_platform == "Bilibili":
    st.write("您选择了Bilibili")
    choose = 2
elif selected_platform == "抖音":
    st.write("您选择了抖音")
    choose = 3
url=st.text_input('输入爬取的网址')
res=0
if url!='' and choose!='':
    st.write("开始爬取中...")
    match choose:
        case 1:
            WeiboCrawler.WeiboCrawler(url)
            st.write("爬取完毕！数据如下")
            filename = "weibo_comment.xls"
            df = pd.read_excel(filename)
            st.dataframe(df)
            res=1
        case 2:
            BilibiliCrawler.BilibiliCrawler(url)
            st.write("爬取完毕！数据如下")
            filename = "bilibili_comment.xls"
            df = pd.read_excel(filename)
            st.dataframe(df)
            res = 1

        case 3:
            DouyinCrawler.DouyinCrawler(url)
            st.write("爬取完毕！数据如下")
            filename = "douyin_comment.xls"
            df = pd.read_excel(filename)
            st.dataframe(df)
            res = 1

if res==1:
    st.write("数据抓取完毕！接下来点击左边菜单栏进入进行可视化模块")

st.markdown('<hr>', unsafe_allow_html=True)
st.markdown('''



        <center> @voluntexi </center> 

''',unsafe_allow_html=True)
