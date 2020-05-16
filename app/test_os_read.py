import os
a=os.popen('ipconfig').read()
print(a)
b=os.popen('ipconfig')
print(b)