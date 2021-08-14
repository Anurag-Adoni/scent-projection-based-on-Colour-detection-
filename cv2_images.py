""" Anurag Nag Adoni """
import cv2
import time
import os
import numpy
import glob
import time
import serial
import serial.tools.list_ports  #getting list of ports 
from serial import Serial
import pygame, sys
from pygame.locals import *


def get_ports():
    ports = serial.tools.list_ports.comports()  
    return ports

def findArduino(portsFound):  #finding specific COM port 
    commPort = 'None'
    numConnection = len(portsFound)
    
    for i in range(0,numConnection):
        port = foundPorts[i]
        strPort = str(port)
        
        if 'USB-SERIAL' in strPort: 
            splitPort = strPort.split(' ')
            commPort = (splitPort[0])
    return commPort
            
                    
foundPorts = get_ports()        
connectPort = findArduino(foundPorts)

if connectPort != 'None':      #initializing COM ports 
    ser = serial.Serial(connectPort,baudrate = 9600, timeout=1)
    print('Connected to ' + connectPort)
else:
    print('Connection Issue!')
print('DONE')

file_names = [img for img in glob.glob("test_photos/*.jpg")]
file_names.sort() 
image_list = []     # this is the list where we stor the images 

for img in file_names:  # here we use thresholding for converting theimage to near rgb
    n= cv2.imread(img) # Note numpy.maximum and numpy.max are different
    scale_percent = 50
    width = int(n.shape[1] * scale_percent / 100)
    height = int(n.shape[0] * scale_percent / 100)
    dim = (width, height)
    (B, G, R) = cv2.split(n)
    M = numpy.maximum(numpy.maximum(R, G), B)
    R[R < M] = 0
    G[G < M] = 0
    B[B < M] = 0
    n = cv2.merge([B, G, R])
    n = cv2.resize(n, dim, interpolation = cv2.INTER_AREA)
    image_list.append(n)
    
#To display the converted thrshold image 
    #cv2.imshow('dst_rt', n)            
    #cv2.waitKey(6000)           
    #cv2.destroyAllWindows()
    
FPS = 1.5   # use this to set the speed of the output data 
fpsClock = pygame.time.Clock()  #note: unit is not frame per second
starttime = time.time()

for i in range(0, len(image_list)):
    
    myimg = image_list[i] # Get the ith image
    avg_color_per_row = numpy.mean(myimg, axis=(0))
    avg_color = numpy.mean(avg_color_per_row, axis=(0))

    b = round(avg_color[0])
    g = round(avg_color[1]) # remove the round function to get data in floats 
    r = round(avg_color[2]) #do not use abs function here 

    #print(" dominant colour = " , round(max(avg_color)))
    x = 'x' # for blue
    y = 'y' # for red
    z = 'z' # for green

    if b > r and b > g:
        print("dominant color is blue = ", b)
        ser.write(b'0')
            
    elif r > b and r > g:
        print("dominant color is red = ", r)
        ser.write(b'1')
        
    elif g > r and g > b:
        print("dominant color is green = ",g)
        ser.write(b'2')

    fpsClock.tick(FPS)
