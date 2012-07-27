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

from M2Crypto  import  RSA,BIO
from bottle import route,run,request,debug

regcode = "KZDJKADJKLASDAKLSDJLAKJDALDJASLKDJKLA"

@route('/st/<name>',method='PUT')
def return_RegCode(name):
    #hardinfoencryptstr = request.forms.get("hardinfoencryptstr")
    hardinfoencryptstr = request.files.values
    if "" != name and "" != hardinfoencryptstr:
         
         f = open('/tmp/temp/ser.txt','w')
         f.write(hardinfoencryptstr)
         f.close
         return "hello"+hardinfoencryptstr
        #return {"success":True,"error":"xihadasdas"}
        #publickey = RSA.load_pub_key('/tmp/temp/FKPZTE-KNYAXH-CNVXEF-NTLVXU-ST-publickey.pem')
        #decryptstr = publickey.public_decrypt(hardinfoencryptstr,RSA.no_padding)
        #return {"success":True,"error":decryptstr}
    else:
        return {"success":False,"error":"xihadasdas"}
    
debug(True)
run(host='0.0.0.0',port=8088)
        
    