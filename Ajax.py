from urllib.parse import *
import requests
from pyquery import PyQuery as pq

base_url='https://m.weibo.cn/api/container/getIndex?'
#编写请求头，在request Headers里面
headers={
    "Host":"m.weibo.cn",
    "Referer":'https://m.weibo.cn/u/2830678474',
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Mobile Safari/537.36",
    "X-Requested-With":"XMLHttpRequest",

}
#type=uid&value=2830678474&containerid=1076032830678474
def get_page(page):
    params={
        'type':'uid',
        'value':'2830678474',
        'containerid':'1076032830678474',
        'page':page

    }
    url=base_url+urlencode(params)#转换为url的get请求参数
    try:
        response=requests.get(url,headers)#发送请求时连同header一起发送
        if response.status_code==200:
            return response.json()#通过JSON()方法解析成为json格式
    except requests.ConnectionError as e:#如果出现链接错误，命名为e
        print('Error',e.args)#打印错误信息

def parse_page(json):
    if json:
        items=json.get('data').get('cards')
        for item in items:
            item=item.get('mblog')
            weibo={}
            weibo['id']=item.get('id')
            weibo["text"]=pq(item.get("text")).text()#借助pyquery把正文中的标签去掉
            weibo["attitudes"]=item.get("attitudes_count")
            weibo['comment']=item.get('comments_count')
            weibo["reposts"]=item.get("reposts_count")
            yield weibo

if __name__=='__main__':
    for page in range(1,11):
        json=get_page(page)
        print(json)
        results=parse_page(json)
        for result in results:
            print(result)