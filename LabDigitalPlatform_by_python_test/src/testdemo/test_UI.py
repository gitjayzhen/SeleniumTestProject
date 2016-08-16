# -*- coding=utf-8 -*-
'''
Created on 2016年4月30日

@author: jayzhen

'''
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import random
'''
driver = webdriver.Firefox()
driver.get("http://192.168.38.129:8080/LabDigitalPlatform_linux/stusign")
weblist = Select(driver.find_element_by_id("class_id")).options
print weblist
webeobj =random.choice(weblist)
print webeobj
print webeobj.get_attribute("value")
print webeobj.text
webeobj.click()
for we in weblist:
    print we.get_attribute("value")
'''
print random.randint(1, 20)  
            

