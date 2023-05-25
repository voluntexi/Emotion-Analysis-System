# Emotion-Analysis-System
 使用BERT进行情感分析，使用Streamlit进行前端展示的情感分析系统

## 使用

* 1.安装所需要库

```
pip install -r requirements.txt
```

* 2.cmd 到项目目录下

```
 streamlit run .\main.py
```

## 功能

**GetData模块：**集成了对微博、bilibili、抖音网页版的数据爬取，包括(用户id，用户名，用户评论，评论时间)只需要输入所需爬取的URL即可进行爬取

**Data Analysis模块：**在完成爬取后，使用微调后的BERT模型进行情感值的计算，并进行可视化（折线图、饼状图、词云图）

**Excel Upload模块：**支持对用户自定义的Excel进行上传并进行可视化

⚠️用户上传的Excel表格列名需要和爬取后的Excel表形式相同，如下：

| Comment_ID | Comment_Name | Comment_Content | Comment_Time | Comment_Value |
| ---------- | ------------ | --------------- | ------------ | ------------- |
| xx         | xx           | xx              | xx           | xx            |

## 系统界面

![图片1](.\img\图片1.png)