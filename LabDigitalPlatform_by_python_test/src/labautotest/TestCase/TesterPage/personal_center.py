# -*- coding:UTF-8 -*-
import unittest
from com.framework.webdriver.baseapi.WebdriverBaseApi import WebdriverApi
from com.framework.logging.Recoed_Logging import LogObj
from com.framework.webdriver.basecase.WebDriverBaseCase import WebDriverDoBeforeTest
from labautotest.common.login.loginPage import web_login
from labautotest.data.data_read.ExcelData import ExcelManager
from selenium.webdriver.common.by import By

class PersonalCenter(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.wd = WebDriverDoBeforeTest()
        self.wd.className ="PersonalCenter"
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

    def test_tester_Personal_Center(self):
        '''实验员个人中心测试用例'''
        self.logger.info("test_PersonalCenter.test_tester_Personal_Center测试用例已执行")
        api = self.driverapi
        loginlab = self.weblogin
        
        tes_xls_data = self.em.readexcel("users")  
        nrows = tes_xls_data.nrows
        
        for i in range(1,nrows):       #for循环式，默认从0--n-1
            typeNum = tes_xls_data.cell(i,2).value
            if typeNum == '1': 
                user = tes_xls_data.cell(i,0).value
                passwd = tes_xls_data.cell(i,1).value   
                print "实验室实验员账号密码及类型",user, passwd, typeNum 
                
                b = loginlab.userType_login(user, passwd, typeNum) 
                if b:
                    api.click(By.XPATH, "//a[@href='myinfo']")
                    api.click(By.ID,"ref_but")
                    api.click(By.ID, "update_myinfo_but")
                    
                    oldname = api.getText(By.ID, "show_name")
                    #api.sendKeys(By.ID, "input_name_text", oldname)
                    
                    oldemail = api.getText(By.ID, "show_email")
                    #api.sendKeys(By.ID, "input_email_text",oldemail )
                    
                    newQQ = "1157757910"
                    api.sendKeys(By.ID, "input_tencentno_text", newQQ)
                    
                    newPhone ="18511403089"
                    api.sendKeys(By.ID, "input_phone_text",newPhone )
                    
                    bb = api.isSelected(By.ID, "is_change_pw")
                    if bb is False:
                        api.scrollbar_SlideTOBottom('main_table_left_box')
                        api.click(By.ID, "is_change_pw")
                        newPW = "123456"
                        api.sendKeys(By.ID,"input_pw_text",newPW)
                        api.click(By.ID, "go_update_myinfo_but")
                        api.accept_alert()
                        loginlab.back_LoginPage(2)
                        self.logger.debug("个人中心信息修改为：%s::%s::%s::%s::%s" %(oldname,oldemail,newQQ,newPhone,newPW))
        print "个人中心信息修改测试用例通过"

if __name__ == "__main__":
    unittest.main()