# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 15:16:02 2017

@author: Prell Lab
"""

import sys
import numpy as np
import argparse
from scipy import interpolate as interpolate
import matplotlib.pyplot as plt
import os


#################### system arguments ##########################
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="name of the file")
ap.add_argument("-d", "--domain", default = "abs", help="would you like real or absolute values. Default is Absolute,"
                                                        "type real for real values")
ap.add_argument("-p", "--plot", default = "no", help="would you like the data plotted?")
args = vars(ap.parse_args())
#################### system arguments ##########################

file_name = args["input"]
f = open(file_name,'r')
x,y=np.loadtxt (f,
       unpack = True,
       delimiter = '\t')



namebase = os.path.splitext(file_name)[0]
datainterpolation = interpolate.InterpolatedUnivariateSpline(x, y, k=3)
xnew = np.linspace(np.min(x), np.max(x), np.size(x), endpoint=True) #number of equally-spaced m/z values is equal to
# number of m/z values in original data
ynew = datainterpolation(xnew)
next2power = np.ceil(np.log2(len(ynew)))
newpadding = pow(2,next2power)-len(ynew)
paddedynew = np.pad(ynew,(0,np.int_(newpadding)),'constant',constant_values=(0,0))
paddedxnew = np.pad(xnew,(0,np.int_(newpadding)),'constant',constant_values=(0,0))                     
span = np.max(x)-np.min(x) #m/z span of mass spec
expandedspan = span + newpadding/len(ynew)*span
temp = np.array(paddedynew)
yflip = np.fliplr([temp])[0]
np.append(yflip,paddedynew)
yfull = np.append(yflip,paddedynew)
maxfreq = np.size(yfull)/expandedspan/2
ftx = np.linspace(0, maxfreq, np.size(yfull), endpoint=True)
FT = np.fft.fft(yfull)
if args["domain"] == "real":
    ABFT=np.real(FT)
    print ("working")
else:
    ABFT=np.absolute(FT)

ftstring = "FT"
ftfilename = namebase + ftstring + ".csv"
ftarrayforexport = np.transpose([ftx,ABFT])

np.savetxt(ftfilename,ftarrayforexport,fmt='%10.6f',delimiter=',')#outputs the FFT data to its own file
print ("your file was Fourier transformed and the data was exported")
if args["plot"] == "yes":
    plt.plot(ftx,ABFT)
    plt.show()
