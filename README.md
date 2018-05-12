# iFAMS
iFAMS, or interactive Fourier Analysis for mass spectra, is the Prell lab's home built deconvolution algorithm for heterogenous mass populations

I am currently in the process of uploading the program to github.  Check back in the next upcoming weeks for updates! I expect to have a fully fuctioning GUI, as well as source code that can be run without the GUI if you'd prefer and familiar with python (I find it to be much faster this way)

iFAMS uses the QT (PyQt5 to be exact) to run its GUI.  Ergo, without this module in your python site packages, you can not use the GUI.  This is simple to install from windows.  Open a command prompt (open start, search for command prompt if you don't know how to this) and type in, "pip install PyQt5". It should automatically install from there.  Elsewise, you will need the standards, such as numpy and scipy.  If an error pops up that says, "ModuleNotFoundError: No module named "module name", this means you're missing one such module, and should be able to install much in the same way I just described for PyQt5.  Any other issues, feel free to contact me, and we'll see if we can figure out what is wrong.
