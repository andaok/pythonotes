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
import MySQLdb
import GlobalArgs
import subprocess
from M2Crypto import RSA
from bottle import route,run,request,debug,static_file

###############################
#Generate registration code
###############################
@route('/software/verify/st/<serialnum>',method='POST')
def generate_RegCode(serialnum):
    
    if "" != serialnum:
         #check the serial number whether has been registered
         dbconn = MySQLdb.connect(host=GlobalArgs.mysqlserver,user=GlobalArgs.mysqluser,passwd=GlobalArgs.mysqlpwd)
         dbcursor = dbconn.cursor()
         dbconn.select_db('SoftwareEncryption')
         value = [serialnum]
         count = dbcursor.execute("select IsVerify from customerinfo where sn=%s",value)
         if count == 0:
             return {"success":False,"error":"serial number is invaild"}
         else:
             result = dbcursor.fetchone()
             dbcursor.close()
             if result[0] == "True":
                 return {"success":False,"error":"the serial number has been registered"}        
             else:
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
                    value = [maindisksn,mainnicmac,"True",serialnum]
                    dbcursor.execute("update customerinfo set maindisksn=%s,mainnicmac=%s,IsVerify=%s,VerifyTime=now() where sn=%s",value)
                    dbcursor.close()
             
                    return {"success":True,"error":"no error"}
                 else:
                    return {"success":False,"error":"generate registration code fail in server side"}  
    else:
        return {"success":False,"error":"serialnum is null from client side"}

###############################
#Return registration code to customer
###############################
@route('/software/verify/st/<serialnum>',method='GET')
def return_Regcode(serialnum):
    if serialnum != "":
        return static_file('regcode.bin',root=GlobalArgs.keyspath+os.sep+serialnum)
    else:
        return {"success":False,"error":"serialnum is null from client side"}
      

################################
#Return ED-publickey to customer
################################
@route('/software/verify/ed/<serialnum>',method="GET")
def return_EDpubkey(serialnum):
    if serialnum != "":
        return static_file('ED-publickey.pem',root=GlobalArgs.keyspath+os.sep+serialnum)
    else:
        return {"success":False,"error":"serialnum is null from client side"}


debug(True)
run(host='0.0.0.0',port=8087)