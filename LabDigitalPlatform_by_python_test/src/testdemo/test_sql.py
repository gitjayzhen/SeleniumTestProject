# -*- coding=utf-8 -*-
'''
Created on 2016年5月4日

@author: jayzhen
'''

from com.framework.databases.sqlcontrol import Execute_SQL

ss = Execute_SQL()
#sql = "select username,password from users;"
#res = ss.execute_select(sql)
#for r in res:
#    print r[0].decode("utf8").encode("gbk")
       
#sql = "insert into yp_files (name,uid,url,code) values ('selenium2',31,'www.nn.com','uuse');"      
#b = ss.execute_addone(sql)         
#print b       
  
#sql = "update yp_files set name='python' where name='selenium2'"     
#print ss.execue_update(sql)
sql = "delete from yp_files where name='python'"     
print ss.execue_update(sql)
       
        
ss.execute_conn_close()