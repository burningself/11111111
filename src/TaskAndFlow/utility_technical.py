# -*- coding: utf-8 -*-
import urllib2,urllib,cookielib
import json
import sys
from StringIO import StringIO
import gzip
from bs4 import BeautifulSoup
from TaskAndFlow.models import *

def urllib2_util_technical():
    resultData = {}
    # 设置保存cookie的文件，同级目录下的cookie.txt
    filename = 'cookie_technical.txt'
   
    # cookie = cookielib.CookieJar()
    # 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    cookie = cookielib.MozillaCookieJar(filename)
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    
    
    # 根据抓包信息 构造headers
    bashheaders = {
        'Accept':'text/html, application/xhtml+xml, */*',
        'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/7.0)',
        'Accept-Language':'zh-CN',
        'Accept-Encoding':'gzip, deflate',
        'Host':'project.scc4.cn:44',
        'Connection':'keep-alive',
        'Cookie':'ASP.NET_SessionId=fqlguf21g541tcfq5jgwnq55',
    }

    try:
        postData={
            "__EVENTTARGET":"",
            "__EVENTARGUMENT":"",
            "__VIEWSTATE":"/wEPDwUKMjA4MTY5MDEzMw8WBB4IdXNlcm5hbWVlHgNwc3dlFgICAQ9kFgICAQ9kFgICBA8PZBYCHgdvbmNsaWNrBRhyZXR1cm4oQ2hlY2tNdXN0SXRlbSgpKTtkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQlpbWdfbG9naW7vHOvShnBKt0yzF3Vm2l73lECfBA==",
            "__EVENTVALIDATION":"/wEWBQKJ2+LLDwLxz5rBDgKQ9vinDwLF8dDtCgL944T5D2BpaLDcaYepk+PaNREV/u1wtsdo",
            "tb_username":"ym2278",
            "tb_password":"111111",
            "tbCheckCode":"ddddd",
            "img_login.x":"24",
            "img_login.y":"23"
        }
        PostUrl = 'http://project.scc4.cn:44/sjxm/login.aspx'
    
        headers = bashheaders.copy()
        headers["Referer"]='http://project.scc4.cn:44/sjxm/login.aspx'
        headers["Content-Type"]='application/x-www-form-urlencoded'
        headers["Content-Length"]='451'
        headers["Cache-Control"]='no-cache'
        
        data = urllib.urlencode(postData)
        request = urllib2.Request(PostUrl,data,headers)
        response = opener.open(request)
        result = response.read()
        cookie.save(ignore_discard=True, ignore_expires=True)
  
        PostUrl = 'http://project.scc4.cn:44/sjxm/ajaxpro/EIS2004Net.Login,eis2006net.ashx'
        headers["Content-Length"] = 51
        headers["Content-Type"] = "text/plain; charset=utf-8"
        headers["Accept"] = "*/*"
        headers["x-ajaxpro-method"] = "setdelphiurl"
        
        postData ='{"str":"http://project.scc4.cn:44/sjxm/login.aspx"}'
        request = urllib2.Request(PostUrl,postData,headers)
        response = opener.open(request)
        print "1111111111111111"
  
        PostUrl = 'http://project.scc4.cn:44/sjxm/ajaxpro/EIS2006Net.Systemasp.AppSys.ExecApp.OutPage.NewAreaSelect,eis2006net.ashx'
        headers["Content-Length"] = 208
        headers["Content-Type"] = "text/plain; charset=utf-8"
        headers["Accept"] = "*/*"
        headers["x-ajaxpro-method"] = "CreateBizrangeSession"
        
        postData='{"DeptWBS":"0004005019009113","currurl":"..\\..\\..\\..\\Systemasp/AppSys/ExecApp/Query/ListProject.aspx?treeno=0186014&Para=o3R5zBuMQKnccv/YBrmNn6vTk0RHRgBQVFou1c4qFXkBL36YXiw¨¹3zk3O¨¹dihFj5","funtype":"10"}'
        request = urllib2.Request(PostUrl,postData,headers)
        response = opener.open(request)
        print "22222222222222222222"

        #PostUrl = 'http://project.scc4.cn:44/sjxm/Systemasp/AppSys/ExecApp/Query/AppQueryList.aspx?para=o3R5zBuMQKnccv/YBrmNn6vTk0RHRgBQVFou1c4qFXkBL36YXiw\250\2713zk3O\250\271dihFj5&SqlQueryCondition=(C_BizRangeId%20in%20(Select%20DeptID%20From%20dbo.GetNewDept([QUOTES]0004005019009113[QUOTES])))&treeno=0186014&showqy=no'
        PostUrl = 'http://project.scc4.cn:44/sjxm/Systemasp/AppSys/ExecApp/Change/AppUpdateList.aspx?para=GSGHfBOJEzT9pPlcjfOTqAKbeE/8Pl/iAQwoxh43LtA=&treeno=0186022&showqy=no&SqlQueryCondition=(C_BizRangeId%20in%20(Select%20DeptID%20From%20dbo.GetNewDept([QUOTES]0004005019009113[QUOTES])))'
        #print PostUrl
        request = urllib2.Request(PostUrl)
        request.add_header("Cookie","ASP.NET_SessionId=fqlguf21g541tcfq5jgwnq55")
        request.add_header("User-Agent","Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/7.0)")
        request.add_header("Connection","keep-alive")
        request.add_header("Accept","text/html, application/xhtml+xml, */*")
        request.add_header("Accept-Encoding","gzip, deflate")
        #request.add_header("Referer","http://project.scc4.cn:44/sjxm/Systemasp/AppSys/ExecApp/Change/AppUpdateList.aspx?para=GSGHfBOJEzT9pPlcjfOTqAKbeE/8Pl/iAQwoxh43LtA=&treeno=0186022&showqy=no&SqlQueryCondition=(C_BizRangeId in (Select DeptID From dbo.GetNewDept([QUOTES]0004005019009113[QUOTES])))")  

        response = urllib2.urlopen(request)
        #print response.info()

        if response.info().get('Content-Encoding') == 'gzip':
            print 'gzip enabled'
            buf = StringIO(response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        else:
            data = response.read()
        
        all_fenye_value = bs4_paraser_fenye(data) 
        all_technical_value = []
        for fenye in all_fenye_value:
            PostUrl = 'http://project.scc4.cn:44/sjxm/Systemasp/AppSys/ExecApp/Change/'+fenye["href"]
            #print PostUrl
            PostUrl = PostUrl.decode('utf-8').encode('gb2312')

            request = urllib2.Request(PostUrl)
            request.add_header("Cookie","ASP.NET_SessionId=fqlguf21g541tcfq5jgwnq55")
            request.add_header("User-Agent","Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/7.0)")
            request.add_header("Connection","keep-alive")
            request.add_header("Accept","text/html, application/xhtml+xml, */*")
            request.add_header("Accept-Encoding","gzip, deflate")
            #request.add_header("Referer","http://project.scc4.cn:44/sjxm/Systemasp/AppSys/ExecApp/Query/AppQueryList.aspx?para=o3R5zBuMQKnccv/YBrmNn6vTk0RHRgBQVFou1c4qFXkBL36YXiwü3zk3OüdihFj5&SqlQueryCondition=(C_BizRangeId in (Select DeptID From dbo.GetNewDept([QUOTES]0004005019009113[QUOTES])))&treeno=0186014&showqy=no");
            response = urllib2.urlopen(request)
            #print response.info()
            
            if response.info().get('Content-Encoding') == 'gzip':
                #print 'gzip enabled'
                buf = StringIO(response.read())
                f = gzip.GzipFile(fileobj=buf)
                data = f.read()
            else:
                data = response.read()
            
            all_technical_value.extend(bs4_paraser_fangan(data))

        syntechnicalinfo(all_technical_value)

    except urllib2.HTTPError,e:
        print e.code


def bs4_paraser_fangan(html):
    all_value = []
    value = {}
    mybytes = html.decode('gb2312','ignore').encode('utf-8')
    soup = BeautifulSoup(mybytes, 'html.parser')
    #print soup.original_encoding
    # 获取所以方案
    all_tr = soup.find_all('tr', attrs={'class': 'query-cntdata'})
    for row in all_tr:
        # 获取每一个方案
        all_td_item = row.find_all('td')
        #print all_td_item
        # 获取方案内容
        #print all_td_item[3].div.font.u.string.encode('gb2312')+" : "+all_td_item[8].string.encode('gb2312')+" : "+all_td_item[11].string.encode('gb2312')
        value['index'] = all_td_item[0].string
        value['number'] = all_td_item[2].string
        value['name'] = all_td_item[3].div.font.u.string
        value['createdate'] = all_td_item[4].string
        value['submitdate'] = all_td_item[5].string
        value['approvedate'] = all_td_item[6].string
        value['hazrd'] = all_td_item[8].string
        value['status'] = all_td_item[11].string
        
        #print value
        all_value.append(value)
        value = {}
    return all_value
        
def bs4_paraser_fenye(html):
    all_value = []
    value = {}
    mybytes = html.decode('gb2312','ignore').encode('utf-8')
    soup = BeautifulSoup(mybytes, 'html.parser')
    #print soup.original_encoding
    # 获取分页
    all_tr = soup.find_all('table', attrs={'width': '90%'}, limit=1)
    for row in all_tr:
        # 获取每一个分页的链接
        all_a_item = row.find_all('a')
        #print all_a_item
        for r in all_a_item:
            # 获取链接内容
            print r.string.encode('gb2312')
            if r.string==u"下一页":
                break
            value['href'] = r['href'].encode('utf-8')
            value['text'] = r.string
            all_value.append(value)
            value = {}
    return all_value
        

def syntechnicalinfo(all_technical_value):
    technical_list_to_insert = list()

    for tech in all_technical_value:
        fangan = Technical.objects.filter(number=tech["number"])
        if fangan:
            fangan = fangan[0]
            if tech["status"]!=u"结束":
                tech['approvedate'] = None
                tech['status'] = 2
                if tech['submitdate']==u"":
                    tech['status'] = 1
            else:
                tech['status'] = 3
            if fangan.status<4:
                fangan.status = tech['status']
            fangan.comment = tech['hazrd']
            fangan.approve_date = tech['approvedate']
            fangan.save()
        else:
            if tech["status"]!=u"结束":
                tech['approvedate'] = None
                tech['status'] = 2
            else:
                tech['status'] = 3
            technical_list_to_insert.append(Technical(number=tech["number"], name=tech["name"], 
                create_date=tech["createdate"], submit_date=tech["submitdate"], approve_date=tech['approvedate'], comment=tech["hazrd"], status=tech["status"], user_id=1))

    Technical.objects.bulk_create(technical_list_to_insert)
