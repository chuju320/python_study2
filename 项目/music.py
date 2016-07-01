#-*-coding:utf-8-*-
from Tkinter import *
import tkMessageBox
import urllib
import json,time,thread
import mp3play

musiclist = []
def music():
    #没有输入时提示
    listBox.delete(0,END)
    if entry.get() == '':
        tkMessageBox.showinfo('提示','请输入歌曲名或者歌手名！')
        return
    name = entry.get().encode('utf-8')#获取文本框的输入内容，并将中文转码成utf-8
    #http://s.music.163.com/search/get/?type=1&limit=50&s=%s
    html = urllib.urlopen('http://s.music.163.com/search/get/?type=1&limit=250&s=%s' %name.strip()).read()
    js = json.loads(html)#将返回的json格式转换成字典
    #print js['result']['songs']
    for i in js['result']['songs']:
        #将歌曲的歌名和歌手名插入到列表中,END是插入的index

        listBox.insert(END,i['name'] + ' - (' + i['artists'][0]['name'] + ')')
        musiclist.append(i['audio'])


def play(event):

    sy = listBox.curselection()[0] #返回listBox中的对象的index，以元祖形式返回
    #print 'sy=',sy
    varl.set('正在加载%s。。。'%listBox.get(listBox.curselection(),last=None).encode('utf-8'))#获取当前行号,并写入信息
    #print '正在加载=',listBox.get(listBox.curselection(),last=None).encode('utf-8')
    urllib.urlretrieve(musiclist[sy],'a.mp3')
    varl.set('正在播放%s。。。'%listBox.get(listBox.curselection(),last=None).encode('utf-8'))
    #print '正在播放=',listBox.get(listBox.curselection(),last=None).encode('utf-8')

    fn = r'a.mp3'
    print '正在缓冲。。。'
    try:
        mp3 = mp3play.load(fn)
    except:
        tkMessageBox.showinfo('提示','此歌曲不可播放！')
    #print 'load..'
    mp3.play()
    print '正在播放。。。'
    min(1,mp3.seconds(time.sleep(500)))
    mp3.stop()

root = Tk()  #实例化
root.geometry('+600+200')
entry = Entry(root)
entry.pack()
button = Button(root,text='搜 索',command=music)
button.pack()
var2 = StringVar()#声明变量var2
listBox = Listbox(root,listvariable=var2,width=50)#把变量的值给listBox

listBox.bind('<Double-Button-1>',play)#绑定双击事件，调用play方法
listBox.pack()
varl = StringVar()
label = Label(root,textvariable=varl,fg='red')
varl.set('音乐盒')
label.pack()


root.title('MusicPlay')


root.mainloop()#通过循环来跟踪窗口的显示位置

