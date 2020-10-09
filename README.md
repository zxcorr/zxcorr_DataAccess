# DESzxcorr <a href="https://github.com/mgckind/easyaccess/blob/master/LICENSE.txt"><img src="https://img.shields.io/badge/license-NCSA%20License-blue.svg" alt="License" /> </a> <a href="https://pypi.python.org/pypi/easyaccess/1.4.7"><img src="https://img.shields.io/badge/pypi-v1.4.7-orange.svg" alt="pypi version"/></a> ![](https://img.shields.io/badge/python-2.7%7C3.6-blue.svg) [![DOI](http://joss.theoj.org/papers/10.21105/joss.01022/status.svg)](https://doi.org/10.21105/joss.01022)



This code was created by Alessandro Marins and Rafael M. Ribeiro(University of Sao Paulo) and is owned by BINGO Telescope. Its use is to extract optical data from DES telescope. Any question about your operation, please, contact us in alessandro.marins@usp.br and rafaelmgr@usp.br.

To use it, run run_DESzxcorr.py.

The variables and conditions are in parameters.ini. Any variable can be altered in terminal with "--" and the same name of the variable in parameter.ini plus underline and the name of class, except the General class, in this use it only variable name. All the letters in minuscule.

For example: python run_PS1Code.py --nside 1024 --use_constraint False --band_flags i --use_declination_strips False

You need to check if there are the Python libraries: numpy, healpy, sys, os, ConfigParser(python2) or configparser(python3), astropy, [easyacces](https://github.com/mgckind/easyaccess)*,[CX-Oracle](https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html) requests, re, json and argparse.




