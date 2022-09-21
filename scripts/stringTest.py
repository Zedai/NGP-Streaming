import matplotlib.pyplot as plt
import numpy as np
import socket
from pickle import loads, dumps

HOST='127.0.0.1'
PORT=12348

s = socket.socket()
print('Socket Created')
s.bind((HOST, PORT))
print('Socket Bound')
s.listen(5)
print('LISTENING')


i = 0

c, addr = s.accept()
print('Got connection from', addr)
while True:
	data = b""
	mat = loads(c.recv(4096))
	print(mat)
	input = input("Enter Input:")
	str = b"Received" + mat +  b"     Sent: " + input 
	c.send(dumps(str))
	c.send(b'done')
