#coding:utf-8
import xml.dom.minidom as xmls
import time

def shop(username):
        '''购物'''
        fruit = {'苹果':5.52,'香蕉':3.20,'梨':2.81,'樱桃':4.32,'香瓜':3.52,'火龙果':5.52,'香橙':2.63}
        vagetables = {'萝卜':0.63,'芹菜':0.82,'韭菜':0.24,'南瓜':0.64,'土豆':0.35,'番茄':0.54,'黄瓜':0.61,'香菇':1.02}
        sock = {'薯片':8.5,'巧克力':25,'布丁':5,'罐头':8,'果冻':12,'麦片':10,'水果糖':18}
        tools = {'卫生纸':2,'毛巾':15,'垃圾袋':10,'洗发水':20,'拖布':15,'收纳盒':18}
        dress = {'西服':204,'T恤':85,'裙子':245,'短裤':152,'风衣':180,'羽绒服':208}
        shopList = {'水果':fruit,'蔬菜':vagetables,'零食':sock,'日用品':tools,'服装':dress}
        print '您好，欢迎来到购物中心，请选择要购买的物品！'
        lists = zip([i for i in range(len(shopList.keys()))],shopList.keys())
        print 'range(len(shopList.keys()))',range(len(shopList.keys()))
        print 'shopList.keys()',shopList.keys()
        print lists
        for i in range(len(lists)):
            print lists[i][0],'   ',lists[i][1]
        while 1:
                    num = raw_input('请输入序号进入相应的购物区：')
                    if num and ord(num)<=ord(str(len(shopList.keys()))):
                        print num
                        print lists[num]
                        print lists[num][1]
                        print shopList[lists[num][1]]#shopList[lists[num][1]]是对应的物品list
                    else:
                        print '您输入的序号不正确，请重新输入！'

shop('li')