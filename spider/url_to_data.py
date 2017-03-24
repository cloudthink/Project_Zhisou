# -*- coding: utf-8 -*-
import urllib
#编码检测工具
import chardet
import urllib.request
import re
from bs4 import BeautifulSoup
import jieba
import jieba.analyse
import random

from rank.main_rank import rankoneurl
USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
USER_PROXIE='http://127.0.0.1:80'
#USER_PROXIE='http://222.186.161.215:3128'
def urltodata(url='http://toutiao.com',user_agent=USER_AGENT,proxie=USER_PROXIE,tiaoshi=False):
    import socket
    print(url)
    my_timeout = 10
    socket.setdefaulttimeout(my_timeout)
    title = can_urltodata = content_type = pagedata = root_url = alink_list = \
        jieba_content_keywords = meta_keywords = meta_description = ''
    #print('start',url)
    can_urltodata=True
    req = urllib.request.Request(url, headers = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': user_agent
    })
    #urllib.request.ProxyHandler({'https': proxie})
    #proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
    #proxy_auth_handler.add_password('realm', 'host', 'username', 'password')

    #opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
    # This time, rather than install the OpenerDirector, we use it directly:
    #opener.open('http://www.example.com/login.html')

    error_log=['']
    #print(google.get_page(url))
    try:
        urlop = urllib.request.urlopen(req, timeout=2,proxies={"http":proxie})
        try:
            content_type=urlop.getheader('Content-Type')

            # 先获取网页内容
            decode_data = urllib.request.urlopen(req).read()

            # 用编码检测组件chardet进行内容分析,{'confidence': 0.99, 'encoding': 'utf-8'},表示99%的概率认为是utf-8
            chardit = chardet.detect(decode_data)
            #print(chardit)

            content_charset=chardit['encoding']
            #print(content_charset)
            if 'html' in content_type:

                alink_list=[]
                # 用突utf-8编码输，避免程序异常中止, 用try..catch处理异常

                try:
                    data = urlop.read().decode(content_charset)
                    #print(len(data))
                    #data = data.replace(" ","")
                    #data = data.replace("\n", "")
                    #data = data.replace("\r", "")
                    #data = data.replace("\t", "")
                    #print(len(data),data)
                except Exception as e:
                    error_log.append(e)
                    #print('can not decode:'+content_charset,content_type,url)
                    can_urltodata=False
                pagedata=str(data)
                htmlsoup = BeautifulSoup(data,'html.parser')
                try:
                    title = str(htmlsoup.title.string)
                except:
                    title='null'

                try:
                    #meta_description=htmlsoup.meta
                    meta_description = htmlsoup.find(attrs={"name":"description"})['content']
                except:
                    meta_description= 'null'

                try:
                    meta_keywords = htmlsoup.find(attrs={"name":"keywords"})['content']
                except:
                    meta_keywords = 'null'

                #print(meta_description,meta_keywords)

                try:
                    #newhtmlsoup=htmlsoup.find('script').extract()
                    for script in htmlsoup.findAll('script'):
                        script.extract()
                    newhtmlsoup=htmlsoup
                    #print(newhtmlsoup)
                    str_content=newhtmlsoup.get_text()
                    #print(str_content)
                    tags = jieba.analyse.extract_tags(str_content, topK=10)
                    tags=",".join(tags)
                    #print(",".join(tags))
                    jieba_content_keywords=str(tags)
                except:
                    try:
                        jieba_content_keywords=meta_keywords
                    except:
                        jieba_content_keywords=title

                #提取网站路径
                urlregular = r'^https?:\/\/([a-z0-9\-\_\.a-z0-9\-\_\.]+)[\/\?]?'
                # url = 'http://baike.segme-ntfault.com/blog/biu/1190000000330941//fafsd/aasfdaf'
                m = re.match(urlregular, url)
                root_url = (m.group())
                if root_url[-1] == '/':
                    root_url = root_url[:-1]

                # 将不完整的url补充完整，并判断该url是否已经爬取过
                for one_link in htmlsoup.find_all('a'):
                    one_link=str(one_link.get('href'))

                    if (('https' not in one_link) and (('http' not in one_link))):
                        if ('//' not in one_link) and ('javascript' not in one_link) and ('None' not in one_link):
                            whole_one_link = root_url + one_link

                        elif 'javascript' in one_link:
                            whole_one_link = root_url + '/' + one_link


                        #rm_http_url=re.sub('http://','',httpurl)
                        rm_https_url = re.sub('http.*://', '', whole_one_link)
                        if rm_https_url not in alink_list:
                            alink_list.append(rm_https_url)
                    #print('ll',one_link.get('href'))
                    # http://example.com/elsie


        except Exception as ee:
            error_log.append(ee)
            print('error:urlopen',url,content_type,content_charset,ee)
            can_urltodata=False
        #if tiaoshi==True:
        #    print(htmlsoup.title, content_charset, content_type, pagedata)


        if tiaoshi==True:
            print(title, can_urltodata, content_type, pagedata, root_url,alink_list,jieba_content_keywords,meta_keywords,meta_description)
        #print(jieba_content_keywords)
        #print('CANTODATA',url,can_urltodata)
    except Exception as eee:
        error_log.append(eee)
        can_urltodata==False
        #print('ooo')

    if can_urltodata==True:
        if len(title)>10:
            print(title,alink_list)
        page_score = rankoneurl(url, pagedata, root_url,alink_list,jieba_content_keywords,meta_keywords,meta_description)
        return (title, can_urltodata, content_type, pagedata, root_url,alink_list,jieba_content_keywords,meta_keywords,meta_description,error_log,page_score)
    else:
        title = can_urltodata = content_type = pagedata = root_url = new_alink_list = \
            jieba_content_keywords = meta_keywords = meta_description = page_score=''
        if error_log=='':
            error_log='wuwuwuwu'
        return (title, can_urltodata, content_type, pagedata, root_url,alink_list,jieba_content_keywords,meta_keywords,meta_description,error_log,page_score)

if __name__ == '__main__':
    urltodata(tiaoshi=True)
