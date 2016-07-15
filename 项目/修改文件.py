#-*-coding:utf-8-*-
'''修改当前目录下的内容含有NQM字样的的文本，删除每行中出现的--人名，并在完成后弹窗提示修改的文本记录'''

from Tkinter import tkinter as tk
import os,time,sys,xlrd
reload(sys)
sys.setdefaultencoding( "utf-8" )


global Dict
Dict = {}
def find():
    '''查找当前目录下的所有文件'''
    pass

def files(fileName='NQM.xls'):
    '''打开指定文件，读取内容并返回指定内容'''
    cotent = xlrd.open_workbook(fileName)
    tables = cotent.sheet_by_index(0)
    return  tables

def getTableData():
    '''获取行内容'''
    table = files()
    for i in range(1,table.nrows):
        yield table.row_values(i)

def indexs(name):
    '''取指定的内容字段的列'''
    table = files()
    rowValues = table.row_values(0)
    try:
        clo1 = rowValues.index(name)
        return clo1
    except:
        print '"%s"未找到！'%name

def hos():
    '''获取所有现场目录'''
    hoslist = []  #所有现场名
    table = files()
    hosName = indexs(u'移动医疗实施项目')
    lines = getTableData()
    for i in lines:
        #i[hosName]=医院名
        hoslist.append(i[hosName])
    hoslist = list(set(hoslist))
    return hoslist


def filew(content):
    '''写文件'''
    with open('123.txt','w') as f:
        f.write(content)

def sqls(row,clo):
    '''检索sql'''
    table = files()
    content = table.cell(row,clo)
    list2 = repr(content).split(r'\n')
    sql = ''
    for i in list2:
        if 'SQL' in i.upper():
            sql += i + '\n'
        else:
            sql += ' '
    return  sql

def start():
    names = hos()
    print 'names:',names
    table = files()
    hosNum = indexs(u'移动医疗实施项目')
    clo1 = indexs(u'标识')
    clo2 = indexs(u'主题')
    clo3 = indexs(u'报告人')
    clo4 = indexs(u'上传源代码文件列表')

    hosdic = {}
    hossql = {}
    nohos = {}
    f = open('123.txt','w')
    for j in range(1,table.nrows):
        clo1s = table.cell_value(j,clo1) #标识
        clo2s = table.cell_value(j,clo2) #主题
        clo3s = table.cell_value(j,clo3) #报告人
        clo4s = table.cell_value(j,clo4) #上传源代码文件列表
        sql = sqls(j,clo4)
        hossql[clo1s] = sql
        hosName = table.cell_value(j,hosNum)
        if hosName.strip()=='':
            nohos[clo1s] = clo2s
            f.write('本地创建任务：\n')
            for i in nohos.keys():
                line1 = '%s %s'%(i,nohos[i])
                f.write('\n')
                f.write(line1)
                f.write('\n')
                f.write(sql)
        else:
            hosdic[clo1s] = clo2s
            Dict[hosName] = hosdic

    keys = Dict.keys()
    for i in keys:
        f.write(i)
        f.write('\n')
        for j in Dict[i].keys():
            line = '%s %s'%(j,Dict[i][j])
            f.write('\n')
            f.write(line)
            f.write('\n')
            f.write(hossql[j])

    f.close()

start()