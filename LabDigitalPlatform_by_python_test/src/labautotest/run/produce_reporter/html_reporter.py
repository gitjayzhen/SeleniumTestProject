# -*- coding:UTF-8 -*-

import os
from com.framework.util.ConfigCommonManager import Config
from com.framework.util.FileCheckAndGetPath import FileChecK
from com.framework.util.DateTimeUtil import DateTimeManager
from com.framework.logging.Recoed_Logging import LogObj
'''
创建一个html文件，并返回文件的对象
'''
def html_reporter():
    logger = LogObj()
    fc = FileChecK()
    pro_path = fc.getProjectPath()
    boolean = fc.is_has_file("framework.ini")
    if boolean:
        inipath = fc.get_fileabspath()
        fw_conf = Config(inipath)
    htmlrp_path = fw_conf.get("htmlreportPath", "htmlreportPath")
    htmreportl_abs_path = os.path.join(pro_path,htmlrp_path)
    timecurrent = DateTimeManager().formatedTime("%Y-%m-%d-%H-%M-%S")
    logger.debug("=====创建了一个html文件报告,路径是：："+htmreportl_abs_path) 
    if not os.path.exists(htmreportl_abs_path):
        os.makedirs(htmreportl_abs_path)
    file_path = str(htmreportl_abs_path)+timecurrent+"-LDP-TestingRreporter.html"
    try:
        if os.path.exists(file_path):
            html_obj = open(file_path,"a") #打开文件   追加
            return html_obj
        else:
            html_obj = file(file_path,"wb+")
            return html_obj 
    except Exception,e:
        logger.error("创建html_reporter出现错误"+str(e)) 
       

    