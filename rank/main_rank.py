# -*- coding: utf-8 -*-
import random
import re
def rankoneurl(oneurl='', pagedata='asdasdasd', root_url='',alink_list=['asd','as'],\
               jieba_content_keywords='',meta_keywords='',meta_description='',tiaoshi=False):
    jieba_content_keywords=re.sub(' ','',jieba_content_keywords)
    jieba_content_keywords=re.sub(',','',jieba_content_keywords)

    meta_keywords=re.sub(' ','',meta_keywords)
    meta_keywords=re.sub(',','',meta_keywords)

    i_score=0.1
    len_j=len(jieba_content_keywords)+0.0001
    len_m=len(meta_keywords)+0.0001
    for i in jieba_content_keywords:
        if i in meta_keywords:
            i_score=i_score+1

    for i in meta_keywords:
        if i in jieba_content_keywords:
            i_score=i_score+1

    score=i_score/float(len_j+len_m)
    if score==0:
        score=0.00001
    if tiaoshi==True:
        print(score)
    return str(score)

if __name__ == '__main__':
    rankoneurl(jieba_content_keywords='哈哈 haha',meta_keywords='呵呵 hehe',tiaoshi=True)