# -*- coding:UTF-8 -*-

from labautotest.TestCase.login.login_lab import Login
from labautotest.TestCase.login.signin_lab_mysql import SignIn
from labautotest.TestCase.TesterPage.personal_center import PersonalCenter
from labautotest.TestCase.TesterLabAdmin.laboratory_management import LaboratoryManagement
from labautotest.TestCase.TeacherPage.apply_for_lab import ApplyLab
from labautotest.TestCase.WebAdminPage.class_management import Class_Management




'''
run_basic是可以管理要进行测试的TestCase
list_class中的参数最小级别必须是类名，不能是方法名，不然会报TypeError错误
这些类的实现一定是继承了unittest.TestCase，其中主要的方法名必须是以test开头
以unittest的套件标准编写测试用例
缺点是：每一次都要从新导入包，设置新的list_class
'''
lists_class = [
                Login,
                SignIn,
                PersonalCenter,
                LaboratoryManagement,
                ApplyLab,
                Class_Management
              ]