# -*- coding:UTF-8 -*-

'''
Created on 2016年5月12日

@author: jayzhen
'''

from com.framework.util.FileCheckAndGetPath import FileChecK
from com.framework.util.ConfigCommonManager import Config

fc = FileChecK()
b = fc.is_has_file("email.ini")
if b:
    fp = fc.get_fileabspath()
    
    c = Config(fp)
    
    cc = c.get("emails", "receiver")
    
    print cc
    ee = cc.split(",")
    print type(ee)
    print type(cc)