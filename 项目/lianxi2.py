#-*-coding:utf-8-*-

import sys,time,re,collections,md5,hashlib

hashs = hashlib.md5()

hashs.update('admin')
b = hashs.hexdigest()
print b
hashss = hashlib.md5()
hashss.update('admin')
a =  hashss.hexdigest()
print a