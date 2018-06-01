# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 16:52:32 2017

@author: Prell Lab
"""
import numpy as np
import sys
file_name = sys.argv[1]
f = open(file_name,'r')
x,y=np.loadtxt (f,
       unpack = True,
       delimiter = ',')

########## system arguments ###############
inputcharge = float (sys.argv[2])
inputbasemass = float (sys.argv[3])
inputsubmass = float (sys.argv[4])
########## system arguments ###############

avgmz=0
varmz=0
totarea = np.sum(y)
for i in range (0,len(y)):
    avgmz += x[i]*y[i]
avgmz = avgmz/totarea
avgtotmass = avgmz*inputcharge
avgtotsubunits = (avgtotmass - inputbasemass)/inputsubmass
for i in range (0,len(y)):
    varmz += (x[i]**2)*y[i]
varmz = varmz/totarea-avgmz**2
stdevmz = np.sqrt(varmz)
stdevlip = (inputcharge*stdevmz/inputsubmass)
avgtotsubunitsdis = str(avgtotsubunits)
stdevlipdis = str(stdevlip)
atsWord = 'the average total sub-units is '
stdevWord = 'with a stdev of '
atsWordfinal = atsWord + avgtotsubunitsdis
stdevWordfinal = stdevWord + stdevlipdis
print (atsWordfinal)
print (stdevWordfinal)