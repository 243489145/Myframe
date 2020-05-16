# -*- coding: UTF-8 -*-
import unittest
from utest import testlib
from parameterized import parameterized

#测试testlib下面的testadd方法
# 创建一个测试类，继承unittest
class PramaTest(unittest.TestCase):
    """
    参数化：单元测试参数化的参数使用的二维列表
    parameterized.，没有这个库自己安装
    这里可以读取Excel
    """


    @parameterized.expand([
       #等价类的方法，80%的问题出现在极值
        ['整数相加', 1, 1, 2],
        ['小数相加', 1.1, 1.33333333, 2.43333333],
        ['整数加字符串', 1, '1', '11'],
        ['整数加小数', 1, 1.1, 2.1],
    ])
    # z参数比较是不是期望值
    def test_add(self, name, x, y, z):
        """

        :param name:    取名字区分用例
        :param x:
        :param y:
        :param z:
        :return:
        """
        print(name)
        self.assertEqual(testlib.add(x, y), z)

#main方法调用unittest运行方式，也可以编辑unittest的运行方式
#运行的时候在运行哪里，edit一个运行方式
if __name__ == '__main__':
    unittest.main()
