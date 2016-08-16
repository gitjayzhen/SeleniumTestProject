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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import random

class SignIn(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        
        self.wd = WebDriverDoBeforeTest()
        self.wd.className ="studentSignin.Signin"
        self.wd.beforeClass()
        
        self.logger = LogObj()
        
        self.weblogin = web_login()
        self.weblogin.back_SigninPage() #返回到student 签到的页面
        
        self.webdriverpai = WebdriverApi(self.weblogin.driver)
        self.em = ExcelManager("UsersLogin.xls")
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.wd.afterClass()
        self.weblogin.driver.close()
 

    def test_student_singin(self):
        try:
            self.logger.info("SignIn.test_student_singin 测试用例已执行")
            driver = self.weblogin.driver
            api = self.webdriverpai
            tes_xls_data = self.em.readexcel("students")  #得到sheet页
            nrows = tes_xls_data.nrows
            print "------ excel中的测试用例条数是：",nrows-1    #excel中 的数据行数从1行开始
            for i in range(1,nrows):       #for循环式，默认从0--n-1
                print "------ 这是第：",i," 条用例"
                row_A = tes_xls_data.cell(i,0).value
                row_B = tes_xls_data.cell(i,1).value
                row_C = tes_xls_data.cell(i,2).value
                print row_A, row_B, row_C 
                
                clss = Select(driver.find_element_by_id("class_id")).options
                random.choice(clss).click()
                driver.implicitly_wait(2)
                
                lab = Select(driver.find_element_by_id("lab_id")).options
                random.choice(lab).click()
                driver.implicitly_wait(2)
                
                driver.find_element_by_id("name").clear()
                driver.find_element_by_id("name").send_keys(row_A)
                driver.implicitly_wait(2)
                
                driver.find_element_by_id("stuno").clear()
                driver.find_element_by_id("stuno").send_keys(row_B)
                driver.implicitly_wait(2)
                
                driver.find_element_by_id("info").clear()
                driver.find_element_by_id("info").send_keys(row_C)
                driver.implicitly_wait(2)
                
                driver.find_element_by_id("sign").click()
                
                b = driver.find_element_by_class_name("layui-layer-btn0").is_displayed()
                
                if b:
                    driver.find_element_by_class_name("layui-layer-btn0").click()
                
                self.weblogin.back_SigninPage() #返回到student 签到的页面
        except Exception,e:
                self.logger.error("SignIn.test_student_singin 测试用例出现异常"+str(e))
            
            
            


if __name__ == "__main__":
    unittest.main()