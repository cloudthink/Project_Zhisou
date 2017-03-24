# -*- coding: utf-8 -*-
import h5py
import numpy as np
import time

import random
#import google
from control.base_config import road_now
road=road_now
datetime=(time.time())
filename='testfile'


try:
    testfile = h5py.File(road+filename+'_a.hdf5','a')
    print('open')
except:
    print('创建hdf5文件失败，或者写入失败')
url_sum=0
all_data_num=0
for one_url in testfile:
    url_sum=url_sum+1
    print('---------' + one_url)
    for one_time in testfile[one_url]:
        road = one_url + '/' + one_time + '/url_content'
        try:
            print('*******one_url:', one_url, one_time, testfile[road].value,testfile[road].attrs['title'],testfile[road].attrs['pagescore'])
            all_data_num=all_data_num+1
        except:
            print('eeeeeeeee')
    print('url_sum',url_sum,'all_data_num',all_data_num)
print(time.time()-datetime)