import os
import re
from selenium import webdriver
import selenium.webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver=webdriver.Chrome("D:\\谷歌\\chromedriver.exe")
url_login='https://kyfw.12306.cn/otn/login/init'
driver.get(url_login)
time.sleep(3)
username=driver.find_element_by_id('username')
password=driver.find_element_by_id('password')
username.clear()
password.clear()
username.send_keys('13258275830')
password.send_keys('52013143344x')
time.sleep(3)
while True:
    current_url=driver.current_url#driver.current_url代表driver当前页面url
    if current_url!=url_login:
        if current_url[:-1]!=url_login:
            print('登陆成功，跳转中!')
            break
    else:
        time.sleep(5)
        print(u'等待用户图片验证')
#输入账号信息进入界面
book_url='https://kyfw.12306.cn/otn/leftTicket/init'

driver.get(book_url)
driver.find_element_by_id('fromStationText').click()#出发地
driver.find_element_by_xpath('//*[@id="fromStationText"]').send_keys('珞璜南')
driver.find_element_by_xpath('//*[@id="citem_0"]').click()

driver.find_element_by_id('toStationText').click()#目的地
driver.find_element_by_xpath('//*[@id="toStationText"]').send_keys('成都东')
driver.find_element_by_xpath('//*[@id="citem_0"]').click()

driver.find_element_by_id('train_date').click()#选择出发日期
train_date=driver.find_element_by_xpath('/html/body/div[30]/div[1]/div[2]/div[30]/div')
train_date.click()

#判断车票是否还有剩余
#all_ticket = driver.find_element_by_id('queryLeftTable')
#ticket=driver.find_element_by_xpath('//*[@id="ticket_5l0000D35271"]/td[13]/a')

tickets=['D1806:6c000D186001','G8684:78000G868400']
bookable=0
count=0
while bookable==0:
    driver.find_element_by_id('query_ticket').click()  # 点击查询
    time.sleep(5)
    for i in tickets:
        path=i.split(':')[1]#列车编号
        checi=i.split(':')[0]#车次//*[@id="ZE_6c000D180601"]/div
        yd_path = '//*[@id="ticket_' + path + '"]/td[12]/a'  # 预定
        edz_path = '//*[@id="ZE_6c000D180601"]'
        wz_path = '//*[@id="WZ_6c000D180601"]'
        print('正在检测车次'+checi)
        try:
            ticket=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,yd_path)))
            time.sleep(3)
            edz=driver.find_element_by_xpath(edz_path).text()
            print(edz)
            time.sleep(3)
            wz=driver.find_element_by_xpath(wz_path).text()
            print(wz)
            time.sleep(3)
            if edz!='无'or wz!='无':#如果买二等座或者无座有票
                ticket.click()#点击预定
                bookable=1
                break
        except Exception as e:
            #count=count+1
            #print('车次:'+checi+'目前尚不能预定,尝试第'+str(count)+'次')
            print('车次:'+checi+'目前尚不能预定,尝试下一车次')
            #continue
    print('所有车次暂时无法预定,持续刷新中')











