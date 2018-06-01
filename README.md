# iFAMS
iFAMS, or interactive Fourier Analysis for Mass Spectrometry, is the Prell lab's home built deconvolution algorithm for heterogenous mass populations

I am currently in the process of uploading the program to github.  Check back in the next upcoming weeks for updates! I expect to have a fully fuctioning GUI, as well as source code that can be run without the GUI if you'd prefer and familiar with python (I find it to be much faster this way)

iFAMS uses the QT (PyQt5 to be exact) to run its GUI.  Ergo, without this module in your python site packages, you can not use the GUI.  This is simple to install from windows.  Open a command prompt (open start, search for command prompt if you don't know how to this) and type in, "pip install PyQt5". It should automatically install from there.  Elsewise, you will need the standards, such as numpy and scipy.  If an error pops up that says, "ModuleNotFoundError: No module named "module name", this means you're missing one such module, and should be able to install much in the same way I just described for PyQt5.  Any other issues, feel free to contact me, and we'll see if we can figure out what is wrong.

# Manual Version

iFAMS Manual Run Instructions

This version of iFAMS contains no GUI, in case you would like to run the program from, say, a command prompt.  You will need python version 3 run this.

These three scripts will do everything EXCEPT calculate the charge states and sub-unit mass.  Reason being, this would be rather awkward to do without a graphical interface.  If you've worked with the GUI, the program chooses points in the graph to calculate these, so without the graph, it might be kind of awkward to keep running the program to eventually get what you want. You can calculate the charge states manually much in the same way you do a mass spectrum though, remembering that each peak in the Fourier Spectrum is a charge state divided by the sub-unit mass (z/sub-unit mass).

I've attached three different scripts, 1. A script that will Fourier Transform a mass spectrum 2. One that will Inverse Fourier transform the FT data to get the individual charge state distributions, and 3. One that will calculate the statistics on the individual charge state distributions.

For the Fourier Transform one, all you need to do is run the script from a command prompt while using the file that contains the mass spec data as an argument.  So, for example, 

"python    iFAMS_Fourier_Transform.py   test.txt" 

would be the command to Fourier Transform that test file I sent you.  It will automatically export the Fourier Spectra as a CSV file. I only have setup to read txt files for this, but you could update it to do more if you would like

For the inverse Fourier Transform script, you'll need to input 3 arguments.  The same file as the Fourier one, the sub-unit mass, and the charge states as a list, in that order. So for the test file, this would be,

 "python     iFAMS_Inverse_Fourier_Transform.py     test.txt     678     [12,13,14,15]"

 It will automatically export the inverse Fourier transforms as CSV files.

5. For the statistical calculator script, you will need 4 arguments.  The name of the IFFT file, the charge state, the base mass, and the sub-unit mass, in that order.  All of these besides the name of the file are floats.  An example of this would be:

"python      iFAMS_statistical_calculator testIFFT12.csv      12      49320      678" 

this time, it will print the info in the command line.  If there isn't a base mass, just type zero for that.

If you have any questions, feel free to contact me, and I’ll be happy to help!!
