import re
import time
from urllib.request import Request, urlopen
import pymysql

localtime = str(time.localtime()[0]) + '-' + str(time.localtime()[1]) + '/' + str(time.localtime()[2])
sql_time = str(time.localtime()[0]) + str(time.localtime()[1]) + str(time.localtime()[2])

lasturl = 'nbs.D110000renmrb_01.htm'

# mysql导入
conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='root',
                       database='people',
                       charset='utf8'
                       )
cursor = conn.cursor()

# mysql数据表格创建
sql_01 = """
CREATE TABLE IF NOT EXISTS people%s (
title CHAR(255),
content TEXT,
number CHAR(100),
primary key ( title )
)ENGINE=innodb DEFAULT CHARSET=utf8;  
""" % ('_'+sql_time)

# cursor.execute(sql_01)
# sql = '''
# INSERT INTO people%s
# (title, content, number)
# VALUES
# (%s, %s, %s);
# ''' % (('_'+sql_time), '2', '1', '1')
#
#
# cursor.execute(sql)
# conn.commit()
# # 关闭光标对象
# cursor.close()
#
# # 关闭数据库连接
# conn.close()
# print('1')
# time.sleep(100000)
def mk_url(last_url=lasturl):

    url = 'http://paper.people.com.cn/rmrb/html/{}/{}'.format(localtime, last_url)
    return url


def open_url(url):

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
            }

    rq = Request(url, headers=header)
    resp = urlopen(rq)
    html = resp.read().decode('utf-8')
    time.sleep(2)
    return html


def titleurl_find(html):
    html=html.replace("./", "")
    # 找到文章各个板块的url
    passage_url = re.compile(r'<a id=pageLink href=(.*?)>')
    url_list = passage_url.findall(html)

    # 找到各个板块url对应的标题
    title = list()
    for i in url_list:
        title_text = re.compile(r'<a id=pageLink href={}>(.*?)</a>'.format(i))
        title.append(title_text.findall(html)[0])

    # 制成字典
    url_dict = dict(zip(title, url_list))

    return url_dict


def passageurl_find(last_url):
    url = mk_url(last_url)
    html = open_url(url)
    # 以下方法存在未知错误，改用文本查找
    # ul = re.compile(r"<ul class='news-list'>(.*?)  </ul>")
    # li = ul.findall(html)
    # 查找某板块下的所有文章的url
    ul = str(html).split("<ul class='news-list'>")[1]
    li = ul.split('</ul>')[0]

    passage = re.compile(r'<a href=(.*?)>')
    passage_url = passage.findall(li)

    title = list()
    # 查找文章的title
    for i in passage_url:
        title_text = re.compile(r"<a href={}>(.*?)  </a>".format(i))
        title.append(title_text.findall(str(li))[0])
    # 将title：url制作成字典
    passage_url_dict = dict(zip(title, passage_url))

    return passage_url_dict


def passage_save(passage_url='nw.D110000renmrb_20201023_1-01.htm'):
    url = mk_url(passage_url)
    html = open_url(url)
    # 以下为查找文章内容
    DIV = str(html).split('<DIV id=ozoom style="zoom:100%;">')[1]
    DIV = DIV.replace('■&nbsp;&nbsp;', '')
    DIV = DIV.replace('</P>', '')
    DIV = DIV.replace('&nbsp;', ' ')
    content = DIV.split('<!--enpcontent-->')[1]
    content = content.split('<!--/enpcontent-->')[0]
    paragraph = content.split('<P>')
    paragraph.remove('')

    # 以下为文章内容效果展示程序
    # for i in paragraph:
    #
    #     print(i)
    # print('*'*100)

    # 返回一个文章内容表格（打印时自带换行）
    return paragraph


url = mk_url()
html = open_url(url)
url_dict = titleurl_find(html)
for number, each_url in url_dict.items():
    passage_url_dict = passageurl_find(each_url)
    for title, passage_url in passage_url_dict.items():
        content = str(passage_save(passage_url))
        content = pymysql.escape_string(content)
        title = pymysql.escape_string(title)
        number = pymysql.escape_string(number)

        sql = '''
        INSERT INTO people%s 
        (title, content, number)
        VALUES
        ('%s', '%s', '%s');
        ''' % (('_'+sql_time), title, content, number)
        cursor.execute(sql)
        conn.commit()
        print('数据导入成功')

# 关闭光标对象
cursor.close()

# 关闭数据库连接
conn.close()
