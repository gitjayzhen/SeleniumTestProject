# -*- coding:UTF-8 -*-
import unittest
from com.framework.webdriver.baseapi.WebdriverBaseApi import WebdriverApi
from com.framework.logging.Recoed_Logging import LogObj
from com.framework.webdriver.basecase.WebDriverBaseCase import WebDriverDoBeforeTest
from labautotest.common.login.loginPage import web_login
from labautotest.data.data_read.ExcelData import ExcelManager
from selenium.webdriver.common.by import By

class Class_Management(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.wd = WebDriverDoBeforeTest()
        self.wd.className ="Class_Management"
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

    def test_ClassManagement(self):
        '''网站管理员班级管理测试用例'''
        self.logger.info("Class_Management.test_ClassManagement测试用例已执行")
        api = self.driverapi
        loginlab = self.weblogin
        
        tes_xls_data = self.em.readexcel("users")  
        nrows = tes_xls_data.nrows
        for i in range(1,nrows):       
            typeNum = tes_xls_data.cell(i,2).value
            if typeNum == '4': 
                user = tes_xls_data.cell(i,0).value
                passwd = tes_xls_data.cell(i,1).value   
                print "实验室管理员账号密码及类型",user, passwd, typeNum 
                b = loginlab.userType_login(user, passwd, typeNum) 
                if b:
                    api.click(By.XPATH, "//a[@href='classmanage']")
                    boolean = True
                    while boolean:
                        
                        api.click(By.ID, "ref_but")
                        api.click(By.ID, "add_clazz_but")
                    
                        api.webList_RandomSelectByOption(By.ID, "grade_id", 5)
                        api.webList_RandomSelectByOption(By.ID, "major_id", 5)
                        api.webList_RandomSelectByOption(By.ID, "class_no", 5)
                        api.click(By.ID, "save_clazz_but")
                        
                        bb = api.is_Displayed(By.CLASS_NAME, "layui-layer-content")
                        if bb:
                            content = api.getText(By.CLASS_NAME, "layui-layer-content")
                            if "班级信息存在" == content:
                                api.click(By.CLASS_NAME, "layui-layer-btn0")
                                continue
                            else:
                                api.click(By.CLASS_NAME, "layui-layer-btn0")
                                api.click(By.CLASS_NAME, "close")
                                boolean = False
                break                
        print "班级管理测试用例通过"           

if __name__ == "__main__":
    unittest.main()