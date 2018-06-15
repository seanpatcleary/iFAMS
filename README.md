# iFAMS
iFAMS, or interactive Fourier Analysis for Mass Spectrometry, is the Prell lab's home built deconvolution algorithm for heterogenous mass populations

I am currently in the process of uploading the program to github.  Check back in the next upcoming weeks for updates! I expect to have a fully fuctioning GUI, as well as source code that can be run without the GUI if you'd prefer and familiar with python (I find it to be much faster this way)

iFAMS uses the QT (PyQt5 to be exact) to run its GUI.  Ergo, without this module in your python site packages, you can not use the GUI.  This is simple to install from windows.  Open a command prompt (open start, search for command prompt if you don't know how to this) and type in, "pip install PyQt5". It should automatically install from there.  Elsewise, you will need the standards, such as numpy and scipy.  If an error pops up that says, "ModuleNotFoundError: No module named "module name", this means you're missing one such module, and should be able to install much in the same way I just described for PyQt5.  Any other issues, feel free to contact me, and we'll see if we can figure out what is wrong.

# Manual Version

iFAMS Manual Run Instructions

This version of iFAMS contains no GUI, in case you would like to run the program from, say, a command prompt.  You will need python version 3 run this.

These three scripts will do everything EXCEPT calculate the charge states and sub-unit mass.  Reason being, this would be rather awkward to do without a graphical interface.  If you've worked with the GUI, the program chooses points in the graph to calculate these, so without the graph, it might be kind of awkward to keep running the program to eventually get what you want. You can calculate the charge states manually much in the same way you do a mass spectrum though, remembering that each peak in the Fourier Spectrum is a charge state divided by the sub-unit mass (z/sub-unit mass).

I've attached three different scripts, 1. A script that will Fourier Transform a mass spectrum 2. One that will Inverse Fourier transform the FT data to get the individual charge state distributions, and 3. One that will calculate the statistics on the individual charge state distributions.

1.	For the Fourier Transform script, there are three inputs.  

-i (input): This is required, which is the name of the data file that you wish to Fourier Transform

-d (domain, optional, default = “abs”) This is optional in case you want the real Fourier spectrum instead of the absolute (absolute is the default, so if this is what you want, you won’t have to input this). Type “real” for real data.

-p (plot, optional, default = “no”) This is optional if you want the data plotted.  The default is no, so you don’t need to type this in if you want it plotted elsewhere.  It plots in MatPlotlib.

To run this script, open a command prompt, and make sure that the data that is being FT’d is in the same directory as the script.  Change to the directory where the script/file is stored, and type the command, 

"python    iFAMS_Fourier_Transform.py   -i test.txt" 

This would be the command to Fourier Transform that test file included on my github page.  Important to note that the data needs to be a .txt file, and the m/z values need to be in the first column (abundance in the 2nd).  It will automatically export the Fourier Spectra as a CSV file.


2.	For the inverse Fourier Transform script, you'll need 3 inputs

-i (input) This is required, which is the name of the data file that you wish to do the full analysis on.  To be clear, this the file that hasn’t been Fourier transformed.  This is NOT the Fourier transformed one.

-sm (subunit mass) This is required, and it is the sub-unit mass.  

-cs (charge states) This is required, and it is the charge states you wish to use.  You’ll need to input with brackets around the full list, and use commas to separate the different charge states.  

 As an example, if you wanted to do the full analysis on the test file using a subunit mass of 678 and charge states 12-15+, you would type:

 "python     iFAMS_Inverse_Fourier_Transform.py     test.txt     678     [12,13,14,15]"


3. For the statistical calculator script, you will need 4 arguments.  The name of the IFFT file, the charge state, the base mass, and the sub-unit mass, in that order.  All of these besides the name of the file are floats.  An example of this would be:

"python      iFAMS_statistical_calculator testIFFT12.csv      12      49320      678" 

this time, it will print the info in the command line.  If there isn't a base mass, just type zero for that.

If you have any questions, feel free to contact me, and I’ll be happy to help!!
