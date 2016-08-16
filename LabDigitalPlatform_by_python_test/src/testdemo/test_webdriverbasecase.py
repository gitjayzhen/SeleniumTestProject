# -*- coding=utf-8 -*-
'''
Created on 2016年4月29日

@author: jayzhen
'''

from com.framework.webdriver.basecase.WebDriverBaseCase import WebDriverDoBeforeTest


wt = WebDriverDoBeforeTest()
wt.beforeClass()
wt.afterClass()
driver = wt.beforeSuite("ie", "http://www.baidu.com")
wt.afterSuite()
wt.beforeTest("testing webdriverbasecase")
name = wt.afterTest("testing webdriverbasecase", False)
wt.captureScreenshot(name)
wt.capture("testcapture")

driver.close()
