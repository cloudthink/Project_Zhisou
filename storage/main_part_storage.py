# -*- coding: utf-8 -*-
import time

import h5py


#import google

def urldata_partsave(filename='testfile',
                url='www.baidu.com',
                url_content_key="urlkey guanjianci 关键词",
                url_content_title="title biaoti 标题",
                url_content_maincontent="content neirong 内容",
                url_content_keywords="meta_keywords",
                url_content_description="meta_description",
                url_anchor='http://www.baidu.com',
                tiaoshi=False):
    #from base_config read base config
    from control.base_config import storage_road
    road=storage_road
    datetime=str((time.time()))
    #filename=storage_file_name
    try:
        #open hdf5 file
        testfile_object = h5py.File(road+filename+'.hdf5','a')
    except:
        print('can not open hdf5 file with a type, so can not write file')


    try:
        url_data_num = len(testfile_object[url])
        if url_data_num >= 3:
            min_last_time = 999999999999999.0
            for one_time in testfile_object[url]:
                if float(one_time) <= min_last_time:
                    min_last_time = float(one_time)
            del testfile_object[url + '/' + str(min_last_time)]
            # print(one_time)
            # print(testfile_object[url+'/'+one_time].name)
            # del testfile_object[url+'/'+one_time]
        else:
            print(url_data_num)

    except:
        print("can not read url number")

    try:
        #hdf5/url/datetime
        data_save_road=url+'/'+datetime
        geturl_key=testfile_object.create_group(data_save_road)
        #geturl_key.attrs['url_father']=url_father
        #geturl_key.attrs['url_son']=url_son
        #print(geturl_key.name)
        datatype_str = h5py.special_dtype(vlen=str)
        one_url_content = geturl_key.create_dataset('url_content', dtype=datatype_str, data=url_content_key)
        one_url_content.attrs['title']=url_content_title
        one_url_content.attrs['content']=url_content_maincontent
        one_url_content.attrs['keywords'] = url_content_keywords
        one_url_content.attrs['description']=url_content_description
        #还可以继续添加单个url特性
        one_url_content.attrs['languange']='zh|en'
        #mtitle[0] = url_content
        #url_anchor,data type is list, 所有引用该页面的链接
        #mtitle[1] = url_anchor

        #调试状态测试写入情况
        print('write data in hdf5 file success：')
        print('|filename:', testfile_object.name,
              '|roadname:', geturl_key.name,
              '|url_content_key:', geturl_key['url_content'].value)
        if tiaoshi==True:
            try:
                print('|filename:',testfile_object.name,
                      '|roadname:',geturl_key.name,
                      '|url_content_key:',geturl_key['url_content'].value ,
                      '|title:',geturl_key['url_content'].attrs['title'],
                      '|content',geturl_key['url_content'].attrs['content'][50:100],
                      '|lanuange:' ,geturl_key['url_content'].attrs['languange'])
                #,mtitle[0],'url_anchor', str(mtitle[1]))
                      #geturl_key.attrs['date'])

            except:
                print('tiaoshi shibai')

    except:
        print('hdf5 file can open ,but data can not write')

    testfile_object.flush()
    testfile_object.close()

    #清除缓存，将数据从内存储存到磁盘


if __name__ == '__main__':
    one_url='www.to9utiao.com'
    title='<title>《今日头条》你关心的,才是头条! - www.toutiao.com</title>'
    root_url='http://www.toutiao.com'
    from control.base_config import storage_road, storage_file_name

    road = storage_road
    filename = storage_file_name
    try:
        #open hdf5 file
        testfile_object = h5py.File(road+filename+'.hdf5','a')
    except:
        print('can not open hdf5 file with a type, so can not write file')
    #urldatasave(filename = 'urlfile', url = one_url, url_content = title, url_anchor = root_url, tiaoshi = True)
    urldatasave(filename='testfile',url='www.baidu.com',
                url_content_key="urlkey guanjianci 关键词",
                url_content_title="title biaoti 标题",
                url_content_maincontent="content neirong 内容",
                url_anchor='http://www.baidu.com',tiaoshi=True)
