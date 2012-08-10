
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
import random
import subprocess
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
#mainDiskSn+mainNicMac
###################################
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

###################################
#Verify that the customer is an authorized user
###################################
try:
    w = open(GlobalArgs.keyspath+os.sep+'regcode.bin','rb')
except IOError:
    raise Exception("Can not find the registration code")
else:
    data = w.read()
    w.close()

execode = subprocess.call("test -s %s"%(GlobalArgs.keyspath+os.sep+'ED-publickey.pem'),shell=True)
if execode != 0:
    connection = httplib.HTTPConnection(GlobalArgs.vhostname)
    connection.request('GET','/software/verify/ed/'+serialnum)
    result = connection.getresponse().read()
    
    f = open(GlobalArgs.keyspath+os.sep+'ED-publickey.pem','w')
    f.write(result)
    f.close()

publickey = RSA.load_pub_key(GlobalArgs.keyspath+os.sep+'ED-publickey.pem')
decrypthardinfo = publickey.public_decrypt(data,RSA.pkcs1_padding)

hardinfolist = decrypthardinfo.split('/')

if hardinfolist[1] == maindisksn and hardinfolist[3] == mainnicmac:
    print "Verify Pass"
else:
    print "Verify Fail"






