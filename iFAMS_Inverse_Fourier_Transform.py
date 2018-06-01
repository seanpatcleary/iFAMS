# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 15:16:02 2017

@author: Prell Lab
"""

import numpy as np
import sys
import ast
from scipy import interpolate as interpolate
import os


chargestatesr=[]
###### system arguments ################

submass= float (sys.argv[2]) #the mass of the sub-unit
chargestatesr= ast.literal_eval( sys.argv[3] ) #the charge states

###### system arguments ################

file_name = sys.argv[1]
f = open(file_name,'r')
x,y=np.loadtxt (f,
       unpack = True,
       delimiter = '\t')



namebase = os.path.splitext(file_name)[0]
datainterpolation = interpolate.InterpolatedUnivariateSpline(x, y, k=3)
xnew = np.linspace(np.min(x), np.max(x), np.size(x), endpoint=True) #number of equally-spaced m/z values is equal to number of m/z values in original data
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
ABFT=np.absolute(FT)
ftspacing = maxfreq/(np.size(yfull)-1)
chargestateints = [int(chargestatesr[i]) for i in range(0,len(chargestatesr))] 

omegafinal = expandedspan/submass*2
msintegral = sum(i[0]*i[1] for i in zip(xnew,ynew))
ABIFTintegral = 0
sumchar  = 0

for i in chargestatesr:
    sumchar += i


ABIFT = []
numchar=len(chargestatesr)



for i in range(0,numchar):  
    freqmax = (chargestatesr[i]+1/2)*omegafinal
    freqmin = (chargestatesr[i]-1/2)*omegafinal
    condition = np.logical_and((ftx/ftspacing) > freqmin, (ftx/ftspacing) < freqmax)
    csdata = np.extract(condition,FT) #extracts the FFT data from the FFT spectrum that are within 1/2 the peak spacing of each maximum
    extlen = np.size(csdata)
    leftzeroes = np.ceil(freqmin)
    rightzeroes = np.size(FT)-extlen-leftzeroes
    paddedcsdata=np.lib.pad(csdata,(np.int_(leftzeroes),np.int_(rightzeroes)),'constant',constant_values=(0,0))
    IFT = np.fft.ifft(paddedcsdata)
    ABIFT.append(abs(IFT[int((len(IFT))/2):]))
#the contribution of each charge state to the mass spectrum here reflects the charge state itself (more closely-space peaks = more contribution) 
    ABIFTintegral += (sum(j[0]*j[1] for j in zip(paddedxnew,ABIFT[i])))

    
             
for i in range(0,numchar): #weight each charge-state-specific mass spectrum by its charge, with the total area = area of original mass spectrum

    xnewfornoise = []
    ABIFTplusnoise = []
    ABIFTminusnoise = []

    for j in range(0,len(ABIFT[i])):            
        
        ABIFT[i][j] = ABIFT[i][j]/ABIFTintegral*msintegral                
        

   
    ifftfilename = 0
    iftstring = "IFFT"
    ifftfilename = namebase + iftstring + str(chargestateints[i]) + ".csv"
    ifftforexport = 0
    ifftforexport = np.transpose([xnew,ABIFT[i][0:int(len(xnew))]])
    np.savetxt(ifftfilename,ifftforexport,fmt='%10.6f', delimiter=',') #outputs each charge-state-specific spectrum to its own csv file
    print("file was exported")
