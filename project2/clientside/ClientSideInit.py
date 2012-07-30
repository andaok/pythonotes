# -*- encoding:utf-8 -*-

'''
Created on Jul 27, 2012
@author: wye 
@Copyright@2012 cloudiya technology 
'''

'''
Purpose:
      Commit customer server hardware information to cloudiya cloud verifyserver,retrieve registration code.
'''

import os
import json
import httplib
import random
import subprocess
import GlobalArgs
import xml.etree.ElementTree as ET
from M2Crypto import RSA

#####################
#Get software serial number
#####################
xmltree=ET.parse(GlobalArgs.keyspath+os.sep+"CustomerInfo.xml")
xmlroot=xmltree.getroot()
serialnum = xmlroot.find('serialnum').text.strip()

#####################
#Fetch server hardware infomation
#mainDiskSn+mainNicMac
#####################
p=subprocess.Popen("hdparm -I /dev/sda | grep 'Serial Number' | awk -F: '{print $2}'",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
if p.stderr.read() == "":
    maindisksn = p.stdout.read().strip()
else:
    raise Exception

p = subprocess.Popen("ifconfig eth0 | grep HWaddr | awk '{print $5}'",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
if p.stderr.read() == "":
    mainnicmac = p.stdout.read().strip()
else:
    raise Exception

def getSerialNumUnit(num):
    serialnum = ""
    while len(serialnum) <  num:
        intnum = random.randint(0,25)
        lcletter = chr(97 + intnum)
        if serialnum.find(lcletter) == -1:
           serialnum  = serialnum + lcletter
    return serialnum.upper()

hardinfo ="WD-"+getSerialNumUnit(10)+"/"+maindisksn+"/"+getSerialNumUnit(10)+"/"+mainnicmac+"/"+getSerialNumUnit(10)

#####################
#Encrypt hardware infomation with the secure transmission public key
#####################
stprikeystr =  xmlroot.find('stprikey').text
privatekey = RSA.load_key_string(stprikeystr)
encrypthardinfo = privatekey.private_encrypt(hardinfo,RSA.pkcs1_padding)

connection = httplib.HTTPConnection(GlobalArgs.vhostname)
header = {'Content-Type': 'application/x-www-form-urlencoded'}
connection.request('POST','/st/'+serialnum,encrypthardinfo,header)
result = connection.getresponse().read()
resultdict = json.loads(result)

if resultdict["success"] == True:
    connection = httplib.HTTPConnection(GlobalArgs.vhostname)
    connection.request('GET','/st/'+serialnum)
    result = connection.getresponse().read()
    
    f = open(GlobalArgs.keyspath+os.sep+'regcode.bin','w')
    f.write(result)
    f.close()
else:
    errorstr = resultdict["error"]
    raise Exception(errorstr)







