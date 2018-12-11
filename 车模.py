import requests
from urllib.parse import urlencode
import json
import os
from hashlib import md5

def get_page(offset):
    params={
        'offset':offset,
        'format':'json',
        'keyword':'车模',
        'autoload':'true',
        'count':'20',
        'cur_tab':'1'
    }
    #拼接url
    url="https://www.toutiao.com/search_content/?"+urlencode(params)
    response=requests.get(url)
    if response.status_code==200:#返回状态码成功，405方法错误，500服务器错误，400错误
       return response.json()#json格式,字典

def get_images(json):#解析数据
    data=json.get('data')
    if data:
        #遍历得到每一个图片的url和标题
        for item in data:
            image_list=item.get('image_list')#图片列表
            title=item.get('title')
            if image_list:
                for image in image_list:#构造一个生成器,返回后保存状态继续执行，
                    yield {
                        'image':image.get('url'),
                        'title':title
                    }
#下载数据保存图片
def save_image(item):#传入
    if not os.path.exists(item.get('title')):#如果没有这样的文件
        os.mkdir(item.get('title'))#以标题生成文件夹名
    #获取图片链接
    local_image_url=item.get('image')
    response=requests.get('http:'+local_image_url)
    if response.status_code==200:
        #0:图片名，
        file_path='{0}/{1}.{2}'.format(item.get('title'),md5(response.content).hexdigest(),'jpg')#将文件名通过md5转换16进制,jpg
        if not os.path.exists(file_path):#如果文件路径不存在
            with open(file_path,'wb') as f:#将图片放入文件夹
                f.write(response.content)

def main(offset):
    #拿到json数据
    json=get_page(offset)
    #得到数据，打印标题，保存数据
    for item in get_images(json):
        print(item)
        save_image(item)

main(500)

