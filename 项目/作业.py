#-*-coding:utf-8-*-
'''
网上银行
功能：
    1.额度15000
    2.可以提现，手续费5%
    3.每月最后一天出账单（每月30天），写入文件
    4.记录每月日常消费流水
    5.提供还款接口
    6.每月10号为还款日，过期未还，按欠款额的5%计息
'''
import time,sys,os,json,re,collections
import cPickle as p
import xml.dom.minidom as xmls
from xml.etree.ElementTree import Element,ElementTree
defaulten = sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding(defaulten)

class bankCount:
    #global nameUser
    #global moneyToPay
    def __init__(self):
        self.shopList = ''
        self.payMoney = 0
        self.nameUser = ''
        self.moneyToPay = ''
        self.no = ['查询','购物','还款','账单']
        self.countDict = collections.OrderedDict()#总购物清单
        self.nowDict = collections.OrderedDict()#临时清单
        self.times = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    def login(self,username,password):
        '''登录网上银行'''
        #print '--登录--'
        try:
            #print '如果可以获取username的 name 和 password属性值'
            name = self.xmlAttr(username,'name')
            paswd = self.xmlAttr(username,'password')
        except:
            #print '获取username的属性失败，需要注册'
            self.loginError()
        if name and password:
            #print 'name:',name
            #print 'paswd:',paswd
            #print 'username:',username
            #print 'password:',paswd
            if username == name and password==paswd:
                self.hello(username)
            else:
                self.loginError()

    def hello(self,username):
        '''登录进银行界面'''
        time.sleep(0.5)
        print '登陆成功！'
        self.nameUser = username
        time.sleep(0.5)
        print '欢迎来到世纪银行，很高兴为您服务！'
        print '请选择您的业务！'
        self.cmd(username)

    def cmd(self,username):
        message = zip(['1','2','3','4'],self.no)
        print '='*40
        print ' '*2,'-*-序 号-*-' + '    ' +'-*-业 务-*-'
        for i in range(len(message)):
            print ' '*7,message[i][0] + '            ' +message[i][1]
        print '='*40
        cmds = raw_input('请选择您的业务序号：').strip()

        if cmds:
            if ord(cmds)==49:
                print '+'*45
                print '|             个人信息查询中心！              |'
                print '+'*45
                time.sleep(1)
                self.chaXun(username)
            elif ord(cmds)==50:
                print '+'*45
                print '|             欢迎进入购物中心！              |'
                print '+'*45
                time.sleep(1)
                self.shop(username)
            elif ord(cmds)==51:
                print '+'*45
                print '|             欢迎进入充值中心！              |'
                print '+'*45
                time.sleep(1)
                self.huanKuan()
            elif ord(cmds)==52:
                print '+'*45
                print '|             账号收支记录中心！              |'
                print '+'*45
                time.sleep(1)
                self.detial()
            else:
                print '您输入的指令有误，请确认后重新输入！'
                time.sleep(0.5)
                self.cmd(username)
        else:
            print '您的序号输入有误，请重新输入！'
    def yon(self,username):
        '''每个指令的返回和重新执行动作'''
        while 1:
            print '下一步操作：\n  1  返回主菜单\n  2  退出系统'
            num = raw_input('请输入指令：').strip()
            if num:
                if ord(num)==49:
                    self.cmd(username)
                    break
                elif ord(num)==50:
                    self.close()
                else:
                    print '您输入的指令有误，请确认后输入！'
                    time.sleep(0.5)
            else:
                print '您的指令有误，请重新输入！'
                time.sleep(0.5)

    def chaXun(self,username):
        '''查询余额'''
        print '以下为您的最新余额信息：'
        print '~'*80
        counts = self.xmlAttr(username,'count')
        times = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        #print 'counts:',counts
        comment = u'%s%s%s%s'% (u'截止',str(times),u'，您的账户余额是：' ,str(counts))
        for i in comment:
            print i,
            time.sleep(0.1)
        print
        print '~'*80
        time.sleep(2)
        self.yon(username)
    def shop(self,username):
        '''购物'''
        fruit = {'苹果':5.52,'香蕉':3.20,'梨':2.81,'樱桃':4.32,'香瓜':3.52,'火龙果':5.52,'香橙':2.63}
        vagetables = {'萝卜':0.63,'芹菜':0.82,'韭菜':0.24,'南瓜':0.64,'土豆':0.35,'番茄':0.54,'黄瓜':0.61,'香菇':1.02}
        sock = {'薯片':8.5,'巧克力':25,'布丁':5,'罐头':8,'果冻':12,'麦片':10,'水果糖':18}
        tools = {'卫生纸':2,'毛巾':15,'垃圾袋':10,'洗发水':20,'拖布':15,'收纳盒':18}
        dress = {'西服':204,'T恤':85,'裙子':245,'短裤':152,'风衣':180,'羽绒服':208}
        shopList = {'水果':fruit,'蔬菜':vagetables,'零食':sock,'日用品':tools,'服装':dress}
        print '您好，欢迎来到购物中心，请选择要购买的物品！'
        lists = zip([i for i in range(len(shopList.keys()))],shopList.keys())

        while 1:
            print '*'*40
            print ' '*6,'< 序 号 >','   ','< 类 别 >'
            for i in range(len(lists)):
                print ' '*9,lists[i][0],' '*10,lists[i][1]
            print '*'*40
            num = raw_input('请输入序号进入相应的购物区：').strip()
            if num and ord(num)<ord(str(len(shopList.keys()))):
                num = int(num)
                #print 'shopList[lists[num][1]]:',shopList[lists[num][1]]
                self.shopping(lists[num][1],shopList[lists[num][1]])#shopList[lists[num][1]]是对应的物品list
            else:
                print '您输入的序号不正确，请重新输入！'
                time.sleep(0.5)

    def shopping(self,name,nameList):
        '''购物区，根据不同的商品列表返回相应的内容'''
        #name:选择的商品区域
        #nameList:选择的商品列表
        print '欢迎来到%s购物区，请浏览商品列表，并输入你需要购物的物品序号！'%name

        while 1:
            n_v_list = zip([i for i in range(len(nameList))],nameList.keys(),nameList.values())
            print '-'*80
            print ' '*6,'序号',' '*4,'价格',' '*4,'名称'
            for i in range(len(n_v_list)):
                n = 0
                a =  n_v_list[i][0],' '*2,n_v_list[i][1],' '*2,n_v_list[i][2]
                for j in a:
                    n += len(str(j))
                print '       %-9s￥%-9s%-10s'%(a[0],a[4],a[2])
                #print ' '*6,a[0],' '*6,a[2],' '*4,a[4]
            print '-'*80
            num = raw_input('请输入商品序号：').strip()  #n_v_list[num][1] 是商品的名字，也是nameList的key
            if num.isdigit() and int(num)<len(nameList.keys()):
                a = 1
                num = int(num)
                while a ==1:
                    num2 = raw_input('请输入你需要多少数量/斤：').strip()
                    if num2 and num2.isdigit():
                        keyName = n_v_list[num][1]
                        print '您好，您本次购物:\n        名称：%s    数量：%s'%(keyName,num2)
                        times = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
                        #print 'keyName:',keyName
                        #print 'num2:',num2
                        dicts = collections.OrderedDict()
                        dicts[keyName]=num2
                        self.countDict[times]=dicts
                        self.nowDict[times]=dicts
                        #print 'self.countDict:',self.countDict
                        self.jiSuan(self.nowDict,nameList)
                        while 1:
                            cmd = raw_input('您是否需要继续购物：\n  1:是\n  2:否\n输入指令：').strip()
                            if cmd:
                                if ord(cmd)==49:
                                    return

                                elif ord(cmd)==50:
                                    print '进入结算系统！'
                                    self.pay()
                                    return
                                else:
                                    print '您的操作有误，请重新输入！'
                                    time.sleep(0.5)
                            else:
                                print '请输入有效指令！'
                                time.sleep(0.5)
                                break
                    else:
                        print '您好，请输入正确的数字！'
                        time.sleep(0.5)
            else:
                print '您好，您输入的商品号不存在，请重新输入！'
                time.sleep(0.5)

    def pay(self):
        '''结算支付系统'''
        #shopList:购物清单
        #payMoney：支付金额
        print '欢迎进入支付系统！您的购物清单如下：'
        print self.shopList
        print '您总共需要支付￥%s的费用！'%self.payMoney
        self.moneyToPay = self.payMoney
        print '结算中',
        for i in '.'*5:
            print i,
            time.sleep(0.5)
        print
        self.total(self.payMoney,False)
    def jiSuan(self,items,nameList):
        '''数据处理中心'''
        #items={ 时间 ：{ 物品 ： 数量 } }
        #keyName:商品名，用来从商品列表中获取价格
        #nameList:商品列表
        print
        print '您目前的购物车信息如下：'
        keysList = items.keys()
        keysList2 = self.countDict.keys()
       # print 'items:',items
       # print 'keysList:',keysList
        for i in keysList2:
            name2 = self.countDict[i].keys()[0]
            num2 = self.countDict[i].values()[0]
            print '        %s 数量: %s'%(name2,num2)
        print
        for i in keysList:
            #print 'items[i].keys()',items[i].keys()
            shopName = items[i].keys()[0]
            shopNums = items[i].values()[0]
            #print 'nameList:',nameList
            #print 'shopName:',shopName
            values = nameList[shopName]
            a =  i +'   '+shopName+' 数量 '+shopNums+'\n'
            self.shopList += a
            self.payMoney += int(shopNums)*int(values)
            self.nowDict = collections.OrderedDict()
            return
    def total(self,menoy,how=True):
        '''改动余额，如果how为True，则充值；如果how为False，则扣款，不足时提示；均返回最后余额'''
        #menoy:改动的金额
        #how:True则充值，False则扣款
        #print 'self.nameUser:',self.nameUser
        nameusers = self.nameUser
        count = self.xmlAttr(nameusers,'count')
        if how:
            self.changeXml(nameusers,'count',(int(count)+int(menoy)))
            time.sleep(1)
            self.write('充值金额：%s'%int(menoy))
            print '充值成功！'
            time.sleep(1)
            print '您目前的余额是%s'%(int(count)+int(menoy))
            self.yon(nameusers)
        else:
            if int(count) > int(menoy):
                self.changeXml(self.nameUser,'count',(int(count)-int(menoy)))
                print '支付成功，您目前的余额是%s'%(int(count)-int(menoy))
                detials = ''
               # print 'self.countDict:',self.countDict
                for i in self.countDict.keys():
                    #print 'self.countDict[i][0]:',self.countDict[i].keys()[0]
                    #print 'self.countDict[i][1]:',self.countDict[i].values()[0]
                    detials += ' %s*%s '%(self.countDict[i].keys()[0],self.countDict[i].values()[0])
               # print 'detials:',detials

                self.write('支付 %s，总共%s元'%(detials,menoy))
                self.countDict = collections.OrderedDict()
                self.shopList = ''
                self.payMoney = 0
                self.yon(self.nameUser)
            else:
                print '抱歉，您的余额不足，你需要支付的金额是%s，您的账户余额是%s'%(menoy,count)
                while 1:
                    cmd = raw_input('请问您需要去充值页面吗？选择1进入充值页面，选择2停留在当前页面：').strip()
                    if cmd:
                        if ord(cmd) == 49:
                            self.moreMoney()
                            n =1
                            while n == 1:
                                cmd = raw_input('您是否需要继续支付？\n   按1继续支付\n   按2退出支付\n选择：').strip()
                                if cmd and cmd.isdigit():
                                    if ord(cmd)==49:
                                        n =2
                                        self.total(self.moneyToPay,False)
                                    elif ord(cmd) == 50:
                                        n =2
                                        self.yon(self.nameUser)
                                    else:
                                        print '你的输入指令有误，请重新输入！'
                                        time.sleep(0.5)
                                else:
                                    print '您好，您输入的指令无效！'
                                    time.sleep(0.5)
                        elif ord(cmd)==50:
                            self.yon(self.nameUser)
                        else:
                            print '您的输入有误，请重新选择！'
                            time.sleep(0.5)
                    else:
                        print '请输入指令！'
                        time.sleep(0.5)
                        break
    def write(self,detials,files='data.xml'):
        '''记录交易'''
        detial1 = self.xmlAttr2(self.nameUser,'countDetial')
        times = time.strftime("%y-%m-%d %H:%M:%S",time.localtime())
        detial1[times] = detials
        self.changeXml(self.nameUser,'countDetial',detial1)


    def moreMenoy(self):
        '''存款充值页面'''
        money = raw_input('请输入您要充值的金额（一次最多10000元，总金额上限100000元）：').strip()
        if money and money.isdigit():
            if int(money) <= 10000:
                now = self.xmlAttr(self.nameUser,'count')
                now2 = int(now)+int(money)
                if int(now2) <= 100000:
                    self.changeXml(self.nameUser,'count',now2)
                    print '充值成功，您目前的余额是：%s元'%now2
                    self.write('充值%s元'%now2)
                    return
                else:
                    print '对不起，您（穷）的（逼）余（你）额（有）已（这）超（多）上（钱）限（么）！'
                    time.sleep(1)
                    self.moreMenoy()
            else:
                print '您好，单次充值金额不能大于10000，请重新输入金额！'
                time.sleep(1)
                self.moreMenoy()
        else:
            print '对不起，您输入的金额无效，如果有钱就请输入合理的数字，如果没钱就请滚粗！'
            time.sleep(1)
            self.moreMenoy()

    def huanKuan(self):
        '''存款系统'''
        print
        print '~'*50
        money = raw_input('请输入您要充值的金额:').strip()
        print '~'*50
        print
        if money and money.isdigit():
            self.total(money)
            return
        else:
            print '请输入合法的金额！'
            self.huanKuan()
        self.yon(self.nameUser)
    def detial(self):
        '''账号消费充值记录'''
        print '以下为您的最新交易信息：\n'
        print '~'*100
        detials =  self.xmlAttr2(self.nameUser,'countDetial')
        for i in  detials.keys():
            print i, ' ',detials[i]
        print '~'*100
        print
        self.yon(self.nameUser)
    def loginError(self):
        '''登录失败'''
        #print '--登录失败--'
        print '登录失败!'
        while 1:
            order = raw_input('您好，你的账号或密码错误，\n    选择1可重新输入\n    选择2可进行注册\n请选择:').strip()
            if order and len(order)==1 and order.isdigit():
                if ord(order) == 49:
                    print '--重新输入--'
                    self.start()
                    return
                elif ord(order) == 50:
                    print '--注册--'
                    self.regist()
                    return
                else:
                    print '您好，您的指令输入有误，请确认后输入！'
                    time.sleep(0.5)
            else:
                print '您好，您的指令输入有误，请确认后输入！'
                time.sleep(0.5)

    def start(self):
        '''程序开始'''
        #print '--开始--'
        cmds = raw_input('    登录请按1\n    注册请按2\n指令：').strip()
        if cmds and cmds.isdigit():
            if ord(cmds)==49:
                #print '--输入账户--'
                username = raw_input(u'请输入您的账户：').strip()
                if username:
                    while 1:
                        #print '--输入密码--'
                        password = raw_input(u'请输入您的6位数字密码：').strip()
                        if password and password.isdigit() and len(password)==6:
                            if os.path.exists('data.xml'):
                                #print '如果存在data.xml'
                                self.login(username,password)
                                return
                            else:
                                #print '如果不存在data.xml'
                                self.files()
                                #print 'data.xml文件创建完毕，进行登录'
                                self.login(username,password)
                                return
                        else:
                            print '您的密码无效，请重新输入，有效密码为6位数字！'
                            time.sleep(0.5)
                else:
                    self.start()
            elif ord(cmds)==50:
                self.regist()
                self.start()
            else:
                print '您输入的指令有误！'
                time.sleep(0.5)
                self.start()
        else:
            print '您输入的指令有误！'
            time.sleep(0.5)
            self.start()
    def files(self,files='data.xml'):
        '''创建xml'''
        impl = xmls.getDOMImplementation()
        dom = impl.createDocument(None,'eBank',None)
        ele = dom.createElement('countDetial')
        root = dom.documentElement
        root.appendChild(ele)
        f = open(files,'w')
        dom.writexml(f,addindent='  ',newl='\n')
        f.close()
        #print 'data.xml文件创建完毕，进行登录'
        return
    def regist(self):
        '''注册'''
        if os.path.exists('data.xml'):
            #print '如果存在data.xml'
            userName = raw_input('请输入您的账户名，以字母开头：').strip()
            if not self.xmlTag(userName):
                while userName[0].isalpha():
                    password = raw_input('请输入6位数字密码:').strip()
                    if len(password)==6 and password.isdigit():
                        self.writeXml(userName,'name',userName)
                        self.changeXml(userName,'password',password)
                        self.changeXml(userName,'count','15000')
                        self.changeXml(userName,'countDetial',"collections.OrderedDict([])")
                        print '注册完成，自动进行登录'
                        self.login(userName,password)
                        break
                    else:
                        print '请输入6位数字密码！'
                        time.sleep(0.5)
                else:
                    print '您输入的账号格式有误，请重新输入！'
                    time.sleep(0.5)
                    self.regist()
            else:
                print '你输入的账号已存在，请直接登录或重新输入！'
                time.sleep(0.5)
                while 1:
                    num = raw_input('1  登录\n2  重新注册').strip()
                    if num and num.isdigit():
                        if ord(num)==49:
                            self.start()
                            break
                        elif ord(num)==50:
                            self.regist()
                            break
                        else:
                            print '您输入的指令有误，请重新输入！'
                            time.sleep(0.5)
                    else:
                        print '您输入的指令有误，请重新输入！'
                        time.sleep(0.5)
        else:
            #print '如果不存在data.xml'
            self.files()
            self.regist()
    def changeXml(self,tagName,Name,values,files='data.xml'):
        '''修改xml属性'''
        #tagName:标签名
        #Name:属性名
        #values:属性值
        tree = ElementTree() #打开文件
        tree.parse(files)
        notes = tree.findall('countDetial/%s'%tagName) #获取符合条件的所有节点
        if len(notes) != 0:
            if type(values) is not str and type(values) is not int:
                notes[0].set(Name,'collections.%s'%values)
            else:
                notes[0].set(Name,'%s'%values)
        tree.write('data.xml', encoding="utf-8",xml_declaration=True)
    def writeXml(self,tagName,Name,values,files='data.xml'):
        '''写入xml'''
        #tagName:标签名
        #Name:属性名
        #values:属性值
        tree = ElementTree()
        tree.parse(files) #打开文件
        first = tree.find('countDetial')
        #print 'first',first
        notes = tree.findall('countDetial/%s'%tagName) #获取符合条件的所有节点
        #print 'notes',notes
        if len(notes) != 0:
            if type(values) is not str and type(values) is not int:
                notes[0].set(Name,'collections.%s'%values)
            else:
                notes[0].set(Name,'%s'%values)
        else:
            if type(values) is not str and type(values) is not int:
                note = Element(tagName,{'%s'%Name:'collections.%s'%values})
            else:
                note = Element(tagName,{'%s'%Name:'%s'%values})
            first.append(note)
        tree.write('data.xml', encoding="utf-8",xml_declaration=True)
    def xmldata(self,tagName,files='data.xml'):
        '''从XML文件中查找对应的text数据'''
        dom = xmls.parse(files)
        data = dom.getElementsByTagName(tagName)
        name = data[0].firstChild.data
        return name

    def xmlAttr(self,tagName,attr,files='data.xml'):
        '''获取xml文件中的属性值'''
        #tagName:标签名
        #attr:属性名
        #print '--获取%s的%s属性--'%(tagName,attr)
        dom = xmls.parse(files)
        data = dom.getElementsByTagName(tagName)
        value = data[0].getAttribute(attr)
        #print '获取到的属性值',value
        return value

    def xmlAttr2(self,tagName,attr,files='data.xml'):
        '''获取xml文件中的属性值'''
        #tagName:标签名
        #attr:属性名
        #print '--获取%s的%s属性--'%(tagName,attr)
        dom = xmls.parse(files)
        data = dom.getElementsByTagName(tagName)
        value = data[0].getAttribute(attr)
        #print '获取到的属性值',value
        return eval(value)

    def xmlTag(self,userName,files='data.xml'):
        '''从xml中获取标签'''
        #userName:标签名，也是用户名
        dom = xmls.parse(files)
        data = dom.getElementsByTagName(userName)
        return data
    def close(self):
        '''系统退出'''
        self.countDict = collections.OrderedDict()
        self.shopList = ''
        self.payMoney = 0
        print '欢迎下次光临，再见！'
        time.sleep(2)
        sys.exit()
a = bankCount()
a.start()