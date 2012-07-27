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

import httplib
import xml.etree.ElementTree as ET
from M2Crypto  import  RSA,BIO

#####################
#Static argument
#####################
customerinfoxml="customerinfo.xml"

#####################
#Get software serial number
#####################
xmltree=ET.parse(customerinfoxml)
xmlroot=xmltree.getroot()
serialnum = xmlroot.find('serialnum').text

#####################
#Fetch server hardware infomation
#CpuID+MainDiskID+NICMAC
#####################
hardinfo = "ckejh345jhyutg700-df-hj-78-89-cd"
#hardinfo = "zxczx"

#####################
#Encrypt hardware infomation with the secure transmission public key
#####################
stprikeystr =  xmlroot.find('stprikey').text
privatekey = RSA.load_key_string(stprikeystr)
encryptstr = privatekey.private_encrypt(hardinfo,RSA.pkcs1_padding)

print encryptstr



publickey = RSA.load_pub_key('/tmp/temp/FKPZTE-KNYAXH-CNVXEF-NTLVXU-ST-publickey.pem')
decryptstr = publickey.public_decrypt(encryptstr,RSA.pkcs1_padding)

print decryptstr

f = open('/tmp/temp/test.txt','w')
f.write(encryptstr)
f.close

connection = httplib.HTTPConnection('192.168.0.111:8088')
send_data = "hardinfoencryptstr="+encryptstr
header = {'Content-Type': 'application/x-www-form-urlencoded'}
connection.request('PUT', '/st/FKPZTE-KNYAXH-CNVXEF-NTLVXU',send_data,header)
result = connection.getresponse().read()
print result
