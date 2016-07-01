#-*-coding:utf-8-*-
'''random.choice(seq)
    choice() 方法返回一个列表，元组或字符串的随机项
    seq -- 可以是一个列表，元组或字符串。
'''
import random

for i in range(5):
    print random.choice([i for i in range(1,250) if i != 156])
