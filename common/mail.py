# coding:utf8
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from common import config, logger
from common.txt import Txt


class Mail:
    """
        powered by Mr Will
        at 2018-12-22
        用来获取配置并发送邮件
    """

    def __init__(self):
        self.mail_info = {}
        # 发件人
        self.mail_info['from'] = config.config['mail']
        #发件人账号
        self.mail_info['username'] = config.config['mail']
        # smtp服务器域名，截取配置文件邮箱，后面的服务器，拼上
        self.mail_info['hostname'] = 'smtp.' \
                                     + config.config['mail'][
                                       config.config['mail'].rfind('@')
                                       + 1:config.config['mail'].__len__()]
        # 发件人的密码
        self.mail_info['password'] = config.config['pwd']
        # 收件人
        self.mail_info['to'] = str(config.config['mailto']).split(',')
        # 抄送人
        self.mail_info['cc'] = str(config.config['mailcopy']).split(',')
        # 邮件标题
        self.mail_info['mail_subject'] = config.config['mailtitle']
        self.mail_info['mail_encoding'] = config.config['mail_encoding']
        # 附件内容，从配置文件读取 初始化
        self.mail_info['filepaths'] = []
        self.mail_info['filenames'] = []

    def send(self, text):
        # 这里使用SMTP_SSL就是默认使用465端口，如果发送失败，可以使用587，后面可以加个port参数port=587
        smtp = SMTP_SSL(self.mail_info['hostname'])
        #smtp = SMTP_SSL(self.mail_info['hostname'],port=587)
        smtp.set_debuglevel(0)

        ''' SMTP 'ehlo' command.
        Hostname to send for this command defaults to the FQDN of the local
        host.
        '''
        smtp.ehlo(self.mail_info['hostname'])
        smtp.login(self.mail_info['username'], self.mail_info['password'])

        # 普通HTML邮件
        # msg = MIMEText(text, 'html', self.mail_info['mail_encoding'])

        # 支持附件的邮件
        msg = MIMEMultipart()
        msg.attach(MIMEText(text, 'html', self.mail_info['mail_encoding']))
        msg['Subject'] = Header(self.mail_info['mail_subject'], self.mail_info['mail_encoding'])
        # msg['from'] = self.mail_info['from']
        h = Header(r'liulanglang', 'utf-8')
        h.append('<' + self.mail_info['from'] + '>', 'ascii')
        msg["from"] = h

        logger.debug(self.mail_info)
        logger.debug(text)
        msg['to'] = ','.join(self.mail_info['to'])
        receive = self.mail_info['to']

        # 抄送
        if self.mail_info['cc'] is None or self.mail_info['cc'][0].__len__() < 1:
            print('没有抄送')
        else:
            msg['cc'] = ','.join(self.mail_info['cc'])
            receive += self.mail_info['cc']

        # 添加附件
        for i in range(len(self.mail_info['filepaths'])):
            #这个是路径，读出来utf8
            att1 = MIMEText(open(self.mail_info['filepaths'][i], 'rb').read(), 'base64', 'utf-8')
            att1['Content-Type'] = 'application/octet-stream'
            # att1['Content-Disposition'] = 'attachment; filename= "'+self.mail_info['filenames'][i]+'"'
            #汉字乱码用gbk
            att1.add_header('Content-Disposition', 'attachment', filename=('gbk', '', self.mail_info['filenames'][i]))
            msg.attach(att1)

        try:
            smtp.sendmail(self.mail_info['from'], receive, msg.as_string())
            smtp.quit()
            logger.info('邮件发送成功')
        except Exception as e:
            logger.error('邮件发送失败：')
            logger.exception(e)


if __name__ == '__main__':
    #把配置文件的所有读出来，返回一个列表
    config.get_config('../conf/conf.properties')
    logger.debug(config.config)
    mail = Mail()
    #mail.mail_info['filepaths'] = ['D:\\PythonReport\\myframe\\test\\test.html']
    #mail.mail_info['filenames'] = ['test.html']
    #../conf/' + config.config['mailtxt'] (拼接htmlmodule)这里的是拼接的路径  把html报告读出来，也是txt一个对象
    htmlmodule = Txt('../conf/' + config.config['mailtxt'])
    print(htmlmodule)
    #读取   htmlmodule
    html = htmlmodule.read()[0]
    mail.send(html)
