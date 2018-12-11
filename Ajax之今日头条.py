import requests
from urllib.parse import *
import os
from hashlib import md5
from multiprocessing.pool import Pool#多线程的进程池


#Request URL: https://www.toutiao.com/search_content/?offset=0&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=1&from=search_tab
def get_page(offset):
    params={
        'offset':offset,
        'format':'json',
        'keyword':'街拍',
        'autoload':'true',
        'count':'20',
        'cur_tab':'3',
    }
    base_url='https://www.toutiao.com/search_content/?'
    url=base_url+urlencode(params)
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.json()
    except requests.ConnectionError as e:#连接错误
        print('Error',e.args)

def get_images(json):
    if json:
        for item in json.get('data'):
            print(item)
            title=item.get('title')
            images=item.get('image_list')
            if images:
                for image in images:#将图片链接以及所属的标题一并返回
                    yield {#构造器
                        'image':image.get('url'),
                        'title':title
                    }

def save_images(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response=requests.get(item.get('image'))
        if response.status_code==200:
            file_path='{0}/{1}.{2}'.format(item.get('title'),md5(response.content).hexdigest(),'jpg')
            #以标题作为文件名,将图片的内容转换为十六进制格式，已经jpg的形式存储
            if not os.path.exists(file_path):
                with open(file_path,'wb') as f:
                    f.write(response.content)
            else:
                print("已经下载",file_path)
    except requests.ConnectionError as e:
        print('无法获取图片')

def main(offset):
    json=get_page(offset)
    print(json)
    items=get_images(json)
    for item in items:
        save_images(item)

GROUP_START=1
GROUP_END=20

#利用多线程的进程池
if __name__ == '__main__':
    pool=Pool()
    groups=([x*20 for x in range(GROUP_START,GROUP_END+1)])
    pool.map(main,groups)#调用map方法实现多进程下载
    pool.close()
    pool.join()
    
