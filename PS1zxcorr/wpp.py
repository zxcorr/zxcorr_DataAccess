#wpp = which part is the pixel?

import os,sys
import argparse
import numpy as np
import healpy as hp
import strips as st
import fraction_sky_range as fsr

###################################################################
# Check the python version and import configparser
###################################################################

if sys.version_info[0]==2:
    import ConfigParser
    config = ConfigParser.RawConfigParser()
	
elif sys.version_info[0]==3:
    import configparser
    config = configparser.ConfigParser()
	
###################################################################
# This part is for extracting information from parameters.ini file
###################################################################

name_params = os.path.join(os.getcwd(),"parameters.ini")
config.read(name_params)

nside           = config.getint(    "General","nside")

dec_strips      = config.getboolean("Strips","use_declination_strips")
dec_center      = config.getfloat(  "Strips","declination_center")
dec_width       = config.getfloat(  "Strips","declination_width")

divide          = config.getboolean("Divide_of_sky_range","divide")
Nparts          = config.getint(    "Divide_of_sky_range","Nparts")
part            = config.getint(    "Divide_of_sky_range","part")

###############################################################################
#You can modify any options in the parameters.ini file by the command terminal
###############################################################################

parser = argparse.ArgumentParser(description='Modify by the command terminal parameters in parameters.ini file')

parser.add_argument('--nside'          , action = 'store', dest = 'nside'          , default = nside          , help = '')

parser.add_argument('--use_declination_strips' , action = 'store', dest = 'dec_strips'     , default = dec_strips     , help = '')
parser.add_argument('--declination_center'     , action = 'store', dest = 'dec_center'     , default = dec_center     , help = '')
parser.add_argument('--declination_width'      , action = 'store', dest = 'dec_width'      , default = dec_width      , help = '')

parser.add_argument('--divide'  , action = 'store', dest = 'divide'  , default = divide  , help = '')
parser.add_argument('--Nparts'  , action = 'store', dest = 'Nparts'  , default = Nparts  , help = '')
parser.add_argument('--part'    , action = 'store', dest = 'part'    , default = part    , help = '')

parser.add_argument('--pixel'    , action = 'store', dest = 'pixel'    , default = 1    , help = '')

###############################################################################
#Variables
###############################################################################
arguments = parser.parse_args()

nside           = int(arguments.nside)

dec_strips      = bool(arguments.dec_strips)
dec_center      = float(arguments.dec_center)
dec_width       = float(arguments.dec_width)

divide          = bool(arguments.divide)
Nparts          = int(arguments.Nparts)
part            = int(arguments.part)

pixel           = int(arguments.pixel)

###############################################################################
# inputs
###############################################################################

NSIDE          = nside
params_strips  = {'dec strips':dec_strips,'dec center':dec_center,'dec width':dec_width}
divideSKYrange = {"divide":divide,"Nparts":Nparts,"part":part}

###############################################################################
# The program start here
###############################################################################

print("\n\n----> wpp = Whhich part is the pixel? <----\n")

NPIX                   = hp.nside2npix(NSIDE)
params                 = {"NSIDE":NSIDE, "NPIX":NPIX} 
params_strips['NSIDE'] = params['NSIDE']

for i in range(divideSKYrange['Nparts']):
	divideSKYrange['part']=i+1
	strips = st.pixelstrips(params_strips) if params_strips['dec strips'] else np.arange(params['NPIX'])
	strips = fsr.divideSKY(divideSKYrange,strips)
	wpp = bool(len(np.where((strips==pixel))[0]))
	if wpp==True:
		print("Part: {0}".format(divideSKYrange['part']))
		break

