#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#自动将crash处理成对应的人
#现阶段只处理主版的crash
import os
import sys
import time
import re
from operator import itemgetter, attrgetter  

#默认地址
#包含各种model的地址
defaultStartPath = ["app/src/main/java/"]

pakageName = "pakageName"

#获取输入参数
def getPath():
    if len(sys.argv) == 1:
        print("请输入crash_log地址")
        return
    return sys.argv[1]

def trimStartSpace(line):
    return str.strip(line)

#从log中拆出来everphoto开头的line
def handleLog(path):
    fileReader = open(path, "r+")
    blameResult = []
    if fileReader == None:
        print("文件不存在")
    else:
        lines = fileReader.readlines()
        for line in lines:
            line = trimStartSpace(line)
            if str.startswith(line, "at pakageName"):
                print(line)
                num = getLineNum(line)
                position = getLinePosition(line)
                blameResult.append(gitBlame(position, num))
    list.sort(blameResult, key = timeCmp, reverse = True)
    return blameResult


#比较函数
def timeCmp(s):
    return s['time']

#从line中获取某个line的具体信息
def getLogInfo(line):
    return 
    

#从line的最后几位获取数字
def getLineNum(line):
    pattern = re.compile(":(.\d*?)\)")
    num = re.findall(pattern, line, 0)
    if num != None and len(num) != 0:
        return num[0]

#从获取文件的路径的
def getLinePosition(line):
    line = str.replace(line, ".java", "dotjava")
    #找有.的路径
    pattern = re.compile("at\s(.+)\.\w*")
    position = re.findall(pattern, line, 0)
    print(position)
    if position != None and len(position) != 0:
         if str.__contains__(position[0], '$'):
             print("ok")
             #将$前的文件名抽出来
             position = re.findall(re.compile("(.+)\$"), position[0], 0)
    
    if position != None and len(position) != 0:
        for startPath in defaultStartPath:
            plusPath = startPath + position[0].replace('.', '/') + ".java"
            print(plusPath)
            if os.path.isfile(plusPath):
                print(plusPath)
                return plusPath

#获取文件的git blame信息
def gitBlame(filePosition, line):
    command = "git blame " + filePosition + " -L " + line + "," + line
    print(command)
    blame = os.popen(command).read()
    print(blame)
    return getInfoFromBlameInfo(filePosition, blame)

#从blame信息中获取名字和时间
def getInfoFromBlameInfo(filePosition, blame):
    patternName = re.compile("\s\((.+?)\s")
    name = re.findall(patternName, blame, 0)
    patternTime = re.compile("\d{4}[\-]\w*[\-]\w*\s\d*\:\d*\:\d*")
    timeResult = re.findall(patternTime, blame)
    print(name)
    print(timeResult)
    # if len(name) == 1 and len(time) == 1:
        #2016-07-26 19:44:22 +0800 时间格式
    info = {"name" : name[0], 
            "time" : time.mktime(time.strptime(timeResult[0], "%Y-%m-%d %H:%M:%S")),
            "timeHumen" : timeResult, 
            "file" : filePosition}
    return info

#打印数据
def printInfo(item):
    print("name :" + dict.get(item, "name"))
    print("file :" + dict.get(item, "file"))
    print("time :" + str(dict.get(item, "timeHumen")))


#main()
path = getPath()
if path != None:
    try:
        result = handleLog(path)
        print(result)
        print("======================最后修改========================")
        printInfo(result[0])
        print("======================相关人员=========================")
        for item in result:
            printInfo(item)
    except :
        print("没有找到相关信息，请手动查找")