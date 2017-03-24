# -*- coding: utf-8 -*-
import time
import os
import re
state=True
from spider.main_spider import spider

while state==True:
    time.sleep(2)
    #print(os.path.abspath('.'))
    #print(os.getcwd())
    now_road=str(os.getcwd())
    urls_data_road=re.sub("control",'data/urls_data',now_road)

    print('runing...', time.time())

    print(os.listdir(urls_data_road))
    for one_file in os.listdir(urls_data_road):
        #print(os.path.splitext(one_file)[0])
    #print([x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1] == '.txt'])
        if 'NO' not in os.path.splitext(one_file)[0]:
            if float(os.path.splitext(one_file)[0])<=time.time():
                print('main----start',os.path.splitext(one_file)[0]+'.txt')
                spider(os.path.splitext(one_file)[0]+'.txt')
                os.rename(urls_data_road+'/'+os.path.splitext(one_file)[0]+'.txt', urls_data_road+'/'+os.path.splitext(one_file)[0]+'_NO.txt')
                #state=False
                print('mainstartend')