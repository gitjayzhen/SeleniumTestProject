#coding:utf-8
'''
Created on 2016年4月30日
@author: jayzhen
'''
import unittest
from com.framework.logging.Recoed_Logging import LogObj
from com.framework.webdriver.basecase.WebDriverBaseCase import WebDriverDoBeforeTest
from com.framework.webdriver.baseapi.WebdriverBaseApi import WebdriverApi
from labautotest.data.data_read.ExcelData import ExcelManager
from labautotest.common.login.loginPage import web_login
from selenium.webdriver.common.by import By

class SignIn(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.logger = LogObj()
        
        self.weblogin = web_login()
        self.weblogin.back_SigninPage() #返回到student 签到的页面
        
        self.wd = WebDriverDoBeforeTest()
        self.wd.className ="studentSignin.Signin"
        self.wd.beforeClass()
        self.wd.driver = self.weblogin.driver   
        
        self.webdriverpai = WebdriverApi(self.weblogin.driver)
        self.em = ExcelManager("UsersLogin.xls")
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.wd.afterClass()
        self.weblogin.driver.close()

    def test_student_singin(self):
        '''学生签到测试用例'''
        try:
            self.logger.info("SignIn.test_student_singin 测试用例已执行")
            api = self.webdriverpai
            
            tes_xls_data = self.em.readexcel("students")  #得到sheet页
            nrows = tes_xls_data.nrows
            print "------ excel中的测试用例条数是：",nrows-1    #excel中 的数据行数从1行开始
            for i in range(1,nrows):       #for循环式，默认从0--n-1
                print "------ 这是第：",i," 条用例"
                row_A = str(tes_xls_data.cell(i,0).value)
                row_B = str(tes_xls_data.cell(i,1).value)
                row_C = tes_xls_data.cell(i,2).value
                print row_A, row_B, row_C 
                
                api.webList_RandomSelectByOption(By.ID, "class_id", 3)
                api.webList_RandomSelectByOption(By.ID, "lab_id", 3)
                api.sendKeys(By.ID, "name",row_A)
                api.sendKeys(By.ID, "stuno",row_B)
                api.sendKeys(By.ID, "info",row_C)
                api.click(By.ID, "sign")
                b = api.is_Displayed(By.CLASS_NAME,"layui-layer-btn0")
                if b:
                    capturename = api.getText(By.CLASS_NAME, "layui-layer-content")
                    if "欢迎使用实验室数字化平台签到" != capturename:
                        self.wd.capture(capturename)
                        api.click(By.CLASS_NAME,"layui-layer-btn0")
                self.weblogin.back_SigninPage() #返回到student 签到的页面
        except Exception,e:
                self.logger.error("SignIn.test_student_singin 测试用例出现异常"+str(e))

if __name__ == "__main__":
    unittest.main()