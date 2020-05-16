import threading
import time
#https://blog.csdn.net/m0_38011218/article/details/81938261  多线程地址

def sing(num):
    for i in range(num):
        print("sing%d" % i)
        time.sleep(0.5)


def dance(num):
    for i in range(num):
        print("dancing%d" % i)
        time.sleep(0.5)


def main():
    """创建启动线程"""
    t_sing = threading.Thread(target=sing, args=(5,))
    t_dance = threading.Thread(target=dance, args=(6, ))
    t_sing.start()
    t_dance.start()


if __name__ == '__main__':
    main()


#继承thread的类
'''
    class MyThread(threading.Thread):
        def run(self):
            for i in range(3):
                time.sleep(1)
                msg = "I'm "+self.name+' @ '+str(i)
                print(msg)
    
    
    def test():
        for i in range(5):
            t = MyThread()
            t.start()
    
    
    if __name__ == '__main__':
        test()
'''


