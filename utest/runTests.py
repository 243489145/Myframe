# -*- coding: UTF-8 -*-
import unittest
from utest import datadriven
from parameterized import parameterized
from inter.interkeys import HTTP


# 创建一个测试类，继承unittest
#把runtest加载到rununittest，这里是一个testcase
class DataRunner(unittest.TestCase):
    """
    参数化：单元测试参数化的参数使用的二维列表
    """
#实例化类的对象
    obj = None

    @classmethod
    def setUpClass(cls) -> None:
        #走到这里的时候 调用了get_parmars()替换了type
        if datadriven.runtype == 'HTTP':
            cls.obj = HTTP(datadriven.writer)
    #把读取的Excel用例传进来
    @parameterized.expand(datadriven.alllist)
    #这里用例一行的内容
    def test_(self, index, name, keyword, param1, param2, param3):
        """

        :param index:   当前运行到哪一行，写入到哪一行
        :param name:
        :param keyword:
        :param param1:
        :param param2:
        :param param3:
        :return:
        """
        print(name)
        #把参数做成一个列表
        line = [keyword, param1, param2, param3]

        try:
            #6个参数，list[0]的时候是整数
            index = int(index)
            #记录当前要写入的行
            self.obj.row = index
            # 反射获取函数，self.obj类的对象，line是列表，取line[0]
            func = datadriven.geffunc(line, self.obj)
            # 获取函数参数个数
            lenargs = datadriven.getargs(func)
            # 执行关键字，这些函数里面调用了，写入方法，self.obj.row = index
            #res是返回值，True 和 Flase
            res = datadriven.run(func, lenargs, line)
            #加断言以后，报告才会出现false，在执行关键字的时候加return true和flash
            self.assertTrue(res)
        except:
            #切换sheet页，已经读取两行了，第一个列表
           # [['授权接口', '', '', '', '', '']   index='授权接口'
            datadriven.writer.set_sheet(index)


