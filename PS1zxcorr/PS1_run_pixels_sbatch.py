import os,sys,subprocess,time
import argparse
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
parser.add_argument( '--spix', action = 'store', dest =  'spix', default = 1        ,   help = '')
parser.add_argument( '--epix', action = 'store', dest =  'epix', default = 10       ,  help = '')
parser.add_argument('--nside', action = 'store', dest = 'nside', default = 64       ,  help = '')
parser.add_argument('--user' , action = 'store', dest = 'user' , default = "amarins",  help = '')
###############################################################################
#Variables
###############################################################################
arguments = parser.parse_args()
spix   = int(arguments.spix)
epix   = int(arguments.epix)
nside  = int(arguments.nside)
user   = int(arguments.user)
###############################################################################
###############################################################################
path = "/".join(("/share/data1",user,"PS1zxcorr"))

path = os.path.join(path,"FITS",str(nside))
files  = os.listdir(path)
pixs = []
for file_ in files:
    file_ = file_.split(".")[0]
    file_ = file_.split("_")[-1]
    pixs.append(file_)
listp  = np.arange(spix,epix+1,1)
pixs   = np.sort(np.asarray(pixs,dtype=np.int))
ndpixs = np.setdiff1d(listp,pixs)
###############################################################################
###############################################################################
def reportERROR(jobNAME=None, err=None, text=None):
        import file_verification as ver
        path      = "/".join(("/share/data1",user,"PS1zxcorr"))
        directory = "ERRORS-jobs"
        filename  = "".join(("error",jobNAME,".err"))
        ver.file_verification(path,filename,directory)
        f = open(path,"w+")
        f.write(err)
        if text!=None:
                text = str(text)
                f.write(text)
        f.close()
        
def JOBID(USER="amarins", jobNAME = None): #recebe o nome de um job (sbatch) rodando no SPLINTER e devolve o seu jobID.
        qstat_out, err = subprocess.Popen("qstat", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        qstat_out      = qstat_out.split("\n")
        qstat_out      = qstat_out[2:-1]
        jobID          = []

        if len(err)==0:
                for i in range(len(qstat_out)):
                        qstat = qstat_out[i].split()
                        user  = qstat[2]
                        jobname = qstat[1]
                        if user == USER and jobname == jobNAME:
                                print(user,jobname)
                                jobID.append(qstat[0])
                return jobID
        else:
                reportERROR(jobNAME,err,None)
                return None

###############################################################################
###############################################################################
label = "sbatch_pixel"
jobs = ndpixs
for pix in jobs:
        job_sbatch = ".".join(("_".join((label,str(pix))),"sh"))
        if pix==jobs[0]:
                        jobNAME = "_".join(("PS1","pixel",str(pix)))
                        cmd     = " ".join(("sbatch",job_sbatch))
                        print(cmd)
                        job, err_job = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                        time.sleep(1)#2sec
                        ID      = JOBID(USER=user, jobNAME=jobNAME)
                        ID      = int(ID[0])
                        print(ID)
        else:
                        jobNAME = "_".join(("PS1","pixel",str(pix)))
                        cmd         = " ".join(("sbatch", "".join(("--depend=afterany:",str(ID))),job_sbatch))
                        print(cmd)
                        job, err_job = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                        time.sleep(1)#2sec
                        ID      = JOBID(USER=user, jobNAME=jobNAME)
                        ID      = int(ID[0])
                        print(ID)
