from inter.interkeys import HTTP
import inspect
from common.Excel import Reader, Writer


http = HTTP(Writer)
#在上两层目录
# 从http这个实例对象里面获取到addheader这个属性或者方法
# func就等价于http.addheader
func = getattr(http, 'addheader')
# 获取参数列表
s = inspect.getfullargspec(func).__str__()
print(s)
s = s[s.find('args=')+5:s.find(', varargs')]
print(s)
s = eval(s)
print(s)
s.remove('self')
print(s)

