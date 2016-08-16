# -*- coding:UTF-8 -*-
from com.framework.logging.Recoed_Logging import LogObj
from selenium import webdriver
from com.framework.util.DateTimeUtil import DateTimeManager
from com.framework.util.ConfigCommonManager import Config
from com.framework.util.FileCheckAndGetPath import FileChecK
from com.framework.webdriver.basecase.WebDriverBaseCase import WebDriverDoBeforeTest

import os,time,thread

from selenium.common import exceptions
from selenium.webdriver.common import action_chains
from selenium.webdriver.common import alert
from selenium.webdriver.common import by
from selenium.webdriver.common import keys
from selenium.webdriver.common import utils
from selenium.webdriver.remote import webelement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import wait
import random
'''
 * 封装整体思路：
 * 1、封装常用方法
 * 2、对于封装过的方法，失败的操作在operationCheck中进行截图
    '''
class WebdriverApi():

    def __init__(self,driver):
        fc = FileChecK()
        boolean= fc.is_has_file("framework.ini")
        if boolean:
            self.projectpath = fc.getProjectPath()
            self.fwInipath = fc.get_fileabspath()
        self.conf = Config(self.fwInipath)
        self.capturePath = os.path.join(self.projectpath,self.conf.get("capturePath", "capturePath"))
        self.pauseTime = self.conf.get("TimeSet", "pauseTime")
        self.logger = LogObj()
        self.driver = driver

    def pause(self,millisecond):
        try:
            time.sleep(millisecond)
        except Exception,e:
            self.logger.error("pause error:"+str(e))

    '''* 截取屏幕截图并保存到指定路径
     * @param filepath:保存屏幕截图完整文件名称及路径
     * @return 无    '''
    def captureScreenshot(self,filepath):
        try:
            self.driver.get_screenshot_as_file(filepath)
        except Exception ,e:
            self.logger.error("保存屏幕截图失败，失败信息："+e)
    '''
     * public method for handle assertions and screenshot.
     * @param isSucceed:if your operation success    '''
    def operationCheck(self,methodName,isSucceed) :
        if (isSucceed) :
            self.logger.info("method 【" + methodName + "】 运行通过！")
        else:
            dateTime = DateTimeManager.formatedTime("-%Y%m%d-%H%M%S%f")
            captureName = self.capturePath+methodName+dateTime+".png"
            self.captureScreenshot(captureName)
            self.logger.error("method 【" + methodName + "】 运行失败，请查看截图快照："+ captureName)
            
    '''
     * rewrite the get method, adding user defined log</BR>
     * 地址跳转方法，使用WebDriver原生get方法，加入失败重试的次数定义。
     * @param url: the url you want to open.
     * @param actionCount:retry: times when load timeout occuers.
    '''
    def get(self,url,actionCount):
        isSucceed = False 
        for i in range(actionCount):
            try:
                self.driver.get(url)
                self.__logger.debug("navigate to url [ " + url + " ]")
                break
            except Exception,e:
                self.__logger.error(e)
        self.operationCheck("get", isSucceed)
        
    '''
     * navigate back</BR> 地址跳转方法，与WebDriver原生navigate.back方法内容完全一致。
         '''
    def navigateBack(self):
        self.driver.back()
        self.logger.debug("navigate back")
    '''
     * navigate forward</BR> 地址跳转方法，与WebDriver原生navigate.forward方法内容完全一致。
    '''
    def navigateForward(self):
        self.driver.forward()
        self.logger.debug("navigate forward")
     
    '''
     * judge if the alert is present in specified seconds</BR>
     * 在指定的时间内判断弹出的对话框（Dialog）是否存在。
     * @param timeout:timeout in seconds
         '''
    def isAlertExists(self,timeout):
        isSucceed = False
        timeBegins = time.time()
        while(time.time() - timeBegins <= timeout * 1000):
            try:
                self.driver.switch_to_alert()
                isSucceed = True
                break
            except Exception,e:
                self.logger.error(e)
        self.operationCheck("isAlertExists", isSucceed)
        return isSucceed

    '''
     * rewrite the findElements method, adding user defined log</BR>
     * 按照指定的定位方式寻找象。
     * @param :the locator of the elements to be find
     * @param timeout:超时时间，单位：秒
     * @return the webelements you want to find    '''
    def findElements(self,by,value,timeout):  
        isSucceed = False 
        self.logger.debug("find elements [" + str(value) + "]") 
        elements =None 
        timeBegins = time.time()
        while(time.time() - timeBegins <= timeout):
            try:
                elements = self.driver.find_element(by, value) 
                isSucceed = True 
                self.logger.debug("find element [" + str(value) + "] success") 
                break 
            except Exception,e:  
                self.logger.error(e) 
        self.operationCheck("findElements", isSucceed) 
        return elements 
     
    '''
     * rewrite the getTitle method, adding user defined log</BR>
     * 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
     * @return the title on your current session    '''
    def getWindowTitle(self):  
        title = self.driver.title() 
        self.logger.debug("current window title is :" + title) 
        return title 
     
    '''
     * rewrite the getCurrentUrl method, adding user defined log</BR>
     * 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
     * @return the url on your current session    '''
    def getCurrentUrl(self):  
        url = self.driver.current_url() 
        self.logger.debug("current page url is :" + url) 
        return url 
     
    '''
     * rewrite the getWindowHandles method, adding user defined log</BR>
     * 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。'
     * @return the window handles set    '''
    def getWindowHandles(self):  
        handles = self.driver.window_handles() 
        self.logger.debug("window handles count are:" + len(handles)) 
        self.logger.debug("window handles are: " + handles) 
        return handles 
     
    '''
     * rewrite the getWindowHandle method, adding user defined log</BR>
     * 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
     * @return the window handle     '''
    def getWindowHandle(self):  
        handle = self.driver.current_window_handle()
        self.debug("current window handle is:" + handle) 
        return handle 
     
    '''
     * rewrite the getPageSource method, adding user defined log</BR>
     * 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
     * @return the page source     '''
    def getPageSource(self):  
        source = self.driver.page_source() 
        #logger.debug("get PageSource : [ " + source + " ]") 
        return source 
     
    '''
     * rewrite the getTagName method, find the element   and get its tag
     * name</BR> 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
     * @param 
     *            the locator you want to find the element
     * @return the tagname     '''
    def getTagName(self, by,value):  
        tagName = self.driver.find_element(by, value).tag_name() 
        self.logger.debug("element [ " + str(by) + " ]'s TagName is: "
                + tagName) 
        return tagName 
     
    '''
     * rewrite the getAttribute method, find the element   and get its
     * attribute value</BR> 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
     * @param :the locator you want to find the element
     * @param attributeName:the name of the attribute you want to get
     * @return the attribute value     '''
    def getAttribute(self,by,value, attributeName): 
        value = self.driver.find_element(by, value).get_attribute() 
        self.logger.debug("element [ " +str(by) + " ]'s " + attributeName
                + "is: " + value) 
        return value 
     
    '''
     * rewrite the clear method, adding user defined log</BR>
     * 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
     * @param element:the webelement you want to operate    '''
    def clear(self,element):  
        element.clear() 
        self.logger.debug("element [ " + element + " ] cleared") 
     
    '''
     * rewrite the click method, adding user defined log</BR>
     * 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
     * @param element:the webelement you want to operate    '''
    def click(self, by,value): 
        self.driver.implicitly_wait(2)
        element = self.findElements(by,value,3)
        element.click() 
        self.logger.debug("click on element [ " + str(element) + " ] ") 
     
    '''
     * rewrite the sendKeys method, adding user defined log</BR>
     * 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
     * @param element:the webelement you want to operate    '''
    def sendKeys(self,by,value, text):
        self.driver.implicitly_wait(2)
        element = self.driver.find_element(by, value)
        element.clear()
        element.send_keys(text) 
        self.logger.debug("input text [ " + text + " ] to element [ " + str(element)+ " ]") 
     

    '''
     * rewrite the isSelected method, the element to be find  </BR>
     * 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
     * @param :the locator you want to find the element
     * @return the bool value of whether is the WebElement selected    '''
    def isSelected(self,by,value):  
        isSelected = self.driver.find_element(by, value).is_selected()
        self.logger.debug("element [ " +value+ " ] selected? "+ str(isSelected)) 
        return isSelected 
    
    def isElementPresent(self,by,value,timeout):
        isSucceed = False
        self.logger.debug("find element [" + value + "]")
        timeBegins = time.time()
        while(time.time() - timeBegins <= timeout):
            try:
                self.driver.find_element(by,value)
                isSucceed = True
                self.logger.debug("find element [" + value+ "] success")
                break
            except Exception,e:
                self.logger.error(e)
            self.pause(self.pauseTime)
        self.operationCheck("isElementPresent", isSucceed)
        return isSucceed
    
    def webList_RandomSelectByOption(self,by,value,timeout):
        isSucceed = False
        timeBegins = time.time()
        while(time.time() - timeBegins <= timeout):
            try:
                webselect = self.driver.find_element(by, value)
                selectElement = Select(webselect)
                ooptions = selectElement.options
                ooption = random.choice(ooptions)
                itemValue = ooption.get_attribute("value")
                selectElement.select_by_value(itemValue)
                isSucceed = True
                self.logger.debug("item selected by item value [ " + itemValue+ " ] on [ " + str(by) + " ]")
                break
            except Exception,e:
                self.logger.error(e)
            self.pause(self.pauseTime)
        self.operationCheck("webList_RandomSelectByOption", isSucceed)

    def selectByValue(self,by,value,itemValue,timeout):
        isSucceed = False
        try:
            if (self.isElementPresent(by,value, timeout)):
                element = self.driver.find_element(by,value)
                select = Select(element)
                select.select_by_value(itemValue)
                self.logger.debug("item selected by item value [ " + itemValue+ " ] on [ " + value + " ]")
                isSucceed = True
        except Exception,e:
            self.logger.error(e)
        self.operationCheck("selectByValue", isSucceed)

    '''
     * rewrite the isEnabled method, the element to be find  </BR>
     * 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
     * @param ：the locator you want to find the element
     * @return the bool value of whether is the WebElement enabled    '''
    def isEnabled(self,by,value):
        isEnabled = self.driver.find_element(by, value).is_enabled()
        self.logger.debug("element [ " + str(by) + " ] enabled? "
                + (isEnabled)) 
        return isEnabled 
     
    '''  * rewrite the getText method, find the element   and get its own
     * text</BR> 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
     * @param :the locator you want to find the element
     * @return the text     '''
    def getText(self,by,value):  
        text = self.driver.find_element(by, value).text
        self.logger.debug("element [ " + value + " ]'s text is: " + text) 
        return text 
     

    '''  * rewrite the isDisplayed method, the element to be find  </BR>
     * 与工具原生API作用完全一致，只是增加了操作结果检查和日志记录。
     * @param :the locator you want to find the element
     * @return the bool value of whether is the WebElement displayed    '''
    def is_Displayed(self,by,value):
        isDisplayed = False
        try: 
            isDisplayed = self.driver.find_element(by, value).is_displayed()
            self.logger.debug("element [ " + str(by) + " ] displayed? "+ str(isDisplayed)) 
        except Exception,e:
            self.logger.error("element元素没有点位到"+str(e))
        return isDisplayed 
    
    '''  * Description: clear error handles does not actruely.</BR>
     * 清理掉实际上并不存在的窗口句柄缓存。
     * @param windowHandles:the window handles Set.    '''
    def clearHandleCache(self,windowHandles):
        errors = "new ArrayList<String>()"
        for handle in windowHandles :
            try:
                self.driver.switchTo().window(handle)
                self.driver.getTitle()
            except Exception ,e:
                errors.add(handle)
                self.logger.debug("window handle " + handle+ " does not exist acturely!")
        for i in range(len(errors)):
            windowHandles.remove(errors.get(i))
        return windowHandles

     
    '''
     * switch to window  handle</BR> 按照指定句柄选择窗口。
     * @param windowHandle:the handle of the window to be switched to    '''
    def  selectWindowHandle(self, windowHandle) : 
        isSucceed = False 
        try:  
            windowHandles = self.driver.window_handles()
            windowHandles = self.clearHandleCache(windowHandles) 
            for  handle in  windowHandles:  
                if (windowHandle.equals(handle)) : 
#                    driver.switchTo().window(handle) 
#                    selectDefaultFrame() 
                    isSucceed = True 
                    break 
        except Exception, e:  
            self.logger.error(e) 
         
#        operationCheck("selectWindowHandle", isSucceed) 
    
    def scrollbar_SlideTOBottom(self,element):
        #将页面滚动条拖到底部
        #js="var q=document.documentElement.scrollTop=10000"
        js="var q=document.getElementById('%s').scrollTop=10000" %element
        self.driver.execute_script(js)
        time.sleep(3) 
        self.logger.debug("将元素%s滑动到底部" %element)
     
    def accept_alert(self):
        try:
            self.driver.switch_to_alert().accept()
            self.logger.debug("切换到弹窗，并点击确定按钮")
        except Exception,e:
            self.logger.error("接受弹窗，出现异常："+str(e))
            
    '''
     * Description: switch to a window handle that exists now.</BR>
     * 切换到一个存在句柄（或者说当前还存在的）的窗口。    '''
    def  selectExistWindow(self):  
        windowHandles = self.driver.getWindowHandles() 
#        windowHandles = clearHandleCache(windowHandles) 
        exist_0 = windowHandles.toArray()[0].to() 
#        if (exist_0 is not null) : 
#            self.driver.switchTo().window(exist_0) 
#        else : 
#            self.logger.debug("no opened windows!") 
         
     
    '''
     * close window  window title and its index if has the same title, 
     *  full pattern</BR> 按照网页标题选择并且关闭窗口，重名窗口按照指定的重名的序号关闭
     * </BR>适用于有重名title的窗口，标题内容需要全部匹配。
     * @param windowTitle:the title of the window to be closed.
     * @param index:the index of the window which shared the same title, beginswith 1.    '''
    def  closeWindow(self, windowTitle, index):  
        isSucceed = False 
        try:  
            winList = []
            windowHandles = self.driver.getWindowHandles() 
            windowHandles = self.clearHandleCache(windowHandles) 
            for handle in windowHandles:  
                self.driver.switchTo().window(handle) 
                if (windowTitle.equals(self.driver.getTitle())):  
                    winList.add(handle) 
                 
             
            self.driver.switchTo().window(winList.get(index - 1)) 
            self.driver.close() 
            self.logger.debug("window [ " + windowTitle + " ] closed  index ["
                    + index + "]") 
            isSucceed = True 
        except Exception, e:  
            self.logger.error(e) 
         
