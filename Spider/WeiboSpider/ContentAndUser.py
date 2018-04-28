#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf8")

class Weibo():
    def __init__(self):
        self.writerID = ''
        self.screen_name = ''
        self.writerurl = ''
        self.weibourl = ''
        self.weiboID = ''
        self.content = ''
        self.content_url = list()
        self.content_at_url = {}
        self.time = ''
        self.forwards_count = 0
        self.comments_count = 0
        self.likes_count = 0

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
            if(count> 1):
                string += ","
                count = count - 1
        string += ""
        return string

class User():
    def __init__(self):
        self.userID = ''
        self.userName = ''
        self.location = ''
        self.gender = ''
        self.birthday = ''
        self.age = ''
        self.description = ''
        self.regtime = ''
        self.WeiLevel = ''
        self.followerCount = 0
        self.followeeCount = 0
        self.WeiboCount = 0
        self.title = list()

class Comment():
    def __init__(self):
        self.commentID = 0
        self.userID = ''
        self.userName = ''
        self.time = ''
        self.toWhom = ''
        self.originID = ''
        self.content = ''
        self.likeCount = 0