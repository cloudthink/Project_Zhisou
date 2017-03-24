# -*- coding: utf-8 -*-
#deque是为了高效实现插入和删除操作的双向列表，适合用于队列和栈
# Python虽然不能利用多线程实现多核任务，但可以通过多进程实现多核任务。多个Python进程有各自独立的GIL锁，互不影响。
from collections import deque
import random
import time
import sys
import matplotlib
#from threading import Thread
import threading
from multiprocessing import Process,Pool
#以下为导入自定义库
print(sys.path)
import h5py
import re
import jieba
import jieba.analyse
tags = jieba.analyse.extract_tags('asddd', topK=1)
from spider.url_to_data import urltodata
#import queue
from multiprocessing import Queue
import queue
#用url_queue储存爬取到的url，待爬取
url_queue = deque()
#set是一种无序不重复列，用url_visited_try储存已爬取url
url_visited_try = set()


#爬虫起始地址
from control.base_config import spider_start_url
start_url = spider_start_url  # 入口页面, 可以换成别的
 
url_queue.append(start_url)
url_geted_number = 0
success_url_number = 0
tiaoshi_state=True

from control.base_config import user_agents_txt_road
ug_road=user_agents_txt_road
USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
try:
    with open(ug_road+'user_agents.txt') as fp:
        user_agents_list = [_.strip() for _ in fp.readlines()]
except Exception:
    user_agents_list = [USER_AGENT]


try:
    try:
        with open(ug_road+'proxies.txt') as nfp:
            user_proxies = [_.strip() for _ in nfp.readlines()]
    except:
        with open(ug_road+'proxies_old.txt') as nfp:
            user_proxies = [_.strip() for _ in nfp.readlines()]
except Exception:
    user_proxies = ['http://127.0.0.1:80']




from control.base_config import storage_road, storage_file_name
from storage.main_storage import urldatasave
road = storage_road
filename = storage_file_name



def geturlsdata(one_url):

    USER_AGENT = random.choice(user_agents_list)
    USER_PROXIE = random.choice(user_proxies)


    try:
        (title, can_urltodata, content_type, pagedata, root_url, new_alink_list, \
         jieba_content_keywords, meta_keywords, meta_description,error_log,page_score)=urltodata(url=one_url,user_agent=USER_AGENT,proxie=USER_PROXIE,tiaoshi=False)
        #url_content_title=title
        #url_content_maincontent=pagedata
        #url_content_keywords=meta_keywords
        #url_content_description=meta_description
        #url_content_key=jieba_content_keywords
        try:
            if 'http://' in one_url:
                new_one_url = re.sub('http://', '', one_url)
            elif 'https://' in one_url:
                new_one_url = re.sub('https://', '', one_url)
                new_one_url = re.sub('/', '<$#!!#$>', new_one_url)
        except:
            print('http do not in url:',new_one_url)
        #title = can_urltodata = content_type = pagedata = root_url = new_alink_list = \
         #   jieba_content_keywords = meta_keywords = meta_description = ''
        #page_score=random.random()
        #error_log=''
        if title!='':
            return([new_one_url,title, can_urltodata, content_type, pagedata, root_url, new_alink_list, \
                        jieba_content_keywords, meta_keywords,meta_description,page_score,error_log])
        else:
            # print('mmmmmm')
            title = can_urltodata = content_type = pagedata = root_url = new_alink_list = \
                jieba_content_keywords = meta_keywords = meta_description = ''

            return ([one_url, title, can_urltodata, content_type, pagedata, root_url, new_alink_list, \
                     jieba_content_keywords, meta_keywords, meta_description, page_score,error_log])
    except Exception as madebug:
        print('未知错误！！！！！！！',time.time(),madebug)





def give_urls_to_geturlsdata_save(part_urls_list):



    now_time = time.time()
    mff = open(ug_road + 'log_cannoturls_'+str(now_time)+'.txt', 'a')
    feature_24h_time = now_time + 60  # 86400
    new_urls_file_name = str(feature_24h_time) + '.txt'
    new_urls_file = open(urls_data_road + new_urls_file_name, 'a')
    time_start = time.time()
    one_task_num=50


    #all_out_data_list = []
    part_out_data_list= []
    #print('len',len(all_urls_list))
    one_process = Pool(one_task_num)

    time_11 = time.time()

    for i in range(0,len(part_urls_list),one_task_num):
        print(i)
        #one_url, title, can_urltodata, content_type, pagedata, root_url, new_alink_list, \
        #jieba_content_keywords, meta_keywords, meta_description=        \
        part_result=one_process.map(geturlsdata, part_urls_list[i:i + one_task_num])
        #part_out_data_list.append([one_url, title, can_urltodata, content_type, pagedata, root_url, new_alink_list, \
        #jieba_content_keywords, meta_keywords, meta_description])
        part_out_data_list.append(part_result)
        #print(result,result[0],result[3])
    time_22 = time.time()


    one_process.close()
    one_process.join()

    time_33 = time.time()
    for part_result in part_out_data_list:
        for one_recoord in part_result:
            #print(one_recoord)
            if one_recoord[1]!='':
                #print('ppp',one_recoord[6])
                #new_urls_file.write(str(one_recoord[6]) + '\n')
                for one_new_url in one_recoord[6]:
                    #print('wwwwwwww',one_new_url)
                    new_urls_file.write(one_new_url+'\n')

                try:
                    urldatasave(filename='testfile', url=str(one_recoord[0]),
                            url_content_key=str(one_recoord[7]),
                            url_content_title=str(one_recoord[1]),
                            url_content_maincontent=str(one_recoord[4]),
                            url_content_keywords=str(one_recoord[8]),
                            url_content_description=str(one_recoord[9]),
                            url_anchor=str(one_recoord[5]),
                            url_content_pagescore=str(one_recoord[10]),
                            tiaoshi=False)
                except Exception as e:
                    mff.write(one_recoord[0] + ',' + str(time.time()) +','+str(e)+ '\n')
                    print('储存失败',e)
            else:
                print('can not url',one_recoord[1]+str(time.time()))
                mff.write(one_recoord[0]+','+str(time.time())+','+str(one_recoord[11])+'\n')

    time_44 = time.time()

    mff.close()
    new_urls_file.close()

    time_end=time.time()
    print('process time', time_22 - time_11)
    print('write time', time_44 - time_33)
    print('part_task_time', time_end - time_start, 's')



def read_urls(read_urlsfile_name):

    time_start=time.time()
    flie_top_1w=open(urls_data_road+read_urlsfile_name)
    urls_list_dq=deque()
    urls_list=[]
    for one_line in flie_top_1w.readlines():
        #print(one_line[:-1]),remove \n
        urls_list_dq.append('http://'+str(one_line[0:-1]))
    time_end=time.time()
    for one in urls_list_dq:
        urls_list.append(one)
    print('read_urls_time',time_end-time_start,'s')
    return urls_list
from control.base_config import urls_data_road
def spider(read_urlsfile_name):

    all_urls_list = read_urls(read_urlsfile_name)
    buchang=500
    for part_i in range(0,len(all_urls_list),buchang):
        ast=time.time()

        print('ptr---------------------------------',part_i)
        #newll=['http://www.toutiao.com','http://www.toutiao.com','http://www.toutiao.com','http://www.toutiao.com','http://www.toutiao.com']
        give_urls_to_geturlsdata_save(all_urls_list[part_i:part_i+buchang])
        wst=time.time()

        aet=time.time()
        print('all_use_time',aet-ast,'all_w_t',aet-wst)


#spider('1486522325.270917.txt')


#1486473432.42246