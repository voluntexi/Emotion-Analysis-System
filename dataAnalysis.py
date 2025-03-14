import pandas as pd
import streamlit as st
import sys
import os

from matplotlib import pyplot as plt
from wordcloud import WordCloud

module_path = os.path.abspath('./core')
sys.path.append(module_path)
from WordCloud import wordFrequency
import addExcel


def drawchart(df):
    df['Sentiment'] = df['Comment_Value'].apply(lambda x: 'Negative' if x < 0 else 'Positive')
    # 统计情感分布
    sentiment_counts = df['Sentiment'].value_counts()
    fig = plt.figure(figsize=(16, 9))
    # 绘制饼状图
    ax = fig.add_subplot()
    ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%')
    ax.set_title('Topic sentiment distribution')

    # 显示图表
    st.pyplot(fig)


st.title("数据分析")
st.write("您已经完成了数据的获取，接下来进行数据的分析阶段吧！")
selected_platform = st.radio("选择数据分析源", ("(从下面三个按钮中开始选择）", "新浪微博", "Bilibili", "抖音"))
choose = ''
if selected_platform == "新浪微博":
    st.write("您选择了新浪微博")
    choose = 1
elif selected_platform == "Bilibili":
    st.write("您选择了Bilibili")
    choose = 2
elif selected_platform == "抖音":
    st.write("您选择了抖音")
    choose = 3
if choose != '':
    match choose:
        case 1:
            st.markdown("> 计算微博平台评论情感中...")
            filename = r"./crawledData/weibo_comment.xlsx"
            addExcel.WriteSenti(filename)
            res = 1
            df = pd.read_excel(filename)
            st.dataframe(df)
            num = []
            for j in range(len(df['Comment_ID'])):
                num.append(j)
            fig = plt.figure(figsize=(16, 9))
            ax = fig.add_subplot()
            ax.plot(num, df['Comment_Value'])
            ax.set_xlabel('Comment_ID')
            ax.set_ylabel('Comment_Value')
            ax.set_title('Data Analysis')
            st.markdown('> 情感计算完毕,接下来进行可视化')
            st.markdown("* 用户情感分布")
            st.pyplot(fig)
            st.markdown("* 该话题用户情感")
            drawchart(df)
            word = wordFrequency(filename)
            word_cloud = WordCloud(font_path="/Users/simhei.ttf",  # 设置词云字体
                                   background_color="white")  # 词云图的背景颜色)
            word_cloud.generate_from_frequencies(word)
            plt.subplots(figsize=(16, 6))
            plt.imshow(word_cloud)
            plt.axis("off")
            plt.show()
            st.markdown("* 词云图")
            st.pyplot(plt)
        case 2:
            st.markdown("> 计算bilibili平台评论情感")
            filename = r"./crawledData/bilibili_comment.xlsx"
            addExcel.WriteSenti(filename)
            res = 1
            df = pd.read_excel(filename)
            st.dataframe(df)
            num = []
            for j in range(len(df['Comment_ID'])):
                num.append(j)
            fig = plt.figure(figsize=(16, 9))
            ax = fig.add_subplot()
            ax.plot(num, df['Comment_Value'])
            ax.set_xlabel('Comment_ID')
            ax.set_ylabel('Comment_Value')
            ax.set_title('Data Analysis')
            st.markdown('> 情感计算完毕,接下来进行可视化')
            st.markdown("* 用户情感分布")
            st.pyplot(fig)
            st.markdown("* 该话题用户情感")
            drawchart(df)
            word = wordFrequency(filename)
            word_cloud = WordCloud(font_path="/Users/simhei.ttf",  # 设置词云字体
                                   background_color="white")  # 词云图的背景颜色)
            word_cloud.generate_from_frequencies(word)
            plt.subplots(figsize=(16, 6))
            plt.imshow(word_cloud)
            plt.axis("off")
            plt.show()
            st.markdown("* 词云图")
            st.pyplot(plt)

        case 3:
            st.markdown("> 计算抖音平台评论情感")

            filename = r"./crawledData/douyin_comment.xlsx"
            addExcel.WriteSenti(filename)
            res = 1

            df = pd.read_excel(filename)
            st.dataframe(df)
            num = []
            for j in range(len(df['Comment_ID'])):
                num.append(j)

            fig = plt.figure(figsize=(16, 9))
            ax = fig.add_subplot()
            ax.plot(num, df['Comment_Value'])
            ax.set_xlabel('num')
            ax.set_ylabel('Value')
            ax.set_title('Data Analysis')
            st.markdown('> 情感计算完毕,接下来进行可视化')
            st.markdown("* **用户情感分布**")
            st.pyplot(fig)
            st.markdown("* **该话题用户情感**")
            drawchart(df)
            word = wordFrequency(filename)
            word_cloud = WordCloud(font_path="/Users/simhei.ttf",  # 设置词云字体
                                   background_color="white")  # 词云图的背景颜色)
            word_cloud.generate_from_frequencies(word)
            plt.subplots(figsize=(16, 6))
            plt.imshow(word_cloud)
            plt.axis("off")
            plt.show()
            st.markdown("* **词云图**")
            st.pyplot(plt)
st.markdown('<hr>', unsafe_allow_html=True)
st.markdown('''



        <center> 基于Bert中文社交媒体的情感分析系统 </center> 

''', unsafe_allow_html=True)
