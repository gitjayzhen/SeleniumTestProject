#coding:utf-8
'''
Created on 2016年4月30日
@author: jayzhen
'''
import unittest
from com.framework.logging.Recoed_Logging import LogObj
from com.framework.webdriver.basecase.WebDriverBaseCase import WebDriverDoBeforeTest
from com.framework.webdriver.baseapi.WebdriverBaseApi import WebdriverApi
from labautotest.common.login.loginPage import web_login
from selenium.webdriver.common.by import By
from com.framework.databases.sqlcontrol import Execute_SQL
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
        
        self.conn = Execute_SQL()
        
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.wd.afterClass()
        self.weblogin.driver.close()
        self.conn.execute_conn_close()
        
    def test_student_singin(self):
        '''学生签到测试用例'''
        try:
            self.logger.info("SignIn.test_student_singin 测试用例已执行")
            api = self.webdriverpai
            sql = 'select * from test_lab;'
            res = self.conn.execute_select(sql)
            for i in res:       #for循环式，默认从0--n-1
                print "------ mysql testcase:",i
                row_A = i[0]
                row_B = i[1]
                row_C = i[2]
                
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
            print u"平台学生签到测试用例通过"
        except Exception,e:
                self.logger.error("SignIn.test_student_singin 测试用例出现异常"+str(e))
        
if __name__ == "__main__":
    unittest.main()