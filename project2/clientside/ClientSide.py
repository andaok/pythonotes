
'''
Created on 2012-7-30
@author: wye 
@Copyright@2012 cloudiya technology 
'''
'''
Purpose : 
    Verify that the customer is an authorized user    
'''
import os
import GlobalArgs
import httplib
from M2Crypto import RSA
import xml.etree.ElementTree as ET

#####################
#Get software serial number
#####################
xmltree=ET.parse(GlobalArgs.keyspath+os.sep+"CustomerInfo.xml")
xmlroot=xmltree.getroot()
serialnum = xmlroot.find('serialnum').text.strip()

###################################
#Fetch server hardware infomation
#CpuID+MainDiskID+NICMAC
###################################
hardinfo = "ckejh345jhyutg00:1A:92:E6:D0:0D-shiyan technolei colcd-cdddcdf"

###################################
#Verify that the customer is an authorized user
###################################
connection = httplib.HTTPConnection('127.0.0.1:8087')
connection.request('GET','/ed/'+serialnum)
result = connection.getresponse().read()
    
f = open(GlobalArgs.keyspath+os.sep+'ED-publickey.pem','w')
f.write(result)
f.close()

w = open(GlobalArgs.keyspath+os.sep+'regcode.bin','rb')
data = w.read()
w.close()

publickey = RSA.load_pub_key(GlobalArgs.keyspath+os.sep+'ED-publickey.pem')
decrypthardinfo = publickey.public_decrypt(data,RSA.pkcs1_padding)

print decrypthardinfo






