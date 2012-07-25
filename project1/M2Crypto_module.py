'''
Created on Jul 23, 2012

@author: root
'''

from M2Crypto  import  RSA,BIO

rsakey = RSA.gen_key(1024, 3,lambda *agr:None)
pub_bio = BIO.MemoryBuffer()
priv_bio = BIO.MemoryBuffer()

print(pub_bio)

rsakey.save_pub_key_bio(pub_bio)
rsakey.save_key_bio(priv_bio, None)

print(pub_bio)

publickey = RSA.load_pub_key_bio(pub_bio)
privatekey = RSA.load_key_bio(priv_bio)

message="cloudiya"
encryptstr = publickey.public_encrypt(message, RSA.pkcs1_padding)
decryptstr = privatekey.private_decrypt(encryptstr, RSA.pkcs1_padding)

print(decryptstr)






