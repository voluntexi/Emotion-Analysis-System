import jieba
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


st.title("自定义数据分析")
st.write("若已有Excel数据表，可在本模块上传Excel表进行可视化分析！")
uploaded_file = st.file_uploader("请选择文件(可多个)：", \
                                 accept_multiple_files=False, type=["xlsx", "xls"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file.read())
    st.dataframe(df)
    num = df.index.tolist()

    # 确保所有评论内容都是字符串类型
    comments = df['Comment_Content'].astype(str).tolist()

    # 合并评论字符串
    text = " ".join(comments)

    # 使用jieba进行分词
    cut_text = jieba.cut(text)
    result = " ".join(cut_text)

    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot()
    ax.plot(num, df['Comment_Value'])
    ax.set_xlabel('Comment_ID')
    ax.set_ylabel('Comment_Value')
    ax.set_title('Data Analysis')
    st.markdown('> Excel读取完毕！接下来进行可视化')
    st.markdown("* 用户情感分布")
    st.pyplot(fig)
    st.markdown("* 该话题用户情感")
    drawchart(df)

    word_cloud = WordCloud(font_path="/Users/simhei.ttf",  # 设置词云字体
                           background_color="white")  # 词云图的背景颜色)
    word_cloud.generate(result)
    plt.subplots(figsize=(16, 6))
    plt.imshow(word_cloud)
    plt.axis("off")
    st.pyplot(plt)

st.markdown('<hr>', unsafe_allow_html=True)
st.markdown('''



        <center> 基于Bert中文社交媒体的情感分析系统 </center> 

''', unsafe_allow_html=True)
