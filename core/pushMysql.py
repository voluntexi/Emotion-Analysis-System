import pandas as pd
from sqlalchemy import create_engine
"""
功能：将对应的excel文件存储至mysql数据库中
def pushWeibo(): 为微博
def pushDouyin(): 为抖音
def pushBlibili(): 为B站
"""
def pushWeibo(filename):
    excelFile = filename+".xls"
    df = pd.DataFrame(pd.read_excel(excelFile))
    engine = create_engine("mysql+pymysql://root:password@localhost:3306/test?charset=utf8mb4", echo=False)
    df.to_sql(filename, con=engine, if_exists='append', index=False)
def pushDouyin(filename):
    excelFile = filename+".xls"
    df = pd.DataFrame(pd.read_excel(excelFile))
    engine = create_engine("mysql+pymysql://root:password@localhost:3306/test?charset=utf8mb4", echo=False)
    df.to_sql(filename, con=engine, if_exists='append', index=False)
def pushBlibili(filename):
    excelFile = filename+".xls"
    df = pd.DataFrame(pd.read_excel(excelFile))
    engine = create_engine("mysql+pymysql://root:password@localhost:3306/test?charset=utf8mb4", echo=False)
    df.to_sql(filename, con=engine, if_exists='append',index=False)
# pushBlibili('bilibili_comment')
pushWeibo('weibo_comment')
# pushDouyin('douyin_comment')
