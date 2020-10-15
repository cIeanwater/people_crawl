import re
import time
from urllib.request import Request, urlopen

localtime = str(time.localtime()[0]) + '-' + str(time.localtime()[1]) + '/' + str(time.localtime()[2])

lasturl = 'nbs.D110000renmrb_01.htm'


def mk_url(last_url = lasturl):

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
    return html


def titleurl_find(html):
    html=html.replace("./", "")
    # 找到文章各个板块的url
    passage_url = re.compile(r'<a id=pageLink href=(.*?)>')
    url_list = passage_url.findall(html)
    print(url_list)

    # 找到各个板块url对应的标题
    title = list()
    for i in url_list:
        title_text = re.compile(r'<a id=pageLink href={}>(.*?)</a>'.format(i))
        title.append(title_text.findall(html)[0])

    # 制成字典
    url_dict = dict(zip(title, url_list))

    return url_dict


def passageurl_find(last_url):
    url = mk_url(lasturl)
    html = open_url(url)

    # 查找某板块下的所有文章的url
    ul = re.compile(r"<ul class='news-list'>(.*?)</ul>")
    li = ul.findall(html)
    passage = re.compile(r'<a href=(.*?)>')
    passage_url = passage.findall(str(li))
    title = list()
    # 查找文章的title
    for i in passage_url:
        title_text = re.compile(r"<a href={}>(.*?)  </a>".format(i))
        title.append(title_text.findall(str(li))[0])
    passage_url_dict = dict(zip(title, passage_url))
    return passage_url_dict


if __name__ == '__main__':
    url = mk_url()

    html = open_url(url)
    a = titleurl_find(html)