#        operationCheck("closeWindow", isSucceed) 
     

    '''
     * close windows except specified window title,   full pattern</BR>
     * 关闭除了指定标题页面之外的所有窗口，适用于有重名title的窗口 </BR>按照指定的重名顺序关闭，标题内容需要全部匹配。
     * @param windowTitle:the title of the window not to be closed
     * @param index:the index of the window to keep shared the same title with
     *            others, begins with 1.    '''
    def closeWindowExcept( self,windowTitle, index):  
        isSucceed = False 
        try:  
            windowHandles = self.driver.getWindowHandles() 
            windowHandles = self.clearHandleCache(windowHandles) 
            for  handle in windowHandles:  
                self.driver.switchTo().window(handle) 
                title = self.driver.getTitle() 
                if (windowTitle.equals( not title)):  
                    self.driver.switchTo().defaultContent() 
                    self.driver.close() 
            winArray = self.driver.getWindowHandles().toArray() 
            winArray = self.driver.getWindowHandles().toArray() 
            for i in range( len(winArray)):  
                if (i + 1 != index):  
                    self.driver.switchTo().defaultContent() 
                    self.driver.close() 
            self.logger.debug("keep only window [ " + windowTitle
                    + " ]  title index [ " + index + " ]") 
            isSucceed = True 
        except Exception, e:  
            self.logger.error(e) 
        self.operationCheck("closeWindowExcept", isSucceed) 

    '''
     * close window  specified window hanlde,   full pattern</BR>
     * 关闭指定句柄的窗口。
     * @param windowHandle:the hanlde of the window to be closed.    '''
    def  closeWindowHandle(self, windowHandle):  
        isSucceed = False 
        try:  
            windowHandles = self.driver.getWindowHandles() 
            windowHandles = self.clearHandleCache(windowHandles) 
            for handle in windowHandles:  
                if (windowHandle.equals(handle)):  
                    self.driver.switchTo().window(handle) 
                    self.driver.close() 
                    break 
                 
             
            self.logger.debug("window [ " + windowHandle + " ] closed ") 
            isSucceed = True 
        except Exception, e:  
            self.logger.error(e) 
         
#        operationCheck("closeWindowHandle", isSucceed) 
     
    '''
     * close windows except specified window hanlde,   full pattern</BR>
     * 关闭除了指定句柄之外的所有窗口。
     * @param windowHandle: the hanlde of the window not to be closed.    '''
    def  closeWindowExceptHandle(self, windowHandle):  
        isSucceed = False 
        try:  
            windowHandles = self.driver.getWindowHandles() 
#            windowHandles = clearHandleCache(windowHandles) 
            for  handle in windowHandles:  
                if (windowHandle != handle):  
                    self.driver.switchTo().window(handle) 
                    self.driver.close() 
            self.logger.debug("all windows closed except handle [ " + windowHandle
                    + " ]") 
            isSucceed = True 
        except Exception, e:  
            self.logger.error(e) 
         
#        operationCheck("closeWindowExceptHandle", isSucceed) 

    '''
     * doubleclick on the element</BR> 在等到对象可见之后双击指定的对象.
     * @param :the locator you want to find the element
     * @param timeout:超时时间，单位：秒    '''
    def  doubleClick( self,by,timeout):  
        isSucceed = False 
        try:  
#            actionDriver.doubleClick(self.driver.findElement()) 
#            actionDriver.perform() 
            self.logger.debug("doubleClick on element [ " + str(by)+ " ] ") 
            isSucceed = True 
             
        except Exception, e:  
            self.logger.error(e) 
         
#        operationCheck("doubleClick", isSucceed) 
     
    '''
     * moveToElement</BR> 在等到对象可见之后移动到指定的对象.
     * @param :the locator you want to find the element
     * @param timeout:超时时间，单位：秒    '''
    def  moveToElement(self,by ,  timeout):  
        isSucceed = False 
        try:  
#            actionDriver.moveToElement(self.driver.findElement()) 
#            actionDriver.perform() 
            self.logger.debug("moveToElement [ " + str(by) + " ] ") 
            isSucceed = True 
             
        except Exception, e:  
            self.logger.error(e) 
         
#        operationCheck("moveToElement", isSucceed) 
     

    '''
     * right click on the element</BR> 在等到对象可见之后鼠标右键点击指定的对象。
     * @param 
     *            the locator you want to find the element
     * @param timeout
     *            超时时间，单位：秒    '''
    def  rightClick(self,by ,  timeout):  
        isSucceed = False 
        try:  
#            actionDriver.contextClick(self.driver.findElement()) 
#            actionDriver.perform() 
#            self.logger.debug("rightClick on element [ " + str(by) + " ] ") 
            isSucceed = True 
             
        except Exception, e:  
            self.logger.error(e) 
         
#        operationCheck("rightClick", isSucceed) 
     

    '''
     * rewrite the submit method, submit on the element to be find  </BR>
     * 在等到指定对象可见之后在该对象上做确认/提交的操作。
     * @param:the locator you want to find the element
     * @param timeout:超时时间，单位：秒    '''
    def  submitForm(self,by,value,timeout): 
        isSucceed = False 
        try:
            if (self.isElementPresent(by, timeout)):  
                self.driver.find_Element(by,value).submit() 
                self.logger.debug("submit on element [ " + str(by) + " ]") 
                isSucceed = True 
        except Exception, e:  
            self.logger.error(e) 
        self.operationCheck("submit", isSucceed) 
     
     

