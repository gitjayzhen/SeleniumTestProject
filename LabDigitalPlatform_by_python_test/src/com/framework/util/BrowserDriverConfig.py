# -*- coding:UTF-8 -*-

'''
Created on 2016年4月26日

@author: jayzhen
'''
import ConfigParser
import os
from com.framework.util.FileCheckAndGetPath import FileChecK
from com.framework.logging.Recoed_Logging import LogObj
'''
读取配置文件.conf的内容，返回driver的绝对路径
'''
class GetBrowserDriver():
    def __init__(self):
        self.conf = ConfigParser.ConfigParser()
        self.__fileabspath =None
        self.__projectpath = None
        self.__logger = LogObj() 
        fc = FileChecK()
        boolean = fc.is_has_file("driverpath.conf")
        if boolean: 
            self.__fileabspath = fc.get_fileabspath()
            self.__projectpath = fc.getProjectPath()
        self.conf.read(self.__fileabspath)
    
    def get_IEDriver(self):
        try:
            # 获取指定的section， 指定的option的值
            iedriverpath = self.conf.get("ie", "iedriver")
            iedriverabspath = os.path.join(self.__projectpath,iedriverpath)
            self.__logger.info("获取到IE Driver")
            return iedriverabspath
        except Exception,e:
            self.__logger.error("get_IEDriver()方法出现异常",e)
    
    def get_ChromeDrvier(self):
        try:
            chromedrvierpath = self.conf.get("chrome", "chromedriver")
            chromedriverabspath = os.path.join(self.__projectpath,chromedrvierpath)
            self.__logger.info("获取到Chrome Driver")
            return chromedriverabspath
        except Exception,e:
            self.__logger.error("get_chromedriver()方法出现的异常",e)
    
    def get_FirefoxDrvier(self):
        try:
            firefoxdrvierpath = self.conf.get("firefox", "firefoxdriver")
            #firefoxdrvierabspath = os.path.join(self.__projectpath,firefoxdrvierpath)
            self.__logger.info("获取到Firefox Driver")
            return firefoxdrvierpath
        except Exception,e:
            self.__logger.error("get_FirefoxDrvier()方法出现的异常",e)
'''            
        #获取所有的section
        #sections = self.conf.sections()
        #print sections
    def write_file(self):       
        #写配置文件
        # 更新指定section, option的值
        self.conf.set("section2", "port", "8081")
        # 写入指定section, 增加新option的值
        self.conf.set("section2", "IEPort", "80")
        # 添加新的 section
        self.conf.add_section("new_section")
        self.conf.set("new_section", "new_option", "http://www.cnblogs.com/tankxiao")
        # 写回配置文件
        self.conf.write(open(self.fileabspath,"w"))
 '''       

        
        