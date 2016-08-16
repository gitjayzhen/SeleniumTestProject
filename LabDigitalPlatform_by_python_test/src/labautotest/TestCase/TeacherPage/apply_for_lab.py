# -*- coding:UTF-8 -*-
import unittest
from com.framework.webdriver.baseapi.WebdriverBaseApi import WebdriverApi
from com.framework.logging.Recoed_Logging import LogObj
from com.framework.webdriver.basecase.WebDriverBaseCase import WebDriverDoBeforeTest
from labautotest.common.login.loginPage import web_login
from labautotest.data.data_read.ExcelData import ExcelManager
from selenium.webdriver.common.by import By
import random

class ApplyLab(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.wd = WebDriverDoBeforeTest()
        self.wd.className ="ApplyLab"
        self.wd.beforeClass()
        
        self.logger = LogObj()
        
        self.weblogin = web_login()
        self.weblogin.back_LoginPage(3)
        
        self.driver = self.weblogin.driver
        self.driverapi = WebdriverApi(self.driver)
        
        self.em = ExcelManager("UsersLogin.xls")
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.driver.close()
        self.wd.afterClass()

    def test_ApplyLab(self):
        '''教师申请实验室用例'''
        self.logger.info("ApplyLab.test_ApplyLab测试用例已执行")
        api = self.driverapi
        loginlab = self.weblogin
        
        tes_xls_data = self.em.readexcel("users")  
        nrows = tes_xls_data.nrows
        
        for i in range(1,nrows):       
            typeNum = tes_xls_data.cell(i,2).value
            if typeNum == '3': 
                user = tes_xls_data.cell(i,0).value
                passwd = tes_xls_data.cell(i,1).value   
                print "实验室管理员账号密码及类型",user, passwd, typeNum 
                b = loginlab.userType_login(user, passwd, typeNum) 
                if b:
                    api.click(By.XPATH, "//a[@href='apply']")
                    api.webList_RandomSelectByOption(By.ID,"year_id", 2)
                    api.webList_RandomSelectByOption(By.ID,"lab_id", 2)
                    api.webList_RandomSelectByOption(By.ID,"class_id", 2)
                    api.webList_RandomSelectByOption(By.ID,"course_id", 2)
                    
                    bb = True
                    while bb :
                        begin = random.randint(1,68)
                        api.sendKeys(By.ID, "ksjc", str(begin))
                        end = random.randint(begin+1,begin+3)
                        api.sendKeys(By.ID, "jsjc", str(end))
                        show = api.getText(By.ID, "ErrorInfo")
                        
                        ebtn = api.is_Displayed(By.CLASS_NAME, "layui-layer-btn0")
                        if ebtn:
                            api.click(By.CLASS_NAME, "layui-layer-btn0")
                            continue
                        if show.strip()=="":
                            bb = False
                            print "执行选择周次"
                            beginWeek = random.randint(1,4)
                            api.selectByValue(By.ID,"kszc",str(beginWeek), 5)
                            endWeek = random.randint(beginWeek+1,beginWeek+5)
                            print "结束周次是：%s"%endWeek
                            api.selectByValue(By.ID,"jszc",str(endWeek), 5)
                        self.logger.debug("课时选择提示：%s"%show)
                        
                    api.click(By.ID, "check_but")
                    show2 = api.getText(By.ID, "ErrorInfo")
                    if "可申请，请点击右侧申请按钮进行申请" == show2:
                        api.click(By.ID, "apply_but")
                        api.click(By.CLASS_NAME, "layui-layer-btn0")
                        result = api.getText(By.CLASS_NAME,"layui-layer-content")
                        self.logger.debug("申请实验室的结果：%s" %result)
                        api.click(By.CLASS_NAME, "layui-layer-btn0")

        print "申请实验室测试用例通过"

if __name__ == "__main__":
    unittest.main()