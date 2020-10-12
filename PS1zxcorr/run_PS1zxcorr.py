#############################################################################################################
# This code was created by Alessandro Marins (University of Sao Paulo) and is owned by BINGO Telescope
#
# Its use is to extract optical data from Pan-STARRS1 telescope
#
# Any question about your operation, please, contact me in alessandro.marins@usp.br
#############################################################################################################

import os,sys
import argparse
import numpy as np
import healpy as hp
import query as qr
import galaxies_pixel as gal
import flags as fl
import strips as st
import write_read_fits as wr
import maxnside as mx
import file_verification as ver
from time import time,strftime, gmtime

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

user            = config.get(       "General","user_ps1")
pwd             = config.get(       "General","pwd_ps1")
nside           = config.getint(    "General","nside")
nside_max       = config.getint(    "General","nside_max")
restart         = config.getboolean("General","restart")

use_constraint  = config.getboolean("Constraint","use")
type_constraint = config.get(       "Constraint","type")
band_constraint = config.get(       "Constraint","band")

use_flags       = config.getboolean("Flags","use")
table_flags     = config.getint(    "Flags","table")
band_flags      = config.get(       "Flags","band")
hex_flags       = config.get(       "Flags","hexadecimal")

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

parser.add_argument('--user_ps1'       , action = 'store', dest = 'user'           , default = user           , help = '')
parser.add_argument('--pwd_ps1'        , action = 'store', dest = 'pwd'            , default = pwd            , help = '')
parser.add_argument('--nside'          , action = 'store', dest = 'nside'          , default = nside          , help = '')
parser.add_argument('--nside_max'      , action = 'store', dest = 'nside_max'      , default = nside_max      , help = '')
parser.add_argument('--restart'        , action = 'store', dest = 'restart'        , default = restart        , help = '')

parser.add_argument('--use_constraint' , action = 'store', dest = 'use_constraint' , default = use_constraint , help = '')
parser.add_argument('--type_constraint', action = 'store', dest = 'type_constraint', default = type_constraint, help = '')
parser.add_argument('--band_constraint', action = 'store', dest = 'band_constraint', default = band_constraint, help = '')

parser.add_argument('--use_flags'      , action = 'store', dest = 'use_flags'      , default = use_flags      , help = '')
parser.add_argument('--table_flags'    , action = 'store', dest = 'table_flags'    , default = table_flags    , help = '')
parser.add_argument('--band_flags'     , action = 'store', dest = 'band_flags'     , default = band_flags     , help = '')
parser.add_argument('--hex_flags'      , action = 'store', dest = 'hex_flags'      , default = hex_flags      , help = '')

parser.add_argument('--use_declination_strips' , action = 'store', dest = 'dec_strips'     , default = dec_strips     , help = '')
parser.add_argument('--declination_center'     , action = 'store', dest = 'dec_center'     , default = dec_center     , help = '')
parser.add_argument('--declination_width'      , action = 'store', dest = 'dec_width'      , default = dec_width      , help = '')

parser.add_argument('--divide'  , action = 'store', dest = 'divide'  , default = divide  , help = '')
parser.add_argument('--Nparts'  , action = 'store', dest = 'Nparts'  , default = Nparts  , help = '')
parser.add_argument('--part'    , action = 'store', dest = 'part'    , default = part    , help = '')

###############################################################################
#Variables
###############################################################################
arguments = parser.parse_args()

user            = str(arguments.user)
pwd             = str(arguments.pwd)
nside           = int(arguments.nside)
nside_max       = int(arguments.nside_max)
restart         = bool(arguments.restart)

use_constraint  = bool(arguments.use_constraint)
type_constraint = str(arguments.type_constraint)
band_constraint = str(arguments.band_constraint)

use_flags       = bool(arguments.use_flags)
table_flags     = int(arguments.table_flags)
band_flags      = str(arguments.band_flags)
hex_flags       = int(arguments.hex_flags,16)

dec_strips      = bool(arguments.dec_strips)
dec_center      = float(arguments.dec_center)
dec_width       = float(arguments.dec_width)

divide          = bool(arguments.divide)
Nparts          = int(arguments.Nparts)
part            = int(arguments.part)

###############################################################################
# inputs
###############################################################################

NSIDE          = 2**nside
NSIDEmax       = 2**nside_max
constraints    = {"use":use_constraint, "type":type_constraint, "band": band_constraint} 
params_flags   = {"use":use_flags, "table":table_flags, "band":band_flags}
params_strips  = {'dec strips':dec_strips,'dec center':dec_center,'dec width':dec_width}
hexa_query     = hex_flags
divideSKYrange = {"divide":divide,"Nparts":Nparts,"part":part}

del use_constraint, type_constraint, band_constraint, use_flags, table_flags,band_flags, dec_strips,dec_center, dec_width, hex_flags, part, Nparts, divide
###############################################################################
# Access PS1 server
###############################################################################

try: # Python 3.x
    from urllib.parse import quote as urlencode
    from urllib.request import urlretrieve
except ImportError:  # Python 2.x
    from urllib import pathname2url as urlencode
    from urllib import urlretrieve

try: # Python 3.x
    import http.client as httplib 
except ImportError:  # Python 2.x
    import httplib

import getpass
if not os.environ.get('CASJOBS_WSID'):
    os.environ['CASJOBS_WSID'] = user
if not os.environ.get('CASJOBS_PW'):
    os.environ['CASJOBS_PW'] = pwd

###############################################################################
# The program start here
###############################################################################

print("----> Starting PS1zxcorr code <----\n")
print("Calculating the maximum resolution that does not cause problems for your connection...")

NPIX                   = hp.nside2npix(NSIDE)
params                 = {"NSIDE":NSIDE, "NPIX":NPIX}
params["NSIDE max"]    = NSIDEmax
params_strips['NSIDE'] = params['NSIDE']

print("Maximum resolution is NSIDE: {}\n".format(params['NSIDE max']))
print("You'll use")
print("NSIDE      : {} (2**{})".format(params['NSIDE'],nside))
print("Num. Pixels: {}".format(params['NPIX']))

strips = st.pixelstrips(params_strips) if params_strips['dec strips'] else np.arange(params['NPIX'])
len_strips = len(strips)
del nside, nside_max
if not restart:
	last   = ver.lastpix(NSIDE,"last")
	if last:
		strips = st.newtrips(strips,last)
	else: pass	
len_strips = len(strips)

print("It will be {:.2f}% of the sky covered.\n".format(100*float(len_strips)/params['NPIX']))

if divideSKYrange["divide"]:
	import fraction_sky_range as fsr
	print("Fractioning the range and taking the part {0}/{1}".format(divideSKYrange['part'],divideSKYrange['Nparts']))
	strips = fsr.divideSKY(divideSKYrange,strips)

print("\n\n")
time0 = time()
for num,pix in enumerate(strips):
	try:
		timei     = time()
		theta,phi = hp.pix2ang(params['NSIDE'],pix, lonlat=True, nest=False)
		
		params['pixel'] = pix
		
		if not ver.exist_or_not_file(params,restart):
			print(ver.exist_or_not_file(params,restart))
			tab, job        = qr.query_function(params, constraints)
			tab             = gal.galaxies_pixel(tab,params)
			tab             = fl.flags_constraints(tab,hexa_query,params_flags)
			
			timef           = strftime('%H:%M:%S', gmtime(time()-timei))
			
			print("Program's time (hh:mm:ss): {}".format(timef))
			print("Pixel {}".format(pix))
			print("{:.2f}% completed program".format(100*(float(num+1)/len_strips)))
			
			if len(tab)>0: wr.write_fits(tab,params)
			else: print("Not save. 0 galaxies")
			
			print("\n\n")
	
	except KeyboardInterrupt:
		sys.exit(0)
	
	except Exception as exc:
		print("Error pixel")
		str_nside = str(params["NSIDE"])
		str_pix   = str(pix)
		path = os.getcwd()
		path = os.path.join(path,"ERRORS")
		filename = ".".join(("_".join((str_nside,str_pix)),"err"))
		ver.file_verification(path,filename,str_nside)
		path = os.path.join(path,str_nside,filename)
		err = str(sys.exc_info()[0])
		f = open(path,"w+")
		f.write(err)
		f.write("\n")
		f.write(str(exc))
		f.close() 
print("End Programm: {0}".format(time0-time()))
