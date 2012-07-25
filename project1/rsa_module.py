# -*- encoding:utf-8 -*-
'''
Created on Jul 23, 2012

@author: root
'''

import rsa

#生成一对公钥与私钥，并保存。
(publickey,privatekey) = rsa.newkeys(1024)

pub = publickey.save_pkcs1()
publickeyfile=open('/tmp/publickey1.pem','w+')
publickeyfile.write(pub)
publickeyfile.close()

pri = privatekey.save_pkcs1()
privatekeyfile = open('/tmp/privatekey1.pem','w+')
privatekeyfile.write(pri)
privatekeyfile.close()

#公钥加密字符串,私钥解密.
message="cloudiya"
with open('/tmp/publickey.pem')  as  publickeyfile:
    p=publickeyfile.read()
    publickey=rsa.PublicKey.load_pkcs1(p)
    
with open('/tmp/privatekey.pem') as privatekeyfile:
    p=privatekeyfile.read()
    privatekey=rsa.PrivateKey.load_pkcs1(p)
    
encryptstr = rsa.encrypt(message,publickey)
decryptstr = rsa.decrypt(encryptstr,privatekey)
print(decryptstr)

#用私钥签名认证,再用公钥验证签名.
signature = rsa.sign(message,privatekey,'SHA-1')
print(rsa.verify('cloudiya',signature,publickey))







