import sys
#import socket module 
import socket
def xor(a,b):
	tryans = []
	for i in range(1,len(b)):
	# Traverse all bits, append their xor to the ans 
		x=((int(a[i]))^(int(b[i])))
		tryans.append(str(x))
	return ''.join(tryans)

# Create a socket object 
s = socket.socket()
#second argument is port's no. on which to connect	
port = int(sys.argv[2])
# connect to the server on local computer
s.connect(('127.0.0.1', port))
# Get the string to be sent from input
send_Str = raw_input("String to be sent:")
#step 1:The string i(x) is converted into binary string data.
bin_str =(''.join(format(ord(x), 'b') for x in send_Str)) 
print("The length of the string is", len(bin_str))
#key of the generator polynomial is the first argument
key = str(sys.argv[1])
print("The key is",key) 
lk = len(key)
#step 2:Augment n-k-1 zeros at the end of the binary data (i.e multiply by xn-k).
append_data = bin_str + '0'*(lk-1)
#step 3:Divide it by generator polynomial g(x) using modulo 2 division.
#Slicing the number of bits to be XORed at a time from the dividend
tmp = append_data[0:lk]
while lk < len(append_data):
	if tmp[0]=='0':
		# If leftmost bit is '0' we have to use all-0s divisor.
		tmp = xor('0'*lk,tmp)
	else:
		# replace the divident by the xor result
		tmp = xor(key,tmp)
	#pull 1 bit down 
	tmp = tmp + append_data[lk]
	# increment ptr to move further
	lk += 1
#For last n bits, it is done normally as increased value of ptr may go out of bounds
if tmp[0]=='0':
	tmp = xor('0'*lk,tmp)
else:	
	tmp = xor(key,tmp)
fin = bin_str + tmp
print(fin)
s.sendall(fin)
# print the received data from the server
print(s.recv(1024))
#close the connection
s.close() 
