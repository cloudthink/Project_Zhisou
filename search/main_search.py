# -*- coding: utf-8 -*-
import datetime
import timeit

import h5py


def searchkeywords(words,tiaoshi=False):
    begin_time = datetime.datetime.now()

    from control.base_config import search_road,storage_file_name
    road=search_road
    #road = get_hdf5_road()
    #datetime=str(int(time.time()))
    filename=storage_file_name
    all_data_num=0
    answer=[]
    answer_list=[]
    try:
        testfile = h5py.File(road+filename+'.hdf5',mode='r',driver='core',backing_store=True)#
    except:
        print('can not open hdf5 file with r type, so can not read file')
    ###
    # hdf5文件结构:www.baidu.com/123091211(时间戳）/url_content（统一字段）
    # one_url_content.values=url_content_key
    # one_url_content.attrs['title']=url_content_title
    # one_url_content.attrs['content']=url_content_maincontent
    # one_url_content.attrs['keywords'] = url_content_keywords
    # one_url_content.attrs['description']=url_content_description
    # 还可以继续添加单个url特性
    # one_url_content.attrs['languange']='zh|en'
    ###


    for one_url in testfile:
        if len(answer_list) < 10:
            try:
                for one_time in testfile[one_url]:
                    road = one_url + '/' + one_time + '/url_content'
                    all_data_num = all_data_num + 1
                    try:
                        #print('*******one_url:', one_url, one_time, testfile[road].value,testfile[road].attrs['content'])
                        content_key=testfile[road].value
                        title=testfile[road].attrs['title']
                        #content=testfile[road].attrs['content']
                        keywords=testfile[road].attrs['keywords']
                        description=testfile[road].attrs['description']
                        pagescore=testfile[road].attrs['pagescore']
                        if words in (title or keywords):
                            answer=[one_url,title,keywords,description,pagescore]
                            answer_list.append(answer)
                            #print(title,keywords)
                        #else:
                         #   print(title)

                    except Exception as e:
                        print('search keywords fail',e)
                        try:
                            delroad=one_url + '/' + one_time
                            del testfile[delroad]
                        except Exception as ee:
                            print('del fail ',ee)
            except:
                pass
        else:
            break
    answer_list_num=len(answer_list)

    end_time = datetime.datetime.now()

    finded_answer_time=end_time-begin_time
    if tiaoshi==True:
        print(answer_list_num,finded_answer_time,all_data_num)
    return (answer_list,answer_list_num,finded_answer_time,all_data_num)

if __name__ == '__main__':

    #print(timeit.timeit("test()", setup="from __main__ import test"))
    print(str(timeit.timeit("searchkeywords('b',tiaoshi=True)",setup="from __main__ import searchkeywords",number=1,))+'s')