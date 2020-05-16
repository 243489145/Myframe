import time
import unittest

from BeautifulReport import BeautifulReport

from common import config, logger
from common.Encrypt import shutdown
from common.excelresult import Res
from common.mail import Mail
from common.mysql import Mysql
from common.txt import Txt
from utest import datadriven

#这个目录跟其他目录同级
if __name__ == '__main__':
    casename = 'HTTP-不加密'
    #datadriven有读取用例的方法和执行用例的方法
    #做web的在改一下
    datadriven.getparams('./lib/%s.xls' % casename,'./lib/result-%s.xls' % casename)
    #读出用例，取的全局变量
    print(datadriven.alllist)
    #开始调用unittest的方法，把runtest加载到rununittest
    test_suite = unittest.defaultTestLoader.discover('./utest', pattern='runTests.py')
    result = BeautifulReport(test_suite)
    #生成报告的路径
    result.report(filename='电商接口测试报告', description='电商接口测试报告')
    datadriven.writer.set_sheet(datadriven.alllist[0][0])
    endtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    datadriven.writer.write(1, 4, endtime)
    datadriven.writer.save_close()

    # 读配置文件
    config.get_config('./conf/conf.properties')
    logger.info(config.config)

    # 初始化数据库
    mysql = Mysql()
    mysql.init_mysql('./conf/userinfo.sql')

    # 结果统计
    res = Res()
    details = res.get_res('./lib/result-%s.xls' % casename)
    r = res.get_groups('./lib/result-%s.xls' % casename)

    # 关闭jvm
    shutdown()

    # 邮件处理
    mail = Mail()
    #拼接成cofn路径下的模板报告，mailtxt是配置正文标题名字
    htmlmodule = Txt('./conf/' + config.config['mailtxt'])
    html = htmlmodule.read()[0]
    # 对模块文本进行处理
    # 替换总体统计信息
    sumlist = ['status', 'passrate', 'starttime', 'endtime']
    for s in sumlist:
        html = html.replace(s, details[s])

    # 生成HTML的一行内容
    alltrs = ''
    for s in r:
        tr = '<tr><td width="100" height="28" align="center" bgcolor="#FFFFFF" style="border:1px solid #ccc;">分组信息</td><td width="80" height="28" align="center" bgcolor="#FFFFFF" style="border:1px solid #ccc;">用例总数</td><td width="80" align="center" bgcolor="#FFFFFF" style="border:1px solid #ccc;">通过数</td><td width="80" align="center" bgcolor="#FFFFFF" style="border:1px solid #ccc;">状态</td></tr>'
        tr = tr.replace('分组信息', str(s[0]))
        tr = tr.replace('用例总数', str(s[1]))
        tr = tr.replace('通过数', str(s[2]))
        tr = tr.replace('状态', str(s[3]))
        alltrs += tr
    #附件报告
    html = html.replace('mailbody', alltrs)
    mail.mail_info['filepaths'] = ['./电商接口测试报告.html','./lib/result-%s.xls' % casename]
    mail.mail_info['filenames'] = ['电商接口测试报告.html','result-%s.xls' % casename]
    mail.send(html)