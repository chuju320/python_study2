#-*-coding:utf-8-*-

import sys,time,re,collections

a = "collections.OrderedDict([])"
b = eval(a)
b['2']=2
print b
c = 'collections.%s'%b
d = eval(c)
print d.keys()
