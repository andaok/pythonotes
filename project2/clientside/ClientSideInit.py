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
#CpuID+MainDiskID+NICMAC
#####################
hardinfo = "ckejh345jhyutg00:1A:92:E6:D0:0D-shiyan technolei colcd-cdddcdf"

#####################
#Encrypt hardware infomation with the secure transmission public key
#####################
stprikeystr =  xmlroot.find('stprikey').text
privatekey = RSA.load_key_string(stprikeystr)
encrypthardinfo = privatekey.private_encrypt(hardinfo,RSA.pkcs1_padding)

print stprikeystr

#serialnum = "ONVAMK-QPOCHM-RJKUHS-YBIPVD"
print serialnum


connection = httplib.HTTPConnection('127.0.0.1:8087')
header = {'Content-Type': 'application/x-www-form-urlencoded'}
connection.request('POST','/st/'+serialnum,encrypthardinfo,header)
result = connection.getresponse().read()
resultdict = json.loads(result)

if resultdict["success"] == True:
    connection = httplib.HTTPConnection('127.0.0.1:8087')
    connection.request('GET','/st/'+serialnum)
    result = connection.getresponse().read()
    
    f = open(GlobalArgs.keyspath+os.sep+'regcode.bin','w')
    f.write(result)
    f.close()
else:
    errorstr = resultdict["error"]
    raise Exception(errorstr)







