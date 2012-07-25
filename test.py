'''
reated on Jun 9, 2012

@author: root

'''


bip1 = "10.2.10.16;10.2.10.17"
#bip2 = "10.2.10.16;10.2.10.17"

bip2=""

if  bip1 == "" and bip2 != "":
    liststr = bip2.split(';')
    bip1 = liststr[0]
    bip2=liststr[1]
    print(bip1+":"+bip2)
    
if  bip2 == "" and bip1 != "":
    liststr = bip1.split(';')
    bip1 = liststr[0]
    bip2=liststr[1]
    print(bip1+":"+bip2)
    


