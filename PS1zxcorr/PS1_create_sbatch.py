import os,sys
import argparse
import file_verification as ver

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
parser.add_argument('--Nparts', action = 'store', dest = 'Nparts', default = 2, help = '')
###############################################################################
#Variables
###############################################################################
arguments = parser.parse_args()
Nparts = int(arguments.Nparts)
###############################################################################
###############################################################################
ver.file_verification(os.getcwd(),"test","sbatch_files")
path = os.path.join(os.getcwd(),"sbatch_files/")

for i in range(Nparts):
	f = open("".join((path,"sbatch_",str(i+1),".sh")),"w+")
	f.write("#!/bin/bash -f\n\n")
	f.write("".join(("#SBATCH --job-name=PS1_",str(i+1),"\n")))
	f.write("".join(("#SBATCH -N1 -n1\n")))
	f.write("#SBATCH --mem=2G\n")
	f.write("#SBATCH -t 300:00:00\n")
	f.write("#SBATCH -p COMPUTE\n")
	f.write("".join(("#SBATCH -o /share/data1/amarins/output_files/file_",str(i+1),".out\n")))
	f.write("".join(("#SBATCH -e /share/data1/amarins/output_files/errfile_",str(i+1),".err\n\n")))
	f.write("cd /share/data1/amarins/PS1zxcorr\n")
	f.write("eval \"$(/share/apps/anaconda/3-2019.07/bin/conda shell.bash hook)\"\n")
	f.write("conda activate /share/data1/amarins/env/\n")
	f.write("echo Time is `date`\n")
	f.write("echo Running on host `hostname`\n")
	f.write("echo Directory is `pwd`\n")
	f.write("echo This jobs runs on the following processors:\n")
	f.write("echo $SLURM_JOB_NODELIST\n")
	f.write("".join(("python run_PS1zxcorr.py --Nparts ",str(Nparts)," --part ",str(i+1),"\n\n")))
	f.write("echo Time is `date`\n")
	f.close()
	
