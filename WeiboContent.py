#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
# if(sys.platform == 'win32'):
#     encoding = "gb2312"
# else:
#     encoding = "utf8"
    
sys.setdefaultencoding("utf8")

from Global import DBInfo
from _mysql_exceptions import DatabaseError
from DBConnection import DBConnection

weibo_content_sql = 'create table weibo_content(id int NOT NULL auto_increment, user_id varchar(20), screen_name varchar(50),verify_type varchar(20),content varchar(500), content_url varchar(1000), content_at_url varchar(1000), time datetime, forward_count int, favorites_count int, comments_count int, province varchar(10), city varchar(10), PRIMARY KEY (id))'


class WeiboContent():

    def __init__(self):
        self.writerID = ''
        self.screen_name = ''
        self.writerurl = ''
        self.content = ''
        self.content_url = list()
        self.content_at_url = {}
        self.time = ''
        self.weibourl = ''
        self.weiboID = ''
        self.forwards_count = 0
        self.comments_count = 0
        self.likes_count = 0
        self.province = ''
        self.city = ''
        self.root = "D://SNS2018//"

    def printIt(self):
        if not os.path.exists(self.root):   # 判断当前根目录是否存在
            os.mkdir(self.root)              # 若不存在根目录，则建立该根目录
        eventname = "陕西米脂砍人事件".decode('utf-8', 'ignore').encode('gbk')
        path = os.path.join(self.root,eventname)

        if not os.path.exists(path):        # 判断该文件是否存在
            os.mkdir(path)

        path1 = self.root + '\%s' % (eventname)
        name = self.screen_name.decode('utf-8', 'ignore').encode('gbk')
        ID = self.weiboID.decode('utf-8', 'ignore').encode('gbk')
        new_path = os.path.join(path1, ID + name)

        if not os.path.exists(new_path):    # 判断该文件是否存在
            os.mkdir(new_path)

        try:
            new_path1 = path1 + "\%s" % (ID + name)
            file_path1 = os.path.join(new_path1, ID + name)
            article_path = str(file_path1) + '.txt'
            file_path2 = os.path.join(new_path1, 'info')
            info_path = str(file_path2) + '.txt'
            with open(article_path, 'wb') as f1:
                f1.write('{articleID: ' + self.weiboID + ',' + '\n'+
                         'writerID: ' + self.writerID + ',' + '\n' +
                         'writerName: ' + self.screen_name + ',' + '\n' +
                         'time: ' + self.time + ',' + '\n' +
                         'content: ' + self.content + ',' + '\n' +
                         'forwardCount: ' + str(self.forwards_count) + ',' + '\n' +
                         'commentCount: ' + str(self.comments_count) + ',' + '\n' +
                         'likeCount: ' + str(self.likes_count) +'}' + '\n')
                f1.close()

            with open(info_path, 'wb') as f1:
                f1.write(self.weibourl)
                f1.write('\n')
                for link in self.content_url:
                    f1.write(link)
                    f1.write('\n')
                f1.close()
            print("文件保存成功")
        except:
            print("爬取失败")
        # print "用户信息:"
        # print "用户ID:", self.writerID
        # print "昵称:", self.screen_name
        # print "用户链接：",self.writerurl
        # print "微博内容:", self.content
        # print "微博外链接:", self.content_url
        # print "@好友：", self.content_at_url
        # print "发布时间:", self.time
        # print "微博链接：", self.weibourl
        # print "微博ID：", self.weiboID
        # print "转发数:", self.forwards_count
        # print "评论数:", self.comments_count
        # print "点赞数：", self.likes_count
        # print "省份:", self.province
        # print "城市:", self.city

    def list_to_string(self, the_list):
        string = ""
        for i in range(0, len(the_list)):
            string += the_list[i]
            if(i < len(the_list) -1):
                string += ","
        return string
    
    def dict_to_string(self, the_dict):
        string = ""
        count = len(the_dict)
        for key, value in the_dict.items():
            item = "\"%s\":\"%s\"" % (key, value)
            string += item
            if(count > 1):
                string += ","
                count = count - 1
        string += ""
        return string
    
    # def insert_table(self):
    #     try:
    #         sql = "insert into weibo_content(user_id, screen_name, verify_type, \
    #                 content, content_url, content_at_url, time, forward_count, \
    #                 favorites_count, comments_count, province, city) \
    #                 values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #
    #         query_sql = "select * from weibo_content where user_id = %s and unix_timestamp(time) = unix_timestamp(%s)"
    #
    #         #delete_sql = "delete from weibo_content where user_id = %s and unix_timestamp(time) = unix_timestamp(%s)"
    #
    #         db = DBConnection()
    #
    #         conn = db.get_conn()
    #
    #         conn.select_db(DBInfo.db)
    #         cur = db.get_cursor()
    #
    #         # 首先检查数据库中是否已经存在, 如果存在则不用插入
    #         count = cur.execute(query_sql, (self.id, self.time))
    #         if(count == 0):
    #             #将微博内容中的url列表转为字符串
    #             content_url = self.list_to_string(self.content_url)
    #             #微博内容中@好友字典转为字符串
    #             content_at_url = self.dict_to_string(self.content_at_url)
    #
    #             ret = cur.execute(sql, (self.id, self.screen_name, self.verify_type, self.content, \
    #                                 content_url, content_at_url, self.time, self.forward_count, \
    #                                 self.favorites_count,self.comments_count, self.province, self.city))
    #         else:
    #             ret = 1
    #
    #         conn.commit()
    #         db.close()
    #         if(ret == 1):
    #             return True
    #         return False
    #     except DatabaseError, e:
    #         print len(content_url), len(content_at_url)
    #         print "insert error", e

    def writeFile(self, filename):

        wfile = open(filename, 'a')
        try:
            wfile.write('{articleID: ' + self.weiboID + ',' + '\n'+
                             'writerID: ' + self.writerID + ',' + '\n' +
                             'writerName: ' + self.screen_name + ',' + '\n' +
                             'time: ' + self.time + ',' + '\n' +
                             'content: ' + self.content + ',' + '\n' +
                             'forwardCount: ' + str(self.forwards_count) + ',' + '\n' +
                             'commentCount: ' + str(self.comments_count) + ',' + '\n' +
                             'likeCount: ' + str(self.likes_count) + '}' + '\n' + '\n')
            # wfile.write(self.weiboID + str(chr(94)))
            # wfile.write(self.screen_name + str(chr(94)))
            # wfile.write(self.content + str(chr(94)))
            # wfile.write("[" + self.list_to_string(self.content_url) + "]" + str(chr(94)))
            # wfile.write("{" + self.dict_to_string(self.content_at_url) + "}" + str(chr(94)))
            # wfile.write(self.time + str(chr(94)))
            # wfile.write(str(self.forwards_count) + str(chr(94)))
            # wfile.write(str(self.likes_count) + str(chr(94)))
            # wfile.write(str(self.comments_count) + str(chr(94)))
            # wfile.write(self.province + str(chr(94)))
            # wfile.write(self.city)
            # wfile.write('\n')
        except IOError, e:
            print 'file error:', e
        finally:
            wfile.close()
        

