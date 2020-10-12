import os,sys
import argparse
import file_verification as ver
import numpy as np
###################################################################
# Check the python version and import configparser
###################################################################
if sys.version_info[0]==2:
    import ConfigParser
    config = ConfigParser.RawConfigParser()
elif sys.version_info[0]==3:
    import configparser
    config = configparser.ConfigParser()
###############################################################################
#You can modify any options in the parameters.ini file by the command terminal
###############################################################################
parser = argparse.ArgumentParser()
parser.add_argument('--nside', action = 'store', dest = 'nside', default = 64, help = '')
parser.add_argument( '--spix', action = 'store', dest =  'spix', default = 1, help = '')
parser.add_argument( '--epix', action = 'store', dest =  'epix', default = 2, help = '')
###############################################################################
#Variables
###############################################################################
arguments = parser.parse_args()
nside        = int(arguments.nside)
spix = int(arguments.spix)
epix = int(arguments.epix)

###############################################################################
###############################################################################
#Select option between: newpixels and errorpixels #############################
###############################################################################
###############################################################################
if spix > -1 and epix > -1:
	pixs = np.arange(spix,epix+1,1)
	dirname = "sbatch_pixels_files/"
	ver.file_verification( os.getcwd(),"test",dirname)
	path    = os.path.join(os.getcwd(),dirname)
	os.system("rm -rf "+path+"*.sh")	
else:
	print("error")
	sys.exit(0)
###############################################################################
###############################################################################
###############################################################################

for pix in pixs:
	f = open("".join((path,"sbatch_pixel_",str(pix),".sh")),"w+")
	f.write("#!/bin/bash -f\n\n")
	f.write("".join(("#SBATCH --job-name=PS1_pixel_",str(pix),"\n")))
	f.write("".join(("#SBATCH -N1 -n1\n")))
	f.write("#SBATCH --mem=10G\n")
	f.write("#SBATCH -t 300:00:00\n")
	f.write("#SBATCH -p COMPUTE\n")
	f.write("#SBATCH -o /share/data1/amarins/output_files/file_error_{}.out\n".format(pix))
	f.write("#SBATCH -e /share/data1/amarins/output_files/errfile_error_{}.err\n\n".format(pix))
	f.write("cd /share/data1/amarins/PS1zxcorr\n")
	f.write("eval \"$(/share/apps/anaconda/3-2019.07/bin/conda shell.bash hook)\"\n")
	f.write("conda activate /share/data1/amarins/env/\n")
	f.write("echo Time is `date`\n")
	f.write("echo Running on host `hostname`\n")
	f.write("echo Directory is `pwd`\n")
	f.write("echo This jobs runs on the following processors:\n")
	f.write("echo $SLURM_JOB_NODELIST\n")
	f.write("python run_pixels_PS1zxcorr.py --pixels {}\n\n".format(pix))
	f.write("echo Time is `date`\n")
	f.close()
	
