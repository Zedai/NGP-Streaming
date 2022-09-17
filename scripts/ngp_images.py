import os
import glob 
import numpy as np
import imageio
import cv2
#import matplotlib.pyplot as plt
import socket
from pickle import dumps
import time

image_frame = glob.glob('/home/sai/ngp_rendered_images/*.png')

HOST='127.0.0.1'
PORT=12345

s = socket.socket()
print('Socket Created')
s.bind((HOST, PORT))
print('Socket Bound')
s.listen(5)
print('LISTENING')
c, addr = s.accept()
print('Got connection from', addr)

try:
	for data in image_frame:
	    #img = Image.open(data)
	    img = imageio.imread(data)
	    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

	    img_array = np.asarray(img)
#	    print(img_array.shape)
	 #   plt.imshow(img_array)
	 #   plt.show()
	    while True:
	        if c.recv(1000) == b"go": break
	    c.send(dumps(img_array)) 
	    c.send(b'done')
#	    time.sleep(10)
	print("All Images Streamed")
	s.close()
except KeyboardInterrupt:
	s.close()
