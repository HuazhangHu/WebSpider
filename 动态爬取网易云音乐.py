from selenium import webdriver
import csv
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')#注意编码方式，很容易出问题
url="http://music.163.com/#/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=0"
driver=webdriver.Chrome()
#用phantomJs创建一个selenium的webdriver
csv_file=open("C:\\Users\ASUS\Desktop\playlist.csv","w",newline="",encoding='utf-8')#创建csv文件
writer=csv.writer(csv_file)
writer.writerow(["标题","播放数","链接"])

while url !='javascript:void(0)':
    driver.get(url)#用webdriver加载界面
    driver.switch_to_frame('contentFrame')#切换至内容的iframe框架，相当于在父级Frame下的子iframe
    data=driver.find_element_by_id('m-pl-container').find_elements_by_tag_name('li')#解析一页中的所有歌单,返回标签列表
    for i in range(len(data)):
        nb=data[i].find_element_by_class_name('nb').text
        nb=nb.split('万')[0]
        msk=data[i].find_element_by_css_selector("a.msk")#获取封面
        writer.writerow([msk.get_attribute('title'),nb,msk.get_attribute('href')])#获取界面的标题和链接
    url=driver.find_element_by_css_selector("a.zbtn.znxt").get_attribute('href')
csv_file.close()


