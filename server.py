import numpy as np
import socket
import sys
def xor(a,b):
    tryans = []
    for i in range(1,len(b)):
        x=((int(a[i]))^(int(b[i])))
        tryans.append(str(x))
    return ''.join(tryans)
s = socket.socket()
print("socket is initialised")
port_number = int(sys.argv[2])
s.bind(('',port_number))
s.listen(5)
print("socket is listening , port is ",port_number)
while(1):
    generator =str(sys.argv[1])#"1011" #
    genlen = len(generator)
    c,addr = s.accept()
    print ("connected to client at address ",addr)
    data = c.recv(1024)
    if(data):
        print "received data from client"
    else:
        break
    #Augment n-k-1 zeros at the end of the binary data (i.e multiply by x^n-k).
    data_dividend = data + '0'*(genlen-1)
    #Divide it by generator polynomial g(x) using modulo 2 division.
    #Slicing the number of bits to be XORed at a time from the dividend
    tmp = data_dividend[0 : genlen]
    leftit = genlen
    while leftit < len(data_dividend):
        if tmp[0] == '0':
            # replace the divident by the xor result
            tmp = xor('0'*leftit, tmp)
        else:
            # If leftmost bit is '0' we have to use all-0s divisor.
            tmp = xor(generator, tmp)
        #pull 1 bit down
        tmp = tmp + data_dividend[leftit]
        # increment ptr to move further
        leftit += 1
    #For last n bits, it is done normally as increased value of ptr may go out of bounds
    if tmp[0] == '0':
        tmp = xor('0'*leftit, tmp)
    else:
        tmp = xor(generator, tmp)
    decoded = tmp
    if(decoded == "0"*(genlen-1)):
        print "DATA RECEIVED WITHOUT ERRORS"
        c.sendall("Thankyou, DATA RECEIVED,remainder is "+decoded)
    else:
        print "ERROR FOUND"
        c.sendall("Error found, Retransmit data and remainder is " +decoded)
c.close()
