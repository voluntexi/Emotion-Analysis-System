import pymysql
def getConn():
    # 打开数据库连接
    conn = pymysql.connect(host="175.178.78.86", user="root", password="123", db="test",port=3306,charset='utf8mb4')
    return conn

# 采用占位符的方式来防止SQL注入
def insert(sql,args):
    conn = getConn()
    cur = conn.cursor()
    result = cur.execute(sql,args)
    print(result)
    conn.commit()
    cur.close()
    conn.close()

def update(sql,args):
    conn = getConn()
    cur = conn.cursor()
    result = cur.execute(sql,args)
    print(result)
    conn.commit()
    cur.close()
    conn.close()

def delete(sql,args):
    conn = getConn()
    cur = conn.cursor()
    result = cur.execute(sql,args)
    print(result)
    conn.commit()
    cur.close()
    conn.close()

def query(sql,args):
    conn = getConn()
    cur = conn.cursor()
    cur.execute(sql,args)
    results = cur.fetchall()
    # print(type(results))  # 返回<class 'tuple'> tuple元组类型
    comment=[]
    for row in results:
        dict={}
        dict['commentID']=row[0]
        dict['commentName']=row[1]
        dict['commentContent']=row[2]
        dict['commentValue']=row[3]
        comment.append(dict)
    conn.commit()
    cur.close()
    conn.close()
    return comment

if __name__ == '__main__':
    # sql = "INSERT INTO student VALUES('%s','%s','%s');"
    # insert(sql,('','',''))
    # sql = 'UPDATE student SET Sname=%s WHERE Sno = %s;'
    # args = ('wangprince', '2')
    # update(sql, args)
    # sql = 'DELETE FROM student WHERE Sno = %s;'
    # args = ('2',) # 单个元素的tuple写法
    # delete(sql,args)
    sql = 'SELECT  * FROM bilibili_comment;'
    print(query(sql,None))