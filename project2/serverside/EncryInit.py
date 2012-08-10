# -*- encoding:utf-8 -*-

'''
Created on Jul 26, 2012
@author: wye 
@Copyright@2012 cloudiya technology 
'''
'''
Purpose :
      Two pairs of keys  and a serial number generated for each set of software
      A pair of keys is used for secure transmission     
      Another a pair of keys is used to encrypt and decrypt the registration code
Usage :
      python EncryInit.py  --customer  Customer Company Name  --email  Customer email      
'''

import os
import optparse
import random
import GlobalArgs
import subprocess
import MySQLdb
from M2Crypto import RSA,BIO
from xml.dom.minidom import Document

######################
#Get command input arguments
######################

cmdopt = optparse.OptionParser(description="init software encryption data for customer",
                                                      prog="EncryInit.py" ,
                                                      version="1.0",
                                                      usage="%prog --customer  Customer Company Name  --email  Customer email" )

cmdopt.add_option('-c','--customer',help="Customer Company Name")
cmdopt.add_option('-e','--email',help="Customer email")

options,arguments = cmdopt.parse_args()


if options.customer == None:
   print "Usage: EncryInit.py --customer  Customer Company Name  --email  Customer email"
else:
   customer =  options.customer.strip()
   
if options.email == None:
   print "Usage: EncryInit.py --customer  Customer Company Name  --email  Customer email"
else:
   email =  options.email.strip()
   
####################
#Serial number generation for customer
####################

def getSerialNumUnit():
    serialnum = ""
    while len(serialnum) <  6:
        intnum = random.randint(0,25)
        lcletter = chr(97 + intnum)
        if serialnum.find(lcletter) == -1:
           serialnum  = serialnum + lcletter
    return serialnum.upper()        

def getSerialNum():
    serialnum = ""
    for i in range(0,4):
        serialnum =  serialnum+ getSerialNumUnit() + "-"
    return serialnum[0:-1]

serialnum =  getSerialNum()

####################
#Check keys store path
####################

execode = subprocess.call("test -d %s"%(GlobalArgs.keyspath+os.sep+serialnum),shell=True)
if execode != 0:
    execode = subprocess.call("mkdir -p %s"%(GlobalArgs.keyspath+os.sep+serialnum),shell=True)
    if execode != 0:
        raise Exception("create keys store path fail")
    else:
        execode = subprocess.call("chown -R apache:apache %s"%(GlobalArgs.keyspath+os.sep+serialnum),shell=True)

####################
#A pair of keys generation for secure transmission
####################

rsakey = RSA.gen_key(1024, 3,lambda *agr:None)
rsakey.save_pub_key(GlobalArgs.keyspath+os.sep+serialnum+os.sep+"ST"+"-"+'publickey.pem')
rsakey.save_key(GlobalArgs.keyspath+os.sep+serialnum+os.sep+"ST"+"-"+'privatekey.pem',None)

#####################
#Another a pair of keys generation for encrypt and decrypt the registration code
#####################

rsakey = RSA.gen_key(1024, 3,lambda *agr:None)
rsakey.save_pub_key(GlobalArgs.keyspath+os.sep+serialnum+os.sep+"ED"+"-"+'publickey.pem')
rsakey.save_key(GlobalArgs.keyspath+os.sep+serialnum+os.sep+"ED"+"-"+'privatekey.pem',None)

#####################
#Generate customer information xml file
#####################
doc = Document()
root = doc.createElement("customerinfo")
doc.appendChild(root)

item = doc.createElement("customer")
item_text = doc.createTextNode(customer)
item.appendChild(item_text)
root.appendChild(item)

item = doc.createElement("email")
item_text = doc.createTextNode(email)
item.appendChild(item_text)
root.appendChild(item)

item = doc.createElement("serialnum")
item_text = doc.createTextNode(serialnum)
item.appendChild(item_text)
root.appendChild(item)

f = open(GlobalArgs.keyspath+os.sep+serialnum+os.sep+"ST"+"-"+'privatekey.pem','rb')
data = f.read()
f.close()

item = doc.createElement("stprikey")
item_text = doc.createTextNode(data.strip())
item.appendChild(item_text)
root.appendChild(item)

f = open(GlobalArgs.keyspath+os.sep+serialnum+os.sep+'CustomerInfo.xml','a+')
f.write(doc.toprettyxml(indent=""))
f.close()

#####################
#Add  customer infomation to database
#####################
dbconn = MySQLdb.connect(host=GlobalArgs.mysqlserver,user=GlobalArgs.mysqluser,passwd=GlobalArgs.mysqlpwd)
dbcursor = dbconn.cursor()
dbconn.select_db('SoftwareEncryption')
value = [customer,email,serialnum]
dbcursor.execute("insert into customerinfo (customer,email,sn) values(%s,%s,%s)",value)
dbcursor.close()


