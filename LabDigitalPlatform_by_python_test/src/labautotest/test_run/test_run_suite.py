# -*- coding:UTF-8 -*-

import unittest, HTMLTestRunner    #在系统中导入所需要的框架模块
from labautotest.run.produce_reporter.html_reporter import html_reporter
from labautotest.run.basic.run_basic import lists_class
from com.framework.logging.Recoed_Logging import LogObj
from com.framework.Emails.SendEmail import Emails
from com.framework.webdriver.basecase.WebDriverBaseCase import WebDriverDoBeforeTest
import time


def test_run_suite():
    logger = LogObj()
    logger.debug("测试集test_run_suite执行了")
    html_obj = html_reporter()      #调用html测试报告方法
    suite = unittest.TestSuite()    #调用套件自动执行容器 
    
    for key in lists_class:
        #将lists_class中的类通过加载器进行加载
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(key))
        
    #使用htmltestrunner生成html报告
    tle = "   LabDigitalPlatform By Python Design Testing By Author jayzhen"
    drp = "   基于Spring MVC的实验室数字化平台-自动化测试 V1.0版本 -自动化测试报告"
    runner = HTMLTestRunner.HTMLTestRunner(stream=html_obj,title=tle,description=drp)
    #批量执行容器中的测试用例
    runner.run(suite)
    
wd = WebDriverDoBeforeTest()  
wd.beforeSuite()  
test_run_suite() 
time.sleep(6)
#Emails().SendEmail_withFile()
print "所有脚本执行完成"
wd.afterSuite()      
    
    
    
    
    