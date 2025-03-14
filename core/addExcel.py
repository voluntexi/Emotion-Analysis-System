import pandas as pd
import sentiAnalysis

'''
功能：读取excel表中用户的评论，计算出每个评论的具体情感值，然后写入excel表中
使用：def WriteSenti(filename): 参数为excel的文件名
'''


def excelwrite(filename, singleEmo):
    df = pd.read_excel(filename)
    if "Comment_Value" in df.columns:
        print("已经存在情感值")
    else:
        df["Comment_Value"] = singleEmo
        df.to_excel(filename, index=False)


def WriteSenti(filename):
    df = pd.read_excel(filename)
    comments = df.iloc[:, 2].tolist()
    singleEmo = sentiAnalysis.singleSentiment(comments)
    print("总的情感值为：" + str(sum(singleEmo) / len(singleEmo)))
    excelwrite(filename, singleEmo)
    return singleEmo


def readExcel(filename):
    df = pd.read_excel(filename)
    return df.values.tolist()
