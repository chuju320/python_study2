#-*-coding:utf-8-*-
'''map()函数接受两个参数，一个是函数，一个是序列，map将传入的函数作用到序列的每个元素，并把结果作为list
返回'''

def f(x):
    return x*x

list1 = map(f,[1,2,3,4,5,6,7,8,9])
print list1  #[1, 4, 9, 16, 25, 36, 49, 64, 81]

print map(str,[1,2,3,4,5,6,7])  #['1', '2', '3', '4', '5', '6', '7']

'''reduce把一个函数作用在一个序列上，这个函数必须接受两个函数，reduce吧结果继续与下一个元素做累积计算'''
def add(x,y):
    return x + y
print reduce(add,[1,2,3,4,5,6,7,8,9])  #45


def fn(x,y):
    return  x*10 + y
print reduce(fn,[1,2,3,4,5,6,7,8,9])  #123456789


def char2num(s):
    return {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}[s]

print reduce(fn,map(char2num,'123467'))  #123467

'''练习
1.利用map()函数，把用户输入的不规范的英文名字，变为首字母大写，其他小写的规范名字。
输入：['adam', 'LISA', 'barT']，输出：['Adam', 'Lisa', 'Bart']。

2.Python提供的sum()函数可以接受一个list并求和，请编写一个prod()函数，可以接受一个list并利用reduce()求积。
'''
#题目1
def bz():
    list2 = []
    while 1:
        name = raw_input('请输入您的英文名：')
        if name:
            list2.append(name)
        else:
            break
    print '你输入的英文名是：',list2
    print '标准英文名是：',[list2[i][0].upper()+list2[i][1:].lower() for i in range(len(list2))]

#bz()

#题目2
def prod(lists):
    print reduce(lambda x,y:x*y,map(int,lists))

prod(['1',23,4,'2'])   #184