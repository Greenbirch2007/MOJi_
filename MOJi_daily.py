# -*- coding:utf-8 -*-
import datetime
import re
import time

import pymysql

from lxml import etree
from selenium import webdriver

driver = webdriver.Chrome()

# 2-63
# //*[@id="__layout"]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]
# //*[@id="__layout"]/div/div[2]/div[2]/div[1]/div[63]/div[2]/div[1]




# 可以尝试第二种解析方式，更加容易做计算
def parse_stock_note(html):

    selector = etree.HTML(html)
    code = selector.xpath('//*[@id="pro_body"]/center/div[4]/h1/strong/text()')
    profits= selector.xpath('//*[@id="right_col"]/table/tbody/tr[1]/td/table/tbody/tr[7]/td/text()')
    d_2018= "".join(profits[1][:-3].split(","))
    d_2017= "".join(profits[2][:-3].split(","))
    d_2016= "".join(profits[3][:-3].split(","))

    big_tuple = (code,d_2018,d_2017,d_2016)
    return big_tuple






def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='JS',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into js_FinData (name,d2018,d2017,d2016,industry) values (%s,%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass

def next_page():
    for i in range(1,62):  # selenium 循环翻页成功！
        driver.find_element_by_xpath('//*[@id="tbl_wrap"]/div/a[last()]').click()
        time.sleep(3)
        html = driver.page_source
        return html

if __name__ == '__main__':

    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='JS',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cur = connection.cursor()

    options = webdriver.ChromeOptions()
    url = 'https://www.mojidict.com/search'
    driver.get(url)
    time.sleep(6)
    driver.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[4]/div[1]/span[2]').click()
    time.sleep(6)
    driver.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]').click()
    html = driver.page_source

    print(html)


    #sql 语句
    # for num in range(1236,3686):
    #     big_list = []
    #     sql = 'select coding from js_infos where id = %s ' % num
    #     # #执行sql语句
    #     cur.execute(sql)
    #     # #获取所有记录列表
    #     data = cur.fetchone()
    #     num_coding = data['coding']
    #     url = 'https://profile.yahoo.co.jp/consolidate/' + str(num_coding)
    #
    #     html = get_first_page(url)
    #     content = parse_stock_note(html)
    #     for item in content:
    #         big_list.append(item)
    #     # 加入查询板块的操作
    #     sql = 'select * from js_infos_finanData where id = %s ' % num
    #     # #执行sql语句
    #     cur.execute(sql)
    #     # #获取所有记录列表
    #     data = cur.fetchone()
    #     try:
    #
    #         data_industry = data['industry']
    #         big_list.append(data_industry)
    #         big_list_tuple = tuple(big_list)
    #         finanl_content = []
    #         finanl_content.append(big_list_tuple)  # 是要带着元括号操作，
    #         insertDB(finanl_content)
    #         print(datetime.datetime.now())
    #     except:
    #         pass
    #


# 因为板块数据是最后嵌套进去的，所以要保持，１．数据库表结构，２．解析整理后的数据结构　３．　插入的字段结构　三者之间都要保持一致
# create table js_FinData(
# id int not null primary key auto_increment,
# name varchar(50),
# d2018 varchar(20),
# d2017 varchar(20),
# d2016 varchar(20),
# industry varchar(8)
# ) engine=InnoDB  charset=utf8;

#  drop table js_FinData;