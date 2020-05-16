# coding=utf-8
import os,threading


{
  "deviceName": "127.0.0.1:62001",
  "platformName": "Android",
  "platformVersion": "5.1.1",
  "appPackage": "com.tencent.mobileqq",
  "appActivity": ".activity.SplashActivity",
  "noReset": "true"
}

def run(cmd):
    os.popen(cmd)
    print('appium已经停止')


res = os.popen('dir').read()
#netstat -aon | findstr  4723  ，查看端口被占用
#打印res有东西说明被占用，反之则没有
print(res)

cmd = 'node E:\\Appium\\resources\\app\\node_modules\\appium\\build\\lib\\main.js'
# 创建一个线程，args接收一个元祖，一个元祖用逗号隔开
th = threading.Thread(target=run,args=(cmd,))
#调用start会走run方法
th.start()
print('appium 正在运行')


