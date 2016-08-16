# -*- coding=utf-8 -*-
'''
Created on 2016年4月28日

@author: jayzhen
'''
from com.framework.browser.Init_Webdriver import InitBrowser

baseURL="http://download.csdn.net/download/zzz889914721/9374830"
initbrowser = InitBrowser()
initbrowser.beforeTestInitBrowser("firefox",baseURL)
driver = initbrowser.getWebDriver()
driver.get("http://www.baidu.com")
initbrowser.stopWebDriver()
print "111111111111111111111111"