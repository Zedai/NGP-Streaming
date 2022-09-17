#!/usr/bin/env python
import rospy
from pickle import dumps, loads
from std_msgs.msg import String, Header
from sensor_msgs.msg import Image
import socket
import matplotlib.pyplot as plt
import numpy as np

global s

def ngp_display():
    pub = rospy.Publisher('ngp_image', Image, queue_size=10)
    rospy.init_node('ngp_display', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
#        data = b""
        fragments = []
        s.send(b"go")
        while True:
            packet = s.recv(1000)
#            print(packet)
            if packet[-4:] == b'done':
                fragments.append(packet[:-4])
                break
            if not packet: break
            fragments.append(packet)
#        data = s.recv(4096000000)
        final = loads(b"".join(fragments))
#        plt.imshow(final)
#        plt.show()
#        print(final.shape)

        head = Header()
        head.seq = 1
        head.stamp.secs = 1
        head.stamp.nsecs = 1
        head.frame_id = "1"

        msg = Image()
        msg.header = head
        msg.height = final.shape[0]
        msg.width = final.shape[1]
        msg.step = final.shape[1] * 3
        msg.encoding = "rgb8"
        msg.is_bigendian = 0 
        convertedData = np.zeros((msg.height, msg.step), dtype = 'int')

        for i in np.arange(final.shape[0]):
            for j in np.arange(final.shape[1]):
                convertedData[i,j * 3] = final[i, j, 0]
                convertedData[i,j * 3 + 1] = final[i, j, 1]
                convertedData[i,j * 3 + 2] = final[i, j ,2]

        msg.data = convertedData.reshape(msg.height * msg.step).tolist()
        
        pub.publish(msg)

        rate.sleep()

if __name__ == '__main__':
    try:
        s = socket.socket()
        while True:
            try:
                s.connect(('127.0.0.1', 12345))
                break
            except ConnectionRefusedError:
                print('Data not ready to stream')
        ngp_display()
    except rospy.ROSInterruptException:
        s.close()
        pass
    except EOFError:
       print("EOF (All Images Received?)") 
       pass
