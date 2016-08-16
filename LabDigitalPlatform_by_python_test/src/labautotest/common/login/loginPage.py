#coding:utf-8

from com.framework.logging.Recoed_Logging import LogObj
from com.framework.util.ConfigCommonManager import Config
from com.framework.util.FileCheckAndGetPath import FileChecK
from com.framework.webdriver.basecase.WebDriverBaseCase import WebDriverDoBeforeTest
from com.framework.webdriver.baseapi.WebdriverBaseApi import WebdriverApi
from labautotest.common.runwhichbroswer.RunBrowserBeforeTestCase import RunBrowser
import time
from selenium.webdriver.common import by

class web_login():

    def __init__(self):
        fc = FileChecK()
        boolean = fc.is_has_file("framework.ini")
        if boolean:
            rwb_ini_path = fc.get_fileabspath()
        conf = Config(rwb_ini_path)
        baseURL = conf.get("baseURL", "baseURL")
        self.driver = RunBrowser(baseURL)
        
        self.driverapi = WebdriverApi(self.driver)
        self.logger = LogObj()
        self.basecase= WebDriverDoBeforeTest()
        self.basecase.driver = self.driver

    '''
    1.登录身份类型设置后，通过两次的定位，如果有定位到错误弹框的元素，及登录的账号密码有问题
    '''    
    def userType_login(self,user,passwd,typeNum):
        isSucceed = False
        self.driver.implicitly_wait(3)
        try:
            self.driver.find_element_by_xpath("//input[@name='sf' and @value='%s']" %typeNum).click()
            self.driver.find_element_by_id("input_username").clear()
            self.driver.find_element_by_id("input_username").send_keys(user)
            self.driver.find_element_by_id("input_password").clear()
            self.driver.find_element_by_id("input_password").send_keys(passwd)
            self.driver.find_element(by.By.ID, "login_btn").click()
            self.driver.implicitly_wait(3)
            try:
                errorbtn = self.driver.find_element_by_class_name("layui-layer-btn0")
                boolean = errorbtn.is_displayed()
                if boolean:
                    errotcontent = self.driver.find_element_by_class_name("layui-layer-content").text
                    self.basecase.capture(errotcontent)
                    self.logger.debug(errotcontent)
                    isSucceed = True
                    errorbtn.click()
            except Exception,e:
                self.logger.debug("未定位到layui-layer-btn0元素，证明登陆的账号密码没有问题")
                
            try:
                webelenment = self.driver.find_element_by_xpath("//a[@href='logout']").is_displayed()
                if webelenment:
                    isSucceed = True
                    self.logger.debug("定位到logout元素，证明实验员成功登录该平台")
            except Exception,e:
                self.logger.debug("未定位到logout元素，证明没有登录成功")
        except Exception,e:
            self.basecase.capture("admin_login")
            self.logger.error(">>>登录员身份登录界面出现异常"+str(e))
        self.basecase.operationCheck("administrator_login", isSucceed)
        return isSucceed

    '''
    1.管理身份进行登录，identity（身份：实验员，实验室管理员，教师，网站管理员）
    2.通过字符串比较后，选中radio
    3.输入账号密码，点击登陆
    '''        
    def administrator_login(self,identity,user,passwd):
        isSucceed = False
        self.driver.implicitly_wait(5)
        try:
            if ("实验员 ".strip()) == identity.strip():
                self.driver.find_element_by_xpath("//input[@name='sf' and @value='1']").click()
                self.driver.find_element_by_id("input_username").clear()
                self.driver.find_element_by_id("input_username").send_keys(user)
                self.driver.find_element_by_id("input_password").clear()
                self.driver.find_element_by_id("input_password").send_keys(passwd)
                self.driver.find_element(by.By.ID, "login_btn").click()
                #login_form
                isSucceed = True
                self.logger.debug("实验员登录该平台")
                
            elif ("实验室管理员".strip()) == identity.strip():
                self.driver.find_element_by_xpath("//input[@name='sf' and @value='2']").click()
                self.driver.find_element_by_id("input_username").clear()
                self.driver.find_element_by_id("input_username").send_keys(user)
                self.driver.find_element_by_id("input_password").clear()
                self.driver.find_element_by_id("input_password").send_keys(passwd)
                self.driver.find_element(by.By.ID, "login_btn").click()
                isSucceed = True
                self.logger.debug("实验室管理员登录该平台")
            elif ("任课教师 ".strip()) == identity.strip():
                self.driver.find_element_by_xpath("//input[@name='sf' and @value='3']").click()
                self.driver.find_element_by_id("input_username").clear()
                self.driver.find_element_by_id("input_username").send_keys(user)
                self.driver.find_element_by_id("input_password").clear()
                self.driver.find_element_by_id("input_password").send_keys(passwd)
                self.driver.find_element(by.By.ID, "login_btn").click()
                isSucceed = True
                self.logger.debug("任课教师登录该平台")
            elif ("网站管理员 ".strip()) == identity.strip():
                self.driver.find_element_by_xpath("//input[@name='sf' and @value='4']").click()
                self.driver.find_element_by_id("input_username").clear()
                self.driver.find_element_by_id("input_username").send_keys(user)
                self.driver.find_element_by_id("input_password").clear()
                self.driver.find_element_by_id("input_password").send_keys(passwd)
                self.driver.find_element_by_id("login_btn").click()
                isSucceed = True
                self.logger.debug("网站管理员登录该平台")
            self.basecase.operationCheck("administrator_login", isSucceed)
        except Exception,e:
            self.basecase.capture("administrator_login")
            self.logger.error("登录员身份登录界面出现异常"+str(e))
        return isSucceed
    '''
    1.不管当前是在哪个页面，只要是回到签到页面，就通过修改url来实现
    '''
    def back_SigninPage(self):
        title = self.driver.title
        currenturl = self.driver.current_url
        urls = currenturl.split("/")
        new_url = urls[0]+"//"+urls[2]+"/"+urls[3]+"/stusign"
        self.driver.get(new_url)
        self.logger.debug("%s界面返回到开放实验室进入签到入口界面"%title)
        
    def back_LoginPage(self,timeout):
        title = self.driver.title
        timeBegins = time.time()
        print title
        if "实验室数字化平台" == title:
            self.driver.find_element_by_xpath("//a[@href='logout']").click()
            while(time.time() - timeBegins <= timeout):
                try:
                    self.driver.find_element_by_xpath("//a[@href='login']").click()
                    break
                except Exception,e:
                    self.logger.error(e)
        else:
            currenturl = self.driver.current_url
            urls = currenturl.split("/")
            new_url = urls[0]+"//"+urls[2]+"/"+urls[3]+"/login"
            self.driver.get(new_url)
        self.logger.debug("%s界面>返回>管理身份登陆界面"%title)
            
'''        
wl = web_login("http://192.168.38.129:8080/LabDigitalPlatform_linux/login")
wl.administrator_login("网站管理员 ", "admin", "123456")  
#a = wl.driver.find_element_by_class_name("layui-layer-btn0").click()
     
wl.back_SigninPage()
time.sleep(3)        
wl.driver.close()'''