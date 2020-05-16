# coding=utf-8
import os, time, traceback
import threading
from appium import webdriver
from common import logger



class App:
    """
    封装App自动化的常用操作
    安装node  命令启动appium，(main.js,nodejs启动)---main.js目录  执行node  ./main.js
    关闭杀掉node进程  tasklist 查找   taskkill杀掉
    """

    def __init__(self,writer):
        # 定义实例变量，存储浏览器，这个浏览器可以在整个
        # 类里面被调用
        self.driver = None
        self.txt = ''
        # 写入结果
        self.row = 0
        self.writer = writer
        # 关联的参数
        self.params = {}
        # app启动的参数字典
        self.conf = {}

    def appconf(self,conf):
        #打开服务器---连接服务器
        #传进一个json字符串，转化为字典
        """
        配置操作APP
        :param conf: appium客户端配置的json字符串
        :return:无
        """
        try:
            conf = conf.replace('\n','')
            self.conf = eval(conf)
            self.__write_excel_res('PASS', '配置成功')
            #连接模拟器
            os.popen('adb connect %s' % self.conf['deviceName'])
        except Exception as e:
            self.__write_excel_res('FAIL','配置格式错误\n' + str(traceback.format_exc()))
            logger.error('配置格式错误')
            logger.exception(e)

    def startappium(self,apppath):
        #打开appium（服务器）  node main,js路径打开appium
        #apppath main,js的绝对路径前半部分
        def run(cmd):
            #从下面调用，执行到read就会停止
            os.popen(cmd).read()
            #调用read函数后，进程会卡主（主线程的时候），但是appium还是运行状态，
            # 因为使用多线程 下面的代码正常执行，不在一个主线程内了（从上到下执行）
            #这里没走到，就是已经停止运行了
            logger.info('appium已经停止')
        #启动appium 的时候生成日子文件
        cmd = 'node ' + apppath + \
              '\\resources\\app\\node_modules\\appium\\build\\lib\\main.js -g %s >> null' \
                % './app/appium.log'
        res = os.popen('netstat -aon | findstr 4723').read().split()
        print(res)
        # if len(res)!=0:
        #     print(res[4])
        #     os.popen('taskkill /F /IM {}'.format(int(res[4])))

        if len(res)>0 and len(res[0]) > 1:
            self.__write_excel_res('FAIL', '端口被占用：\n' + str(res))
            logger.error('端口被占用：')
            logger.error(res)
            exit(-1)
        else:
            # 创建一个线程，去启动appium
            th = threading.Thread(target=run, args=(cmd,))
            th.start()  #这个方法会调用run方法，走完以后走下面的
            time.sleep(15)
            self.__write_excel_res('PASS', 'appium 正在运行')
            logger.info('appium 正在运行')

    def stopappium(self):
        #用node启动  杀死node进程，appium就会关掉
        os.popen('taskkill /F /IM node.exe').read()
        self.__write_excel_res('PASS', 'appium已经停止运行')

    def linkappium(self):
        """
        连接appium服务器
        :return: 无
        """
        # 连接appium服务器
        try:
            self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", self.conf)
            self.driver.implicitly_wait(10)
            self.__write_excel_res('PASS', 'appium连接成功')
        except Exception as e:
            self.__write_excel_res('FAIL', traceback.format_exc())
            logger.exception(e)
            exit(-1)


    def click(self, xpath):
        """
        点击元素
        :param xpath: 定位元素的xpath
        :return: 无
        """
        try:
            ele = self.__findele(xpath)
            ele.click()
            self.__write_excel_res('PASS', '点击元素成功')
        except Exception as e:
            self.__write_excel_res('FAIL', traceback.format_exc())
            logger.exception(e)

    def clear(self, xpath):
        """
        点击元素
        :param xpath: 定位元素的xpath
        :return: 无
        """
        try:
            ele = self.__findele(xpath)
            ele.clear()
            self.__write_excel_res('PASS', '清空输入框成功')
        except Exception as e:
            self.__write_excel_res('FAIL', traceback.format_exc())
            logger.exception(e)

    def input(self, xpath, value):
        """
        输入文本
        :param xpath: 定位元素的xpath
        :param value: 需要输入的文本
        :return: 无
        """
        try:
            ele = self.__findele(xpath)
            ele.send_keys(value)
            self.__write_excel_res('PASS', '元素输入文本成功')
        except Exception as e:
            self.__write_excel_res('FAIL', traceback.format_exc())
            logger.exception(e)

    def gettext(self, xpath,paramname):
        """
        获取元素的文本
        :param xpath: 定位元素的xpath
        :return: 元素的文本
        """
        try:
            ele = self.__findele(xpath)
            self.params[paramname] = ele.text
            self.__write_excel_res('PASS', '获取元素文本成功：' + self.params[paramname])
            return self.params[paramname]
        except Exception as e:
            self.params[paramname] = ''
            self.__write_excel_res('FAIL', traceback.format_exc())
            logger.exception(e)
            return None

    def __findele(self, xpath):
        """
        封装xpath找元素的方法
        :param xpath: 定位元素的xpath，id，accessibility_id
        :return: 找到的元素，如果没找到，就返回None
        #跟web xpath一样   有contains   statswith   endwith函数
        #app.driver.findElement(By.id("com.tencent.mobileqq:id/btn_login")).click();//点击登录按钮
        #app.click("//*[@resource-id=\"com.tencent.mobileqq:id/btn_login\"]");//点击用户名输入框
        """
        if xpath.__contains__(':id/') > 0:
            # 用id定位
            ele = self.driver.find_element_by_id(xpath)
        elif xpath.startswith('/'):
            ele = self.driver.find_element_by_xpath(xpath)
        else:
            ele = self.driver.find_element_by_accessibility_id(xpath)
        return ele

    def sleep(self, t=1):
        if t is None or t == '':
            t = 1
        else:
            t = int(t)

        time.sleep(t)
        self.__write_excel_res('PASS', '')

    def assertequals(self,paramname , exp_value, msg=''):
        """
        校验上一步获取的文本和期望值一样
        :param exp_value: 期望值
        :return: 是否一样
        """
        paramname = self.__get_relations(paramname)
        if (not paramname is None) and paramname == exp_value:
            print(msg + '校验成功')
            self.__write_excel_res('PASS', paramname)
            return True
        else:
            print(msg + '校验失败')
            self.__write_excel_res('FAIL', paramname)
            return False

    def quit(self):
        """
        退出当前打开的浏览器
        :return: 无
        """
        try:
            self.driver.quit()
            self.__write_excel_res('PASS', '')
        except Exception as e:
            self.__write_excel_res('FAIL', traceback.format_exc())
            logger.exception(e)


    def __write_excel_res(self,status,msg):
        # 写入excel
        self.writer.write(self.row,7,status)
        self.writer.write(self.row,8,str(msg))

    def __get_relations(self,params):
        """
        将参数里面用到关联的地方，替换为关联后的值
        :param params: 关联前的参数
        :return: 关联后的结果
        """
        if params is None or params == '':
            return ''
        else:
            # 遍历当前保存后的参数字典
            # 然后把参数里面凡是符合：{keys}这种
            # 形式的字符串，都替换为relations这个字典里面keys这个键的值
            for keys in self.params:
                params = params.replace('{' + keys + '}'
                                        ,self.params[keys])

        return params

