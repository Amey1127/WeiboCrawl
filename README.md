weibo_crawler
=============

本工具使用模拟登录来实现微博搜索结果的爬取，如果用户需要爬取更多的数据，请在weibo\_zhanghao.txt中添加微博帐号的用户名密码（可以注册小号)，每一行一个账户，用户名和密码用逗号隔开。

环境要求
----------------------
1. Python

    系统中需要先安装Python，这是Python官网链接[http://www.python.org](http://www.python.org)
    
2. BeautifulSoup

    BeautifulSoup是Python的一个html解析库，用来解析微博搜索结果中相关信息，版本是BeautifulSoup4, 安装方法可自行百度
    
    有关BeautifulSoup的更多信息，请访问[http://www.crummy.com/software/BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)

使用
-----------------------
将要查询的关键词添加到keywords文件中，并启动程序

        python ./Crawler.py

以文件形式保存博文信息


关于爬取时间间隔
----------------------
微博爬取中，如果爬取过快，会导致帐号被封，需要输入验证码，因此，工具里面每爬取一页会有一定时间休眠，在类SinaSearchCrawler的randomSleep和randomSnap中，每爬取一页，randomSnap一次，如果出现帐号被封，则会randomSleep，时间较长，唤醒后会切换帐号重新爬取
每个页面默认重试3次




