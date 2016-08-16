# -*- coding:UTF-8 -*-
'''
Created on 2016年4月26日
@author: jayzhen
'''
import os
from selenium import webdriver
from com.framework.util.BrowserDriverConfig import GetBrowserDriver
from com.framework.logging.Recoed_Logging import LogObj
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from com.framework.util.FileCheckAndGetPath import FileChecK
from com.framework.util.ConfigCommonManager import Config


class InitBrowser():
    '''
    configbrowser本身的self对象去调用其他的类方法
    '''
    def __init__(self):
        
        self.__GBD = GetBrowserDriver()
        self.__logger = LogObj()
        self.driver = None
        fc = FileChecK()
        boolean = fc.is_has_file("framework.ini")
        if boolean:
            self.inipath = fc.get_fileabspath()
            
        self.fw_conf = Config(self.inipath)
        self.waitTimeout = self.fw_conf.get("TimeSet", "waitTimeout")
        self.scriptTimeout = self.fw_conf.get("TimeSet", "scriptTimeout")
        self.pageLoadTimeout = self.fw_conf.get("TimeSet", "pageLoadTimeout")
        
    
    def beforeTestInitBrowser(self,browsername,baseURL):
        if "chrome" == browsername:
            self.startChromeDriver(baseURL)
        elif "ie" == browsername:
            self.startInternetExplorerDriver(baseURL)
        elif "firefox" == browsername:
            self.startFirefoxDriver(baseURL)
        else:
            self.startFirefoxDriver(baseURL)

    def startFirefoxDriver(self,baseURL):
        try:
            firefoxdriver = self.__GBD.get_FirefoxDrvier()
            os.environ["webdriver.firefox.bin"] = firefoxdriver
            self.driver = webdriver.Firefox()
            
            self.driver.set_page_load_timeout(self.pageLoadTimeout)
            self.__logger.debug("set pageLoadTimeout : "+self.pageLoadTimeout);
            self.driver.implicitly_wait(self.waitTimeout)
            self.__logger.debug("set waitTimeout : " +self.waitTimeout)
            self.driver.set_script_timeout(self.scriptTimeout)
            self.__logger.debug("set scriptTimeout : " +self.scriptTimeout);
            self.__logger.info("初始化火狐浏览器成功")
            self.driver.maximize_window()
            self.get(baseURL, 3)
        
        except Exception,e:
            self.__logger.error("getFirefoxDriver()方法发生异常，异常信息："+e)
    
    def startChromeDriver(self,baseURL):
        try:
            chromedriver = self.__GBD.get_ChromeDrvier()
            os.environ["webdriver.chrome.driver"] = chromedriver
            self.driver = webdriver.Chrome(chromedriver)
            
            self.driver.set_page_load_timeout(self.pageLoadTimeout)
            self.__logger.debug("set pageLoadTimeout : "+self.pageLoadTimeout);
            self.driver.implicitly_wait(self.waitTimeout)
            self.__logger.debug("set waitTimeout : " +self.waitTimeout)
            self.driver.set_script_timeout(self.scriptTimeout)
            self.__logger.debug("set scriptTimeout : " +self.scriptTimeout);
            self.driver.maximize_window()
            self.__logger.info("初始化谷歌浏览器成功")
            self.get(baseURL, 3)
        except Exception,e:
            self.__logger.error("getChromeDriver()方法出现异常"+str(e))
    
    def startInternetExplorerDriver(self,baseURL):
        try:
            ie_dc = DesiredCapabilities.INTERNETEXPLORER
            ie_dc['INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS']=True
            ie_dc['ignoreProtectedModeSettings'] = True
            ie_dc['NATIVE_EVENTS'] = False
            ie_dc["unexpectedAlertBehaviour"] = "accept" 
            iedriver = self.__GBD.get_IEDriver()
            os.environ["webdriver.ie.driver"] = iedriver
            self.driver = webdriver.Ie(iedriver,ie_dc)
            
            self.driver.set_page_load_timeout(self.pageLoadTimeout)
            self.__logger.debug("set pageLoadTimeout : "+self.pageLoadTimeout);
            self.driver.implicitly_wait(self.waitTimeout)
            self.__logger.debug("set waitTimeout : " +self.waitTimeout)
            self.driver.set_script_timeout(self.scriptTimeout)
            self.__logger.debug("set scriptTimeout : " +self.scriptTimeout);
            self.driver.maximize_window()
            
            self.__logger.info("初始化IE浏览器成功")
            self.get(baseURL, 3)
        except Exception,e:
            self.__logger.error("getInternetExplorerDriver()方法出现异常"+e)

    def stopWebDriver(self):
        try: 
            self.driver.quit();
            self.__logger.info("stop Driver");
        except Exception,e:
            self.__logger.error("执行stopWebDriver()方法发生异常，异常信息："+ e);

    def get(self, url, actionCount):
        for i in range(actionCount):
            try:
                self.driver.get(url);
                self.__logger.debug("navigate to url [ " + url + " ]");
                break;
            except Exception,e:
                self.__logger.error(e);

    def getWebDriver(self):
        return self.driver



