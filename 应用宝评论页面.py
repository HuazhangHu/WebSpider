from selenium import webdriver
import time
from pandas import Series ,DataFrame
import pandas as pd
import re

url='http://sj.qq.com/myapp/detail.htm?apkName=com.baidu.lbs.waimai'
driver=webdriver.Chrome()
#用phantomJs创建一个selenium的webdriver

Score=[];Name=[];Date=[];Comment=[]
driver.get(url)
time.sleep(10)
for i in range(30):
    driver.find_element_by_id("J_DetCommentShowMoreBtn").click()#click()点击获取更多
Data=driver.find_elements_by_class_name('det-comment-list-every')
for i in range(len(Data)):
    Name.append(Data[i].find_element_by_class_name('comment-name-line').find_element_by_class_name('comment-name').text.strip())
    Score.append(Data[i].find_element_by_class_name('comment-name-line').find_element_by_xpath("//div[@class='comment-name-line']/div[2]"))

    Date.append(Data[i].find_element_by_class_name('comment-name-line').find_element_by_class_name('comment-date').text.strip("$nbsp;"))
    Comment.append(Data[i].find_element_by_class_name('comment-datatext').text.strip())


data = {'name': Name, 'score': Score, 'date': Date, 'comment': Comment}
table = pd.DataFrame(data)
table.to_csv('C:\\Users\ASUS\Desktop\comments.csv',encoding='utf-8')




