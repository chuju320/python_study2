#-*-coding:utf-8-*-
'''Python内建的filter()函数用于过滤序列。

和map()类似，filter()也接收一个函数和一个序列。和map()不同的时，filter()把传入的函数依次作用于每个元素，
然后根据返回值是True还是False决定保留还是丢弃该元素。'''
def is_pdd(n):
    return n % 2 == 1

print filter(is_pdd,[1,2,3,4,5,6,7,8,9])   #[1, 3, 5, 7, 9]

def not_empty(n):
    return n.strip()

print filter(not_empty,['1   ','  ','  21  21  '])  #['1   ', '  21  21  ']


'''练习

请尝试用filter()删除1~100的素数。'''

def susu(n):
        j = 2
        while j<n:
            if i % j ==0:
                break
            j += 1
        if j == n:
            return  n

print filter(susu,[i for i in range(1,101)])
