# -*- encoding:utf-8 -*-

'''
Created on Jul 27, 2012
@author: wye 
@Copyright@2012 cloudiya technology 
'''
'''
Purpose : 
      Return registration code to customer
      Verify the registration code for customer
'''

import os
import sys
import bottle
import MySQLdb
import GlobalArgs
import subprocess
from M2Crypto import RSA
from bottle import route,run,request,debug,static_file

os.chdir(os.path.dirname(__file__))
wsgi_dir=os.path.dirname(__file__)
sys.path = [wsgi_dir]+sys.path

###############################
#Generate registration code
###############################
@route('/st/<serialnum>',method='POST')
def generate_RegCode(serialnum):
    
    if "" != serialnum:
         encrypthardinfoObject = request.body.read() 
         publickey = RSA.load_pub_key(GlobalArgs.keyspath+os.sep+serialnum+os.sep+'ST-publickey.pem')
         decrypthardinfo = publickey.public_decrypt(encrypthardinfoObject,RSA.pkcs1_padding)
         
         privatekey = RSA.load_key(GlobalArgs.keyspath+os.sep+serialnum+os.sep+'ED-privatekey.pem')
         encryptregcode = privatekey.private_encrypt(decrypthardinfo,RSA.pkcs1_padding)
         
         f = open(GlobalArgs.keyspath+os.sep+serialnum+os.sep+'regcode.bin','w')
         f.write(encryptregcode)
         f.close()
         
         execode = subprocess.call("test -s %s"%(GlobalArgs.keyspath+os.sep+serialnum+os.sep+'regcode.bin'),shell=True)
         if execode == 0:
             #add customer hardware information to database
             hardinfolist = decrypthardinfo.split('/')
             maindisksn = hardinfolist[1]
             mainnicmac = hardinfolist[3]
             
             dbconn = MySQLdb.connect(host=GlobalArgs.mysqlserver,user=GlobalArgs.mysqluser,passwd=GlobalArgs.mysqlpwd)
             dbcursor = dbconn.cursor()
             dbconn.select_db('SoftwareEncryption')
             value = [maindisksn,mainnicmac,serialnum]
             dbcursor.execute("update customerinfo set  maindisksn=%s,mainnicmac=%s where sn=%s",value)
             dbcursor.close()
             
             return {"success":True,"error":"no error"}
         else:
            return {"success":False,"error":"generate registration code fail in server side"}  
    else:
        return {"success":False,"error":"serialnum is null from client side"}


###############################
#Return registration code to customer
###############################
@route('/st/<serialnum>',method='GET')
def return_Regcode(serialnum):
    if serialnum != "":
        return static_file('regcode.bin',root=GlobalArgs.keyspath+os.sep+serialnum)
    else:
        return {"success":False,"error":"serialnum is null from client side"}
      

################################
#Return ED-publickey to customer
################################
@route('/ed/<serialnum>',method="GET")
def return_EDpubkey(serialnum):
    if serialnum != "":
        return static_file('ED-publickey.pem',root=GlobalArgs.keyspath+os.sep+serialnum)
    else:
        return {"success":False,"error":"serialnum is null from client side"}


###############################
application = bottle.app()
###############################
