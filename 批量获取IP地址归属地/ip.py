#!/usr/bin/env python
#-*- coding: utf-8 -*-
import re      #导入正则表达式模块
import sys     
import requests
import time

#以只读方式打开文件，sys.argv[1]表示的是运行时传入的第二个参数
f = open(sys.argv[1], "r") 
arr = {}      #用字典来存储IP跟访问次数

num='((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}'
lines = f.readlines()
#遍历文件的每一行   
for line in lines:
        match = re.search(num,line)  #python中用“+”来连接字符串
        if match: 
                ip = match.group()
                if ip in arr:
                    arr[ip] += 1 
                else:  
                    arr[ip]=1  
f.close()  
for key in arr:
    try:
        r=requests.post(url='http://ip.taobao.com/service/getIpInfo2.php', data={'ip': key})
        if(r.status_code==200 and r.json()['code']==0):
            jsonObj=r.json()['data']
            print(key+"-"+str(arr[key])+"-"+jsonObj['country']+'-'+jsonObj['area']+'-'+jsonObj['region']+'-'+jsonObj['city']+'-'+jsonObj['isp']  )
        else:
            print(" 错误应答"+str(r.status_code)+str(r.json()['code']))
        time.sleep(1)
    except Exception as e:
        print("错误"+str(e))       # Important!
    