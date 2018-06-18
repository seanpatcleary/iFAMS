import numpy as np
import sys
import ast
import argparse
from scipy import interpolate as interpolate
import matplotlib.pyplot as plt
import os


chargestatesr=[]
###### system arguments ################
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="name of the file")
ap.add_argument("-sm", "--subunit_mass", required=True, help="The mass of the subunit")
ap.add_argument("-cs", "--charge_states", required=True, help="the charge states")
ap.add_argument("-p", "--plot", default = "no", help="would you like the data plotted?")
ap.add_argument("-d", "--domain", default = "abs", help="would you like real or absolute values. Default is Absolute,"
                                                        "type real for real values")
args = vars(ap.parse_args())

submass= float(args["subunit_mass"])
chargestatesr= ast.literal_eval(args["charge_states"]) #the charge states
file_name = args["input"]
###### system arguments ################


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
if args["domain"] == "real":
    ABFT=np.real(FT)
if args["domain"] == "abs":
    ABFT=np.absolute(FT)
ftspacing = maxfreq/(np.size(yfull)-1)
chargestateints = [int(chargestatesr[i]) for i in range(0,len(chargestatesr))]

omegafinal = expandedspan/ submass * 2
ABIFT = []
ABIFTmax = []
ABIFTmaxfinal = 0
ABIFTintegral = 0
msintegral = sum(y)
for i in range(0, len(chargestatesr)):
    freqmax = (chargestatesr[i] + 1 / 2) * omegafinal
    freqmin = (chargestatesr[i] - 1 / 2) * omegafinal
    condition = np.logical_and((ftx/ ftspacing) > freqmin, (ftx / ftspacing) < freqmax)
    csdata = np.extract(condition, FT)  # extracts the FFT data from the FFT spectrum that are within 1/2
    # the peak spacing of each maximum
    extlen = np.size(csdata)
    leftzeroes = np.ceil(freqmin)
    rightzeroes = np.size(FT) - extlen - leftzeroes
    paddedcsdata = np.lib.pad(csdata, (np.int_(leftzeroes), np.int_(rightzeroes)), 'constant', constant_values=(0, 0))
    IFT = np.fft.ifft(paddedcsdata)
    if args["domain"] == "real":
        ABIFT.append(np.real(IFT[int((len(IFT)) / 2):]))
    if args["domain"] == "abs":
        ABIFT.append(abs(IFT[int((len(IFT)) / 2):]))


############### Normalization of the IFFT Data ##########################
if args["domain"] == "abs":
    for i in range(0, len(chargestatesr)):
        ABIFTmax.append(max(ABIFT[i]))

    ABIFTmaxfinal = max(ABIFTmax)

    for i in range(0, len(chargestatesr)):
        for j in range(0, len(ABIFT[i])):
            ABIFT[i][j] = ABIFT[i][j] / ABIFTmaxfinal

    for i in range(0, len(chargestatesr)):
        ABIFTintegral += sum(ABIFT[i])
    for i in range(0, len(chargestatesr)):
        for j in range(0, len(ABIFT[i])):
            ABIFT[i][j] = ABIFT[i][j] / ABIFTintegral * msintegral

if args["domain"] == "real":
    for i in range(0, len(chargestatesr)):
        ABIFTmax.append(max(ABIFT[i]))

    ABIFTmaxfinal = max(ABIFTmax)

    for i in range(0, len(chargestatesr)):
        for j in range(0, len(ABIFT[i])):
            ABIFT[i][j] = ABIFT[i][j] / ABIFTmaxfinal

    for i in range(0, len(chargestatesr)):
        for j in range(0, len(ABIFT[i])):
            if ABIFT[i][j] >= 0:
                ABIFTintegral += ABIFT[i][j]
            else:
                ABIFTintegral += 0
    for i in range(0, len(chargestatesr)):
        for j in range(0, len(ABIFT[i])):
            ABIFT[i][j] = ABIFT[i][j] / ABIFTintegral * msintegral/2





    ############### Normalization of the IFFT Data ##########################

for i in range (0, len(chargestateints)):
    ifftfilename = 0
    iftstring = "IFFT"
    ifftfilename = namebase + iftstring + str(chargestateints[i]) + ".csv"
    ifftforexport = 0
    ifftforexport = np.transpose([xnew,ABIFT[i][0:int(len(xnew))]])
    np.savetxt(ifftfilename,ifftforexport,fmt='%10.6f', delimiter=',') #outputs each charge-state-specific spectrum to its own csv file
    print("file was exported")

if args["plot"] == "yes":
    plt.plot(x,y,color='k')
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'b', 'g', 'r', 'c', 'm', 'y', 'k', 'b', 'g', 'r', 'c', 'm', 'y', 'k',
              'b', 'g', 'r', 'c', 'm', 'y', 'k', 'b', 'g', 'r', 'c', 'm', 'y', 'k']
    for i in range(0, len(chargestateints)):
        plt.plot(xnew, ABIFT[i][0:int(len(xnew))],label=chargestateints[i],color = colors[i])
    plt.legend(loc='upper right', title='Charge State')
    plt.show()
