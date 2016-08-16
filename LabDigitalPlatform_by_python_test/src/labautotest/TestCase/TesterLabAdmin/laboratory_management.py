# -*- coding:UTF-8 -*-
import unittest
from com.framework.webdriver.baseapi.WebdriverBaseApi import WebdriverApi
from com.framework.logging.Recoed_Logging import LogObj
from com.framework.webdriver.basecase.WebDriverBaseCase import WebDriverDoBeforeTest
from labautotest.common.login.loginPage import web_login
from labautotest.data.data_read.ExcelData import ExcelManager
from selenium.webdriver.common.by import By
import random

class LaboratoryManagement(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.wd = WebDriverDoBeforeTest()
        self.wd.className ="LaboratoryManagement"
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

    def test_LaboratoryManagement(self):
        '''实验员管理测试用例'''
        self.logger.info("LaboratoryManagement.test_LaboratoryManagement测试用例已执行")
        api = self.driverapi
        loginlab = self.weblogin
        
        tes_xls_data = self.em.readexcel("users")  
        nrows = tes_xls_data.nrows
        for i in range(1,nrows):       
            typeNum = tes_xls_data.cell(i,2).value
            if typeNum == '2': 
                user = tes_xls_data.cell(i,0).value
                passwd = tes_xls_data.cell(i,1).value   
                print "实验室管理员账号密码及类型",user, passwd, typeNum 
                b = loginlab.userType_login(user, passwd, typeNum) 
                if b:
                    api.click(By.XPATH, "//a[@href='lab_tech']")
                    api.click(By.ID, "ref_but")
                    api.click(By.ID, "add_lab_tech_but")
                    
                    num = random.randint(1, 20)
                    newname = "jayzhen"+ str(num)
                    api.sendKeys(By.ID, "lab_tech_name_text",newname)
                    
                    newemail = "1234546@qq.com"
                    api.sendKeys(By.ID, "lab_tech_email_text",newemail)
                    
                    newqq = str(random.randint(111111, 999999999))
                    api.sendKeys(By.ID, "lab_tech_qq_text",newqq)
                    
                    newphone = str(random.randint(18311111111, 18399999999))
                    api.sendKeys(By.ID, "lab_tech_phone_text",newphone)
                    
                    api.webList_RandomSelectByOption(By.ID, "lab_id", 3)
                    
                    api.click(By.ID, "save_lab_tech_but")
                    
                    bb = api.is_Displayed(By.CLASS_NAME, "layui-layer-btn0")
                    if bb:
                        errorcont = api.getText(By.CLASS_NAME, "layui-layer-btn0")
                        self.logger.debug("填完新增实验员的内容后，点击确定，提示：%s" %errorcont)
                        api.click(By.CLASS_NAME, "layui-layer-btn0")
                    api.click(By.CLASS_NAME, "close")
        print "实验室管理测试用例通过"

if __name__ == "__main__":
    unittest.main()