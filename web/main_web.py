# -*- coding: utf-8 -*-
"""This example can handel the URIs
/ -> OnePage.index
/foo -> OnePage.foo -> foo
"""
import re,os
import sys
import urllib
import urllib.request

import cherrypy

#sys.path.append('/Users/zychen/code/zhisearch_linux/')
print(sys.path)

from search.main_search import searchkeywords
html_form='''
<!DOCTYPE html>
<html lang='zh-CN'>
  <head>
    <meta charset='utf-8'>
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <style>
    body { padding-top: 70px; }
    </style>
    <title>zhisou</title>

    <!-- Bootstrap -->
    <link href='css/bootstrap.min.css' rel='stylesheet'>

    <!-- 最新版本的 Bootstrap 核心 CSS 文件 -->
    <link rel='stylesheet' href='https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css' integrity='sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u' crossorigin='anonymous'>

    <!-- 可选的 Bootstrap 主题文件（一般不用引入） -->
    <link rel='stylesheet' href='https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap-theme.min.css' integrity='sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp' crossorigin='anonymous'>

    <!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
    <script src='https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js' integrity='sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa' crossorigin='anonymous'></script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src='https://cdn.bootcss.com/html5shiv/3.7.3/html5shiv.min.js'></script>
      <script src='https://cdn.bootcss.com/respond.js/1.4.2/respond.min.js'></script>
    <![endif]-->


  </head>
  <body>
    <!-- Fixed navbar -->
    <nav class='navbar navbar-default navbar-fixed-top'>
      <div class='container'>
        <div class='navbar-header'>
          <button type='button' class='navbar-toggle collapsed' data-toggle='collapse' data-target='#navbar' aria-expanded='false' aria-controls='navbar'>
            <span class='sr-only'>zhisou</span>
            <span class='icon-bar'></span>
            <span class='icon-bar'></span>
            <span class='icon-bar'></span>
          </button>
          <a class='navbar-brand' href='#'>zhisou</a>
        </div>
        <div id='navbar' class='navbar-collapse collapse'>
          <ul class='nav navbar-nav'>

            <!--<li><a href='#contact'>Contact</a></li>-->

          </ul>
          <form action='/search?word=' class='navbar-form navbar-left' role='search' style='width:70%'>
            <div class='form-group' style='width:70%'>
              <input name='word' type='text' class='form-control' placeholder='Search' style='width:100%'>
            </div>
            <button  class='btn btn-default'>找找</button>

          </form>

          <ul class='nav navbar-nav navbar-right'>
            <li><a href='../navbar/'>开</a></li>
            <li><a href='../navbar-static-top/'>心</a></li>
            <li class='active'><a href='./'>！ <span class='sr-only'>(current)</span></a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>

    <div class='container'>

      <!-- Main component for a primary marketing message or call to action -->
      <div class='jumbotron' style='width:66%'>
        <h3>Happy Search！----换一种搜索引擎，是一种新的生活方式。</h3>
      </div>


'''
#html_form="<!DOCTYPE html><html><head><style>body{background-color:rgb(220,220,220);}a{color:blue;}h1{color:#rgb(20,200,100)}</style></head><body>\
 #       <div style='float:center;'>\
  #      <h1 style='float:center;'>Happy Search！</h1></b>\
   #     <form action='/search?word='><input name='word' type='search' style='width:40%;height:200%;'></input><button>搜索</button></form>\
    #    </div>\
     #   </body></html>"

class Indexpage(object):
    @cherrypy.expose
    def index(self):

        return open('exp_index.html')


    @cherrypy.expose
    def search(self,word='hi!'):
        all_html_answer=""
        (answer_list, answer_list_num, finded_answer_time, all_data_num)=searchkeywords(word)
        all_html_answer="<p>用时(s)："+str(finded_answer_time)+'      从'+str(all_data_num)+"中找到结果："+str(answer_list_num)+"个</p>"
        if len(answer_list)>0:

            for one_answer in answer_list:
                #print(one_answer[0])
                one_url=re.sub('\<\$\#\!\!\#\$\>','/',one_answer[0])
                title=one_answer[1]
                keywords=one_answer[2]
                description=one_answer[3]
                content=one_answer[4]
                one_html_answer='''
                <div class='jumbotron' style='width:66%'>
                <h4>'''+"<a target='_blank' href='http://"+one_url+"'>"+"<h4>"+title+"</h4></b><span>"+one_url+"</span></a></b><p>"+description+"</p>"\
                +'''</h4>
                      </div>

                '''

                all_html_answer=all_html_answer+one_html_answer
            all_html_answer=all_html_answer+'''
                </div>
    <!-- /container -->



    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src='https://cdn.bootcss.com/jquery/1.12.4/jquery.min.js'></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src='js/bootstrap.min.js'></script>
  </body>
</html>
                '''
        else:
            all_html_answer="</b>不好意思，没有帮您找到答案。"
        return html_form+all_html_answer


def index_words_search(words):
    all_html_answer = ""
    (answer_list, answer_list_num, finded_answer_time, all_data_num) = searchkeywords(words)
    all_html_answer = "<p>用时：" + str(finded_answer_time) + '秒      ' + "找到结果：" + str(
        answer_list_num) + "个</p>"
    if len(answer_list) > 0:
        for one_answer in answer_list:
            # print(one_answer[0])
            one_url = re.sub('\<\$\#\!\!\#\$\>', '/', one_answer[0])
            if len(one_url)>30:
                short_url=one_url[0:27]+'...'
            title = one_answer[1]
            if len(title)>34:
                title=title[0:34]+'...'
            #keywords = one_answer[2]
            description = one_answer[3]
            pagescore = one_answer[4]
            one_html_answer = '''
                <div class='jumbotron' style='width:61.8%;padding:2.2%;display:block;' >
                    <h4>''' + "<a target='_blank' href='http://" + one_url + "' >" + title + \
                    "</h4></b></a><p style='font-size:initial;'>" + description + "</p></b>\
                    <span class='.small'>链接：" + one_url + "--好评度："+pagescore+"</span>" \
                + '''
                </div>
                    '''
            all_html_answer = all_html_answer + one_html_answer
    else:
        all_html_answer = "</b>不好意思，没有帮您找到答案。"
    return all_html_answer

@cherrypy.expose
class IndexpageWebService(object):


    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return cherrypy.session['mystring']

    def POST(self, search_words='test'):
        print('get post')
        all_html_answer=index_words_search(search_words)
        some_string = ''.join(all_html_answer)
        #cherrypy.session['mystring'] = some_string
        return some_string

    def PUT(self, another_string):
        cherrypy.session['mystring'] = another_string

    def DELETE(self):
        cherrypy.session.pop('mystring', None)


if __name__ == '__main__':
    from control.base_config import web_host,web_port

    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/indexsearch': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    web_host='127.0.0.1'
    web_port=8080
    cherrypy.config.update({'server.socket_host': web_host,
                            'server.socket_port': web_port,})
    #root = Indexpage()
    #root.login = login
    #root.open = open
    rootweb = Indexpage()
    rootweb.indexsearch = IndexpageWebService()
    cherrypy.quickstart(rootweb, '/', conf)

    #cherrypy.quickstart(root)