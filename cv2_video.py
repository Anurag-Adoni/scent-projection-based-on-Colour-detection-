""" Anurag Nag Adoni """
import cv2
import time
import os
from os import listdir
from os.path import isfile, join
import os, shutil
import numpy
import glob
import time
import serial
import serial.tools.list_ports  #getting list of ports
import sys
from serial import Serial
import pygame, sys
from pygame.locals import *
import multiprocessing # do notinstall this module if python version is old 
import pyfiglet

result = pyfiglet.figlet_format("Code Version: 2.4.1", font = "slant" )
print(result)

'''initializing the serial communication to arduino'''

arduino_com_port = 'COM7'
print(arduino_com_port)
try:
    ser = serial.Serial(arduino_com_port, 9600)
    ser.timeout = 1
except:
    print("Error connecting to com port")
    
'''Reading the input video file and resizing it to dim(160,90)'''

cap = cv2.VideoCapture('test2.mp4')  # Video File Path 
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.mp4',fourcc, 24, (160,90)) # Resizing params

''' converting video file to frames'''

while True:
    ret, frame = cap.read()
    if ret == True:
        b = cv2.resize(frame,(160,90),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
        out.write(b)
    else:
        break
cap.release()
out.release()
cv2.destroyAllWindows()    


def video_to_frames(input_path, output_path):
    """this is a Function to extract frames from a input video file
    and save them as separate frames in an output directory
    input_path: is the input video file. 
    output_path: is the output directory to save the frames. note: the file is
    later deleted"""
    
    try:
        os.mkdir(output_path)
    except OSError:
        pass
    time_start = time.time()
    cap = cv2.VideoCapture(input_path)
    # Finding the number of frames
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    print ("No of frames is : ", video_length)
    count = 0
    print ("Converting video file......\n")
    # converting the video
    while cap.isOpened():
        # Extracting the frames
        ret, frame = cap.read()
        if not ret:
            continue
        # Write the results back to output location.
        cv2.imwrite(output_path + "/%#05d.jpg" % (count+1), frame)
        count = count + 1
        # check for no additional frames
        if (count > (video_length-1)):
            time_end = time.time()
            cap.release()
            print ("Finished extracting frames.\n%d frames extracted" % count)
            print ("It took %d seconds for conversion of frames." % (time_end-time_start))
            break

if __name__=="__main__":

    input_path = 'output.mp4'
    output_path = 'frames'
    video_to_frames(input_path, output_path)
    
'''alternate code for reading the files <without color threshold
reading images and saving to images[] list

mypath=r"frames"
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
images = numpy.empty(len(onlyfiles), dtype=object)
for n in range(0, len(onlyfiles)):
  images[n] = cv2.imread( join(mypath,onlyfiles[n]) )'''

filenames = [img for img in glob.glob("frames/*.jpg")]
filenames.sort() 
images = []     # this is the list where we store the images

for img in filenames:  # here we use thresholding for converting theimage to near rgb
    n= cv2.imread(img) # Note numpy.maximum and numpy.max are different 
    (B, G, R) = cv2.split(n)
    M = numpy.maximum(numpy.maximum(R, G), B)
    R[R < M] = 0
    G[G < M] = 0
    B[B < M] = 0
    n = cv2.merge([B, G, R])
    images.append(n)
#To display the converted thrshold image 
''' cv2.imshow('dst_rt', n)            
cv2.waitKey(1500)           
cv2.destroyAllWindows() '''

''' ----------- Finding the dominant color----------------'''

FPS = 31    # use this to set the rate of output data 
fpsClock = pygame.time.Clock()  #note: unit is not in frame per second
starttime = time.time()
n = b'\n'
for i in range(0, len(images)):
    
    myimg = images[i] # Get the ith image
    avg_color_per_row = numpy.mean(myimg, axis=(0))
    avg_color = numpy.mean(avg_color_per_row, axis=(0))

    b = round(avg_color[0])
    g = round(avg_color[1]) # remove the round function to get data in floats 
    r = round(avg_color[2]) #do not use abs function here 

    #print(" dominant colour = " , round(max(avg_color)))

    x = "x" # for blue
    y = "y" # for red
    z = "z" # for green

    if b > r and b > g:
        print("dominant color is blue = ", b)
        try:ser.write(b'1')
        except:print('error comport 2')
            
    elif r > b and r > g:
        print("dominant color is red = ", r)
        try:ser.write(b'0')
            #ser.write(n)
        except:print('error comport 2')
        
    elif g > r and g > b:
        print("dominant color is green = ",g)
        try:ser.write(b'z')
        except:print('error comport 2')

    fpsClock.tick(FPS)

# calculating time taken to run
# use this to adjust timing 
print("--- %s seconds ---" % (time.time() - starttime)) 

''' ----------------------------- removing folder ----------------------------'''

print("Removing Folder....")    #removing contents in frames dir 
    
folder = 'frames'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete the files %s. Reason: %s' % (file_path, e))

# removing the "frames" directory
dir_path = 'frames'
try:
    os.rmdir(dir_path)
    
except OSError as e:
    print("Error: %s : %s" % (dir_path, e.strerror))

print("Folder and file contents removed")    
print("<----------------End of Script--------------->")

""" note if stopping the code in the middle of a run you must delete the folder
manually for it to run properly or run the code two times """ 
