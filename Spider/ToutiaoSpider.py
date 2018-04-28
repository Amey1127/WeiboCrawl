# -*- coding:utf-8 -*-
import requests
#from urllib.parser import urlencode
from requests.exceptions import RequestException
import json
import sys
import MySQLdb
from random import *
import time

reload(sys)
# if(sys.platform == 'win32'):
#     encoding = "gb2312"
# else:
#     encoding = "utf8"

sys.setdefaultencoding("utf8")


def get_data(data):
    # urlencode(data)就是链接解析
    url = 'https://www.toutiao.com/search_content/'
    response = requests.get(url,params=data)
    #print response.text
    try:
        if response.status_code == 200:
            return response.text
    except RequestException:
        print('data is error')
        return None

def parser_data(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            title = item.get('title'),
            url = item.get('url')
            post0 = (title, url, url)
            insert_post0 = 'INSERT INTO toutiaopost(title,link) VALUES (%s,%s) ON DUPLICATE KEY UPDATE link = %s'
            cursor.execute(insert_post0, post0)

if __name__ == '__main__':
    db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="Toutiao", port=3306, charset="utf8")
    cursor = db.cursor()
    for i in range(5):
        t = randint(1,5)
        time.sleep(t)
        data = {
            'offset': 20 * i,
            'format': 'json',
            'keyword': '物理学家霍金去世',
            'autoload': 'true',
            'count': 20,
            'cur_tab': 1,
            'from':'search_tab'
        }
        html = get_data(data)
        list = parser_data(html)
        for i in list:
            print i

#头条评论https://www.toutiao.com/api/comment/list/?group_id=6532649159076348419&item_id=6532649159076348419&offset=0&count=5