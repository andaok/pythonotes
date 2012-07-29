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
import GlobalArgs
import subprocess
from M2Crypto import RSA,BIO
from bottle import route,run,request,debug,static_file

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
#Verify the registration code for customer
################################
@route('/ed/<serialnum>',method="GET")
def return_EDpubkey(serialnum):
    if serialnum != "":
        return static_file('ED-publickey.pem',root=GlobalArgs.keyspath+os.sep+serialnum)
    else:
        return {"success":False,"error":"serialnum is null from client side"}


debug(True)
run(host='0.0.0.0',port=8087)