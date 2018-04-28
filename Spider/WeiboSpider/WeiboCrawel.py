#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

reload(sys)
# if(sys.platform == 'win32'):
#     encoding = "gb2312"
# else:
#     encoding = "utf8"

sys.setdefaultencoding("utf8")

import urllib
import urllib2
import socket
import cookielib
import base64
import re
import time
import random
import json
import rsa
import binascii
import gzip, StringIO
import types
from bs4 import BeautifulSoup
from ContentAndUser import User, Content,Comment
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_user_agent():
    user_agents = list()
    fp = open('./user_agents', 'r')
    line = fp.readline().strip()
    while (line):
        user_agents.append(line)
        line = fp.readline().strip()
    fp.close()
    return user_agents

class UserAgents:
    user_agents = load_user_agent()
    @staticmethod
    def get_random_user_agent():
        length = len(UserAgents.user_agents)
        index = random.randint(0, length - 1)
        user_agent = UserAgents.user_agents[index].strip()
        return user_agent

PROXY = '211.159.177.212:3128'
proxy = urllib2.ProxyHandler({'http': PROXY})
cookiejar = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cookiejar)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

parameters = {
    'entry': 'weibo',
    'callback': 'sinaSSOController.preloginCallBack',
    'su': 'TGVuZGZhdGluZyU0MHNpbmEuY29t',
    'rsakt': 'mod',
    'checkpin': '1',
    'client': 'ssologin.js(v1.4.5)',
    '_': '1362560902427'
}

class SinaLogin():
    def __init__(self):
        # 用户帐户列表，用于模拟登录
        self.username = list()
        self.passwd = list()
        self.read_account_list()

    def read_account_list(self):
        with open('weibo_zhanghao.txt') as weibo_file:
            for line in weibo_file:
                items = line.split(',')
                self.username.append(items[0].strip())
                self.passwd.append(items[1].strip())

    def set_request(self, url, data, headers):
        self.request = urllib2.Request(
            url=url,
            data=data,
            headers=headers
        )

    def encrypt_username(self, uname):
        username_ = urllib.quote(uname)
        encrypt_username = base64.encodestring(username_)[:-1]
        return encrypt_username

    def encrypt_pwd(self, pwd, servertime, nonce, pubkey):
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(pwd)  # 拼接明文 js加密文件中得到
        passwd = rsa.encrypt(message, key)  # 加密
        passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制
        return passwd

    def get_server_time(self):
        url = 'http://login.sina.com.cn/sso/prelogin.php?' + urllib.urlencode(parameters)
        data = urllib2.urlopen(url).read()
        p = re.compile('\((.*)\)')
        try:
            json_data = p.search(data).group(1)
            data = json.loads(json_data)
            servertime = str(data['servertime'])
            nonce = data['nonce']
            pubkey = data['pubkey']
            rsakv = data['rsakv']
            return servertime, nonce, pubkey, rsakv
        except:
            print 'Get severtime error!'
            return None

    def login(self):
        if (len(self.username) < 1):
            print "微博用户不存在"
            return False
        index = random.randint(0, len(self.username) - 1)
        uname = self.username[index]
        pwd = self.passwd[index]

        url = 'http://login.sina.com.cn/sso/login.php?client= .js(v1.4.5)'
        try:
            servertime, nonce, pubkey, rsakv = self.get_server_time()
        except:
            return False

        global postdata
        postdata['servertime'] = servertime
        postdata['nonce'] = nonce
        postdata['rsakv'] = rsakv
        postdata['su'] = self.encrypt_username(uname)
        postdata['sp'] = self.encrypt_pwd(pwd, servertime, nonce, pubkey)
        postdata_encode = urllib.urlencode(postdata)
        user_agent = UserAgents.get_random_user_agent()
        headers = {
            'User-Agent': user_agent,
            'Accept-Encoding': 'gzip',
            'referer': 'http://www.weibo.com'
        }

        self.set_request(url, postdata_encode, headers)

        response = urllib2.urlopen(self.request)
        html = response.read()
        if (response.headers.get('content-encoding', None) == 'gzip'):
            html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()

        p = re.compile('location\.replace\(.(.*?).\)')
        try:
            # 如果没有异常返回，说明此时已自动登录，之后只需设置url和data就可以post或者直接get，
            # 注意不要在request中设置header，这是因为cookie也是header的一部分，如果设置header会导致没有cookie，也就没有登录
            login_url = p.search(html).group(1)
            urllib2.urlopen(login_url)
            return True
        except Exception, e:
            with open("./error_log", "a+") as test_file:
                test_file.write(html)
            print e
            return False


class SinaSearchCrawler():
    base_url = "http://s.weibo.com"
    sina_user = None
    """
        模拟登录
    """

    def login(self):
        status = self.sina_user.login()
        if (status == True):
            print '登录成功.'
        else:
            print '登录失败.'

    def __init__(self):
        # 模拟一个用户并登录
        self.sina_user = SinaLogin()
        self.login()

        self.request = None
        timeout = 40
        socket.setdefaulttimeout(timeout)

    """
        随机分配睡眠时间
    Input:
        factor: 睡眠因子，因子越大，睡眠的时间越久
    """

    def randomSleep(self, factor):
        sleeptime = random.randint(20, 40)
        time.sleep(sleeptime * factor)

    def randomSnap(self):
        sleeptime = random.randint(20, 30)
        time.sleep(sleeptime)
        # pass

    """
        根据URL获取网页源代码
    Input:
        url:网址
    Output:
        html:网页源代码
    """

    def get_html(self, url):
        html = None
        retry = 3
        while (retry > 0):
            try:
                self.request = urllib2.Request(url=url)
                response = urllib2.urlopen(url)
                html = response.read()

                if (response.headers.get('content-encoding', None) == 'gzip'):
                    html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()
                break
            except urllib2.URLError, e:
                print 'url error:', e
                self.randomSleep(4 - retry)
                retry = retry - 1
                continue
            except Exception, e:
                print 'error:', e
                self.randomSleep(4 - retry)
                retry = retry - 1
                continue
        return html

    """
        根据爬取的第一页的结果分析结果总数，并计算需要爬取的页数，最大可爬取页数不超过50页
    Input:
        html:爬取的搜索结果第一页源代码
        page_num_pattern: 匹配结果数的模式（正则表达式）
        num_per_page: 每一页的结果数
    Output:
        pages_num: 结果页数(-1 error)
    """

    def get_pages_num(self, html, page_num_pattern):
        # get json
        reg = re.compile(r'%s' % page_num_pattern, re.I)
        match = reg.findall(html)
        if (match):
            for m in match:
                header_json = json.loads(m)
                if (type(header_json) == types.DictType):
                    soup = BeautifulSoup(header_json['html'])

                    # 获取微博搜索结果数
                    lis = soup.find("div", class_="layer_menu_list W_scroll").find("ul").find_all("li")
                    if (lis == None):
                        return -1
                    elif (len(lis) == 0):
                        print "无搜索结果"
                        return 0
                    else:
                        return len(lis)

'''
微博内容爬取类
'''
class WeiboSearchCrawler(SinaSearchCrawler):

    def __init__(self):
        SinaSearchCrawler.__init__(self)
        self.base_url = "%s/weibo" % SinaSearchCrawler.base_url
        self.root = "F://SNS2017//"

    #获取weibourl和wirterurl
    def get_url(self,html):
        weibo_list = list()
        reg = re.compile(r'<script>STK && STK\.pageletM && STK\.pageletM\.view\((\{"pid":"pl_weibo_direct".+?)\)</script>', re.I)
        match = reg.search(html)
        if (match):
            m = match.group(1)
            header_json = json.loads(m)
            if (type(header_json) == types.DictType):
                soup = BeautifulSoup(header_json['html'])
                div = soup.find("div", class_="search_feed")
                if (type(div) == types.NoneType):
                    return weibo_list

                # 获取微博用户列表
                wb_list = div.find_all("div", class_="WB_cardwrap S_bg2 clearfix")
                if (type(wb_list) == types.NoneType):
                    return weibo_list

                for wb in wb_list:
                    weibo = Content()
                    #用户url
                    div_tag = wb.find("div", class_="feed_content wbcon")
                    if (type(div_tag) != types.NoneType):
                        links = div_tag.find_all("a")
                        if (len(links) >= 1):
                            if (type(links[0]) != types.NoneType):
                                if (links[0].has_attr("href") == True):
                                    weibo.writerurl = 'http:' + str(links[0]["href"])

                    # 微博url
                    p_time = wb.find_all("div", class_="feed_from W_textb")
                    # 在某些情况下微博发布时间找不到，原因未知
                    # 如果没有微博发布时间，则默认该微博不存在
                    if (len(p_time) > 0):
                        if (type(p_time) != types.NoneType):
                            p_len = len(p_time)
                            link = p_time[p_len - 1].find("a", class_="W_textb")
                            if (type(link) != types.NoneType):
                                if (link.has_attr("href") == True):
                                    weibo.weibourl = 'http:' + str(link['href'])
                    else:
                        print "extract publish time error:%s" % (html)
                        continue

    def extract_userinfo(self,url):
        driver.get(url)
        user = User()
        user.userID = driver.find_elements_by_class_name()


    def extract_weiboinfo(self,weibo,url):
        driver.get(url)
        id_parttern = re.compile()
        weibo.weiboID =

    #输入：
    #输出：微博昵称和微博url,用户ID
    def extract_writer_info(self, weibo, tag):
        if(type(tag)!=types.NoneType):
            links = tag.find_all("a")
            if (len(links) >= 1):
                if (type(links[0]) != types.NoneType):
                    # 用户微博昵称
                    if (links[0].has_attr("title") == True):
                        weibo.writername = links[0]["title"]

                    # 用户微博url
                    if (links[0].has_attr("href") == True):
                        weibo.writerurl = 'http:' + str(links[0]["href"])

                    # 用户ID
                    if (links[0].has_attr("usercard") == True):
                        idstr = links[0]["usercard"]
                        id_pattern = re.compile(r'id=([0-9]+)')
                        id_m = id_pattern.search(idstr)
                        if (id_m):
                            weibo.writerID = id_m.group(1)

    def extract_forward_favorite_comment_like_count(self, weibo, tag):
        if(type(tag) != types.NoneType):
            forward = tag.find("a", attrs={"action-type": "feed_list_forward"})
            pattern = re.compile(r"(\d+)")
            if (type(forward) != types.NoneType):
                m = pattern.search(forward.get_text())
                if (m):
                    weibo.forwardCount = int(m.group(0))

            favorite = tag.find("a", attrs={"action-type": "feed_list_favorite"})
            if (type(favorite) != types.NoneType):
                m = pattern.search(favorite.get_text())
                if (m):
                    weibo.favoriteCount = int(m.group(0))

            comment = tag.find("a", attrs={"action-type": "feed_list_comment"})
            if (type(comment) != types.NoneType):
                m = pattern.search(comment.get_text())
                if (m):
                    weibo.commentCount = int(m.group(0))

            like = tag.find("a", attrs={"action-type": "feed_list_like"})
            if (type(like) != types.NoneType):
                m = pattern.search(like.get_text())
                if (m):
                    weibo.likeCount = int(m.group(0))

    def extract_publish_time(self, weibo, tag):
        if(type(tag) != types.NoneType):
            p_len = len(tag)
            link = tag[p_len - 1].find("a", class_="W_textb")
            if(type(link) != types.NoneType):
                if(link.has_attr("title") == True):
                    weibo.time = str(link['title']) + ':00'
                if (link.has_attr("href") == True):
                    weibo.weibourl = 'http:' + str(link['href'])
                    id_pattern = re.compile(r'https://weibo.com/([0-9]+)')
                    id_m = id_pattern.search(weibo.weibourl)
                    weibo.weiboID = id_m.group(1)

    def get_weibo_content_commit(self, weibo, html):
        weibo_list = list()
        reg = re.compile(r'<script>STK && STK\.pageletM && STK\.pageletM\.view\((\{"pid":"pl_weibo_direct".+?)\)</script>', re.I)
        match = reg.search(html)
        if (match):
            m = match.group(1)
            header_json = json.loads(m)
            if (type(header_json) == types.DictType):
                soup = BeautifulSoup(header_json['html'])

    def extract_weibo_comments(self,html):
        coments_list = list()


    def extract_weibo(self, html):
        weibo_list = list()
        reg = re.compile(r'<script>STK && STK\.pageletM && STK\.pageletM\.view\((\{"pid":"pl_weibo_direct".+?)\)</script>', re.I)
        match = reg.search(html)
        if (match):
            m = match.group(1)
            header_json = json.loads(m)
            if (type(header_json) == types.DictType):
                soup = BeautifulSoup(header_json['html'])
                # print u"输入文件名称"
                # eventname = raw_input("%s")
                # path = self.root + eventname + '//'
                div = soup.find("div", class_="search_feed")
                if (type(div) == types.NoneType):
                    return weibo_list

                # 获取微博用户列表
                wb_list = div.find_all("div", class_="WB_cardwrap S_bg2 clearfix")
                if (type(wb_list) == types.NoneType):
                    return weibo_list

                for wb in wb_list:
                    weibo = Content()
                    # 获取微博(用户名、认证类型、微博内容)
                    div_tag = wb.find("div", class_="feed_content wbcon")
                    self.extract_writer_info(weibo, div_tag)

                    # 微博发布时间
                    p_time = wb.find_all("div", class_="feed_from W_textb")
                    # 在某些情况下微博发布时间找不到，原因未知
                    # 如果没有微博发布时间，则默认该微博不存在
                    if (len(p_time) > 0):
                        self.extract_publish_time(weibo, p_time)
                    else:
                        print "extract publish time error:%s %s" % (weibo.weiboID, weibo.writername)
                        continue

                    # 转发收藏评论数
                    wb_action = wb.find("div", class_="feed_action clearfix")
                    self.extract_forward_favorite_comment_like_count(weibo, wb_action)

                    # 微博内容
                    weibo_html = self.get_html(weibo.weibourl)
                    self.get_weibo_content_commit(weibo, weibo_html)

                    weibo_list.append(weibo)
            else:
                print "extract_weibo:get error"
            return weibo_list

    def get_pages(self, html):
        page_num_pattern = '<script>STK && STK\.pageletM && STK\.pageletM\.view\((\{"pid":"pl_weibo_direct".+?)\)</script>'
        pages_num = SinaSearchCrawler.get_pages_num(self, html, page_num_pattern)
        return pages_num

    def search(self, keyword="中美贸易战", pro_code=0, city_code=1000, pages=0):
        # keyword = keyword.decode("gb2312").encode("utf-8")
        weibo_list = list()
        # 设置爬取失败重试次数
        retry = 3
        # 获取第一页搜索结果并计算搜索结果页数
        if (pro_code == 0):
            req_url = "%s/%s&xsort=time&nodup=1" % (self.base_url, urllib.quote(keyword))
        else:
            req_url = "%s/%s&xsort=time&region=custom:%d:%d&nodup=1" % (self.base_url, urllib.quote(keyword), pro_code, city_code)
        page_num = 0
        while (retry > 0):
            # 获取第一页搜索结果
            html = self.get_html(req_url)
            # 根据第一页结果得到搜索结果页数
            page_num = self.get_pages(html)
            # page_num = 5
            if (page_num < 0):
                print "爬取异常，等待。。。"
                self.randomSleep(4 - retry)
                print "等待结束，切换登录用户重新开始尝试"
                self.login()
                retry = retry - 1
            else:
                retry = 0

            # 首先判断搜索结果页数是否为0，0表示默认爬取所有页
            # 如果pages大于实际搜索结果页数， 取实际搜索结果页数
            if (pages == 0 or (pages > page_num and page_num >= 0)):
                pages = page_num

        if (page_num < 0):
            pages = 0
            print "无搜索结果"

        print "共有%d页搜索结果" % pages

        # 分页获取搜索结果
        for i in range(1, pages + 1):
            # 每个页面尝试3次
            retry = 3
            if (pro_code == 0):
                req_url = "%s/%s&xsort=time&page=%d&nodup=1" % (self.base_url, keyword, i)
            else:
                req_url = "%s/%s&xsort=time&region=custom:%d:%d&page=%d&nodup=1" % (self.base_url, keyword, pro_code, city_code, i)
            while (retry > 0):
                print "开始爬取第 %d页" % i
                # 第一页不用再次爬取
                if (i != 1):
                    html = self.get_html(req_url)
                if (type(html) == types.NoneType):
                    print "下载网页失败"
                    retry = retry - 1
                    continue
                weibo_infos = self.extract_weibo(html)
                # 写入相应的文件
                if (type(weibo_infos) != types.NoneType):
                    if (len(weibo_infos) > 0):
                        for weibo_info in weibo_infos:
                            # 添加微博地点信息
                            # if (pro_code != 0):
                            #     weibo_info.province = province_dict[str(pro_code)]
                            # if (DBInfo.enable == True):
                            #     weibo_info.insert_table()
                            # else:
                            #     weibo_info.writeFile("./weibo_info")
                        weibo_list.extend(weibo_infos)
                        retry = 0
                    else:
                        print "爬取异常，等待。。。"
                        self.randomSleep(4 - retry)
                        print "等待结束，切换登录用户重新开始尝试"
                        self.login()
                        retry = retry - 1
                else:
                    print "该页没有结果"
                    continue

                # 每爬取完一页以后随机睡眠一段时间
                print '防止被服务器封锁，随机睡眠。。。'
                self.randomSnap()

        return weibo_list

def read_keywords():
    keywords = list()
    fp = open("./keywords.txt")
    line = fp.readline().strip()
    while (line):
        keywords.append(line)
        line = fp.readline().strip()
    fp.close()
    return keywords

if __name__ == '__main__':
    keywords = read_keywords()
    driver = webdriver.Chrome()
    for keyword in keywords:
        print "搜索关键词: %s" % keyword
        # 搜索微博
        weibo_api = WeiboSearchCrawler()
        weibo_api.search(keyword=keyword, pages=2)
    driver.close()