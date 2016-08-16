# -*- coding:UTF-8 -*-
'''
Created on 2016年4月29日
@author: jayzhen
'''
from com.framework.logging.Recoed_Logging import LogObj
from com.framework.util.ConfigCommonManager import Config
from com.framework.util.FileCheckAndGetPath import FileChecK
from com.framework.webdriver.basecase.WebDriverBaseCase import WebDriverDoBeforeTest
'''
在配置文件中设置好需要run的浏览器，通过fc对象获取
'''
def RunBrowser(baseURL):
    fc = FileChecK()
    boolean = fc.is_has_file("RunWhichBrowser.ini")
    if boolean:
        rwb_ini_path = fc.get_fileabspath()
    conf = Config(rwb_ini_path)
    runBrowser = conf.get("run", "browser")
    LogObj().debug("======本次试用%s浏览器进行测试======" %runBrowser)
    driver =WebDriverDoBeforeTest().getDriverTooler(runBrowser, baseURL)
    return driver
#RunBrowser("http://192.168.38.129:8080/Lab_linux/login")        
    