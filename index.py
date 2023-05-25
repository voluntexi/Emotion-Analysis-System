import streamlit as st
st.title("社交网络舆情分析系统😊")
st.write("随着如今互联网的快速发展催生了网络数据爆炸式的增长，人们能够借助微博、抖音等国内主流的社交网络应用平台，"
         "对感兴趣的公众事件和突发事件自由发表谈吐、表达观点、交换意见。在分析网民的观点时候，面对大量数据的网页信息，"
         "设计出一个稳定、高效的情感分析系统实施互联网领域数据的收集、分析和可视化，通过人们对事件的的情绪使决策信得过、"
         "有支撑是一个具有现实意义的挑战。本项目以预训练语言模型BERT进行情感分析模型，力求实现一款特定领"
         "域的情感分析系统。")
st.markdown('<hr>', unsafe_allow_html=True)
st.markdown('''
本系统包含两个模块，本别是

* **数据获取模块(Get Data)**：在国内主流的社交媒体：微博、B站、抖音爬取用户评论数据
'''
            )
import streamlit as st
from PIL import Image
image = Image.open(r'E:\PythonProject\sentiment\img\img.png')
st.image(image)
st.markdown('''
* **数据分析模块(Data Analysis)**：对爬取的信息进行情感分析可视化
            ''')
image = Image.open(r'E:\PythonProject\sentiment\img\bert1.png')
st.image(image)
st.markdown('<hr>', unsafe_allow_html=True)
st.markdown('''



        <center> @voluntexi </center> 

''',unsafe_allow_html=True)