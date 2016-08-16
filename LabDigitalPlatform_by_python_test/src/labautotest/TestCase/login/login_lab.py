# -*- coding=utf-8 -*-
'''
自动化——登录网站
1.导入包，加载驱动，打开浏览器
2.输入网址，找到主页
3.锁定元素，传入参数，锁定元素的技术
4.提交数据，校验结果
'''
from com.framework.logging.Recoed_Logging import LogObj
from com.framework.webdriver.basecase.WebDriverBaseCase import WebDriverDoBeforeTest
from labautotest.data.data_read.ExcelData import ExcelManager
from labautotest.common.login.loginPage import web_login
import unittest

class Login(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.wd = WebDriverDoBeforeTest()
        self.wd.className ="login_lab.Login"
        self.wd.beforeClass()
        
        self.logger = LogObj()
        
        self.weblogin = web_login()
        self.weblogin.back_LoginPage(5)
        self.driver = self.weblogin.driver
        self.em = ExcelManager("UsersLogin.xls")
        
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.wd.afterClass()
        self.driver.close()
    
    def test_login_labPlatf(self):
        '''身份登录测试用例'''
        self.logger.info("Login.test_login_labPlatf测试用例已执行")
        tes_xls_data = self.em.readexcel("users")  #得到sheet页
        nrows = tes_xls_data.nrows
        print "------ excel中的测试用例条数是：",nrows-1    #excel中 的数据行数从1行开始
        for i in range(1,nrows):       #for循环式，默认从0--n-1
            print "------ 这是第：",i," 条用例"
            row_A = tes_xls_data.cell(i,0).value
            row_B = tes_xls_data.cell(i,1).value
            row_C = tes_xls_data.cell(i,2).value
            print row_A, row_B, row_C
            b = self.weblogin.userType_login(row_A, row_B, row_C)
            if b:
                title = self.driver.title
                print title
                if "实验室数字化平台" == title:               
                    print "------ 登录成功  ------"
                    self.em.writexcel(i, 3, "pass")
                    self.weblogin.back_LoginPage(5)
            else:
                print "------ 登录失败  ------"
                self.em.writexcel(i, 3, "failed")
                self.weblogin.back_LoginPage(5)
        print "------ 登录测试用例执行成功 ------"
    
if __name__ == "__main__":
    unittest.main()    


