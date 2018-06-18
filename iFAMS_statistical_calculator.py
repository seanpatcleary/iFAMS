# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 16:52:32 2017

@author: Prell Lab
"""
import numpy as np
import sys
import argparse

########## system arguments ###############
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="name of the file")
ap.add_argument("-sm", "--subunitmass", required=True, help="the subunit mass")
ap.add_argument("-cs", "--charge_state", required=True, help="the charge state")
ap.add_argument("-bm", "--basemass", default = "0", help="The base mass")
args = vars(ap.parse_args())
########## system arguments ###############
file_name = args["input"]
f = open(file_name,'r')
x,y=np.loadtxt (f,
       unpack = True,
       delimiter = ',')
inputcharge = float(args["charge_state"])
inputsubmass = float(args["subunitmass"])
inputbasemass = float(args["basemass"])

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
