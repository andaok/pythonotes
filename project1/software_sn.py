# -*- encoding:utf-8 -*-

'''
Created on Jul 25, 2012

@author: root
'''

import random

#软件序列号

def getstr():
    st = ""
    while len(st) <  6:
        intnum = random.randint(0,25)
        temp = chr(97 + intnum)
        if st.find(temp) == -1:
            st = st+temp
    return st.upper()        

def getsn():
    sn = ""
    for i in range(0,4):
        sn = sn + getstr() + "-"
    return sn[0:-1]

print(getsn())

