#coding='utf-8'
import time
import re
import requests
import xlwt
import os
import time as t
import random
import numpy as np	
import datetime
import urllib3
'''
功能：爬取微博用户ID、Comment_Name、用户评论 以及微博的原文
使用方法：
在WeiboCrawler(url):函数中 输入爬取的网站的网址 即可实现信息的爬取
在爬取完毕后会将数据以EXCEL表的形式存入当前目录，命名为：WeiboComment.xls
同时会返回该微博原文，以字符串的形式返回
'''
urllib3.disable_warnings()#消除警告信息
#随机cookie
cookie_1='_T_WM=69c4e58b06421720acabaa780bb7cd58; SUB=_2A25JaQlYDeRhGeVH6FQU8SnJyTmIHXVqlZcQrDV6PUJbkdANLXDQkW1NT0hDh0TqoA05ST9VGORg3Z7iSYNZIgjY; SCF=Ah49Zdz2iFtZYZf2w2nZAQpilZJirFLfzllP-KvmZgCuIcklvUn9WORwJx9O2WKfjEMxjFNdK3wYPQe9fs_5nAU.; SSOLoginState=1684896008'#两种标头 中文版和英文版
headers_1 = {
				  'Accept-Encoding': 'gzip, deflate, br',
				 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
				 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.36',
				'Accept': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1 Edg/113.0.0.0',
				'Referer': 'https://weibo.cn/comment/LncH85pAQ?uid=2803301701&rl=0&gid=10001&page=2',
			    'Connection': 'keep-alive',
				'Cookie': cookie_1,
				}

headers_list=[headers_1,headers_1]#列表
topic=""
def require(url,headers):
	"""获取网页源码"""
	while True:
		try:
			response = requests.get(url, headers=headers,timeout=(20,50),verify=False)
			code_1=response.status_code
			if code_1==200:
				print('正常爬取中，状态码：'+str(code_1))#状态码
				t.sleep(random.randint(1,2))
				break
			else:
				print('请求异常，重试中，状态码为：'+str(code_1))#状态码
				t.sleep(random.randint(10,15))
				continue
		except:
			t.sleep(random.randint(2,3))
			continue
	html=response.text#源代码文本
	return html

def html_1(url,headers):#返回网页源码和评论页数
	html=require(url,headers)
	try:
		page=re.findall('&nbsp;1/(.*?)页',html,re.S)
		page=int(page[0])

	except:
		page=0
	#page=re.findall('<input name="mp" type="hidden" value="(.*?)">',html,re.S)
	return html,page

def count(alls):
	n=0
	for all in alls:
		for i in all:
			n=n+1
	return n

def body(h_1,j):#提取主体
	global topic
	html_2=re.findall('<div class="c" id="C.*?">(.*?)</div>',str(h_1),re.S)
	if(j==1):
		topic=re.findall('<span class="ctt">:.*?</span>',str(h_1),re.S)[0]
		topic = topic.replace('<br/>', '')
		topic = topic.replace('</span>:', '')
		topic = topic.replace('</a>', '')
		topic = re.findall(r'<span class="ctt">:(.+?)</span>', topic)[0]
		topic=re.sub('<a href=".*?">',"",topic)
		topic=re.sub("<a href='.*?'","",topic)
		topic=re.sub("<.*?>","",topic)
		topic=re.sub('<',"",topic)
		topic=re.sub('>',"",topic)
	html_2=str(html_2)
	# print(html_2)
	user_ids=re.findall('<a href=".*?&amp;fuid=(.*?)&amp;.*?">举报</a> ',html_2,re.S)#从举报链接入手
	
	names_0=re.findall('<a href=.*?>(.*?)</a>',html_2,re.S)
	names=[]#Comment_Name
	ma=[ '举报', '赞[]', '回复']
	pattern = re.compile(r'\d+')#匹配数字
	for i in names_0:
		i=re.sub(pattern, "", i)
		if i not in ma:
			if '@' not in i:
				names.append(i)

	pattern_0= re.compile(r'回复<a href=.*?</a>:')#匹配回复前缀
	pattern_0_1= re.compile(r'<a href=.*?</a>')#匹配回复内容后面的表情图片地址
	pattern_0_2= re.compile(r'<img alt=.*?/>')#匹配回复内容的图片地址
	contents=[]#Comment_Content
	contents_2=[]#Comment_Content初步
	contents_0=re.findall('<span class="ctt">(.*?)</span>',html_2,re.S)#一级
	contents_1=re.findall('<a href=.*?>@.*?</a>(.*?)<a href=.*?>举报</a> ',html_2,re.S)#二级

	for i in contents_0:
		i=re.sub(pattern_0,'',i)
		i=re.sub(pattern_0_1,'',i)
		i=re.sub(pattern_0_2,'',i)
		i=i.replace(':','')
		i=i.strip()
		contents_2.append(i)

	for i in contents_1:
		i=re.sub(pattern_0,'',i)
		i=re.sub(pattern_0_1,'',i)
		i=re.sub(pattern_0_2,'',i)
		i=i.replace('</span>','')
		i=i.replace('&nbsp;','')
		i=i.replace(':','')
		i=i.strip()
		contents_2.append(i)

	for i in contents_2:
		i=re.sub('\s','',i)#去除空白
		if len(i)==0:
			pass
		else:
			contents.append(i)
	times_0=re.findall('<span class="ct">(.*?)</span>',html_2,re.S) #获取时间
	times=[]#时间
	pattern_1= re.compile(r'\d{2}月\d{2}日')#匹配日期
	for i in times_0:
		try:
			t_1= re.match(pattern_1, i).group()
			t_1=t_1.replace("月","-")
			t_1=t_1.replace("日","-")
			t_1="2022-"+t_1
		except:
			a=datetime.datetime.now().strftime('%Y-%m-%d')
			t_1=a#改为当天
		times.append(t_1)
	
	all=[]
	for i in range(len(user_ids)):#这有问题
		try:
			al=[user_ids[i],names[i],contents[i],times[i]]
		except:
			j='空'
			contents.append(j)
			al=[user_ids[i],names[i],contents[i],times[i]]
		all.append(al)
	return all

def save_afile(alls,filename):
    """将一个微博评论数据保存在一个excle"""
    f=xlwt.Workbook()
    sheet1=f.add_sheet(u'sheet1',cell_overwrite_ok=True)
    sheet1.write(0,0,'Comment_ID')
    sheet1.write(0,1,'Comment_Name')
    sheet1.write(0,2,'Comment_Content')
    sheet1.write(0,2,'Comment_Time')
    # sheet1.write(0,3,'时间')
    i=1
    for all in alls:
        for data in all:
            for j in range(len(data)):
                sheet1.write(i,j,data[j])
            i=i+1
    f.save(filename+'.xls')

# def extract(inpath,l):
#     """取出一列数据"""
#     data = xlrd.open_workbook(inpath, encoding_override='utf-8')
#     table = data.sheets()[0]#选定表
#     nrows = table.nrows#获取行号
#     ncols = table.ncols#获取列号
#     numbers=[]
#     for i in range(1, nrows):#第0行为表头
#         alldata = table.row_values(i)#循环输出excel表中每一行，即所有数据
#         result = alldata[l]#取出表中第一列数据
#         numbers.append(result)
#     return numbers

def run(url):
	alls=[]#每次循环就清空一次
	pa=[]#空列表判定
	# url='https://weibo.cn/comment/hot/LfjaPmbKW?rl=1&gid=10001'#一个微博的评论首页
	headers=random.choice(headers_list)#每次随机挑一个headers
	html,page=html_1(url,headers)
	# print('源码：'+html)
	print('页数：'+str(page))
	print(url)
	# print(headers)
	if page==0:#如果为0，即只有一页数据
		#print('进入页数为0')
		try:
			data_1=body(html)
		except:
			data_1=pa
		alls.append(data_1)#将首页爬取出来
		#print('共计1页,共有'+str(count(alls))+'个数据')
	else:#两页及以上
		#print('进入两页及以上')
		#print('页数为'+str(page))
		for j in range(1,page+1):#从1到page
			if j>=51:
				print("页面超过50页，提取前50页数据")
				break
			else:
				url_1=url+'&page='+str(j)
				#print(url_1)
				print("正在爬取第"+str(j)+"页")
				htmls,pages=html_1(url_1,headers)
				alls.append(body(htmls,j))
	print('原微博共计'+str(page)+'页,爬取了'+str(count(alls))+'个数据')
	save_afile(alls,"weibo_comment")
	print('爬取的评论数据文件、保存完毕')
	return topic

def WeiboCrawler(url):
	#由于微博限制，只能爬取前五十页的
	#里面的文件是爬取到的正文文件
	# url='https://weibo.cn/comment/LncH85pAQ?uid=2803301701&rl=0&gid=10001#cmtfrm'#一个微博的评论首页
	url = url[: -7]
	topic=run(url)
	return topic
# WeiboCrawler("https://weibo.cn/comment/LncH85pAQ?uid=2803301701&rl=0&gid=10001#cmtfrm")


