# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import os

def getintourl(url):
    list1 = list()
    list2 = list()
    browser.get(url)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="js_report_article3"]')))
    b = browser.find_element_by_xpath('//*[@id="meta_content"]').text  # 文章发表时间及表头
    id = url.split('/')[-1]
    time = browser.find_element_by_xpath('//*[@id="post-date"]').text
    author = browser.find_element_by_xpath('//*[@id="post-user"]').text
    title = browser.find_element_by_xpath('//*[@id="activity-name"]').text  # 标题
    content = browser.find_element_by_xpath('//*[@id="js_content"]').text  # 内容
    r = browser.page_source
    try:
        soup = BeautifulSoup(r, 'lxml')
        tag = soup.find_all("img", class_="img_loading")
        for data in tag:
            print data
            if (data.has_attr("data-src") == True):
                src = data['data-src']
                list1.append(src)
            if (data.has_attr("data-type") == True):
                type = data['data-type']
                list2.append(type)
    except:
        print("爬取失败")
    if True:
        b = b.strip()
        title = title.strip()
        content = content.strip()

    # 文件存储
    path = os.getcwd()
    key = "事件库".decode('utf-8', 'ignore').encode('gbk')
    path1 = os.path.join(path, key)
    if not os.path.exists(path1):  # 如果文件夹不存在则创建
        os.makedirs(path1)
    path2 = path + "\%s" % (key)  # 存储图片文件位置
    keyword01 = b.decode('utf-8', 'ignore').encode('gbk')
    keyword02 = title.decode('utf-8', 'ignore').encode('gbk')
    new_path = os.path.join(path2, keyword02 + keyword01)
    if not os.path.exists(new_path):  # 如果文件夹不存在则创建
        os.makedirs(new_path)
    new_path1 = path2 + "\%s" % (keyword02 + keyword01)
    new_path2 = os.path.join(new_path1, keyword02 + keyword01)
    new_path3 = os.path.join(new_path1, "info")

    file_path = str(new_path2) + ".txt"
    file_path1 = str(new_path2) + "1" + ".txt"
    file_path2 = str(new_path3) + ".txt"

    with open(file_path, 'wb') as f1:
        f1.write('{title: ' + title + ',' + '\n'
                 'time: ' + time + ',' + '\n'
                 'writerID: ' + id + ',' + '\n'        
                 'writerName: ' + author + ',' + '\n'
                 'content: ' + content + '}')
        f1.close()

    fnew = open(file_path1, 'wb')
    with open(file_path) as f:
        for line in f.readlines():
            data = line.replace(' ', '')
            if len(data) != 0:
                fnew.write(data)
        f.close()
        fnew.close()
    os.remove(file_path)
    with open(file_path2, 'wb') as f1:
        f1.write(url)
        f1.write('\n')
        for link in list1:
            f1.write(link)
            f1.write('\n')
        f1.close()

    img(list1, new_path1, list2)

    print("爬取成功")
    print(list1)
    print(b)
    print(title)


def img(list1, new_path, list2):
    k = len(list1)
    print k
    try:
        for i in list1:
            if k >= 0:
                new_img_path = os.path.join(new_path, str(k))
            else:
                break
            k = k - 1
            if (len(list2) != 0):
                path = new_img_path + "." + list2[k]
            else:
                path = new_img_path + ".png"
            r = requests.get(i)
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
    except:
        print("爬取失败")


if __name__ == "__main__":

    url = str(raw_input("请输入要爬取的链接:  "))
    browser = webdriver.Chrome()
    while(url):
        getintourl(url)
        url = str(raw_input("请输入要爬取的链接:  "))
    browser.close()