import unittest
from BeautifulReport import BeautifulReport

if __name__ == '__main__':
    #测试UtestWtest  UI自动化脚本， 跑的是当前目录Pramatest.py脚本
    #test_suite = unittest.defaultTestLoader.discover('./', pattern='UtestWebTest.py')
    test_suite = unittest.defaultTestLoader.discover('./', pattern='Pramatest.py')
    result = BeautifulReport(test_suite)
    #还有一个参数log_path='report'  当前目录
    #在文件模板template 里面改title
    result.report(filename='电商项目测试报告', description='电商项目测试报告')