#!/usr/bin/env python
import rospy
from pickle import dumps, loads
from std_msgs.msg import String, Header, UInt8
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped
import socket
import matplotlib.pyplot as plt
import numpy as np
import time

global s
global latestData

def interface():
    rospy.init_node('nerf_tester', anonymous=True)
    rospy.Subscriber("/trigger", UInt8, callback)
    pub = rospy.Publisher('renderedView', String, queue_size=10)

    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        while True:
            try:
                if latestData is not None:
                    break
                break
            except NameError:
                pass

        print("out")
        fragments = []
        s.send(dumps(mat))
        while True:
            packet = s.recv(1000)
            if packet[-4:] == b'done':
                fragments.append(packet[:-4])
                break
            if not packet: break
            fragments.append(packet)
        final = loads(b"".join(fragments))


        msg.data = final

        pub.publish(msg)

        rate.sleep()


def callback(data):
    print("Callback")
    try:
        if latestData is None:
            latestData = 1
    except NameError:
        latestData = 1
    latestData += 1


if __name__ == '__main__':
    try:
        s = socket.socket()
        while True:
            try:
                s.connect(('127.0.0.1', 12348))
                break
            except ConnectionRefusedError:
                print('NerF Simulator not Running')
                
        interface()
    except rospy.ROSInterruptException:
        s.close()
        pass
