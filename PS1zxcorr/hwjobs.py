import os,sys,subprocess,time
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
parser.add_argument( '--show', action = 'store', dest =  'show', default = False,   help = '')
parser.add_argument( '--user', action = 'store', dest =  'user', default = "amarins",   help = '')

###############################################################################
#Variables
###############################################################################
arguments = parser.parse_args()
show = int(arguments.show)
user = str(arguments.user)


###############################################################################
###############################################################################
def JOBrun(USER="amarins", jobRUN = "R"): #recebe o nome de um job (sbatch) rodando no SPLINTER e devolve o seu jobID.
        qstat_out, err = subprocess.Popen("qstat", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        qstat_out      = qstat_out.split("\n")
        qstat_out      = qstat_out[2:-1]
        count = 0
        jobnames = []
        jobids   = []
        jobtimes = []

        if len(err)==0:
                for i in range(len(qstat_out)):
                        qstat   = qstat_out[i].split()
                        jobid   = qstat[0] 
                        jobname = qstat[1] 
                        user    = qstat[2]
                        jobtime = qstat[3]
                        jobrun  = qstat[4]
                        if user == USER and jobrun == jobRUN:
							count+=1
							jobnames.append(jobname)
							jobids.append(jobid)
							jobtimes.append(jobtime)
							
                return int(count),np.asarray(jobnames),np.asarray(jobids),np.asarray(jobtimes)
###############################################################################
###############################################################################
count,jobnames,jobids,jobtimes = JOBrun(user,"R")

print("Jobs running: {}".format(count))

if show:
	for iname,ids,itimes in zip(jobnames,jobids,jobtimes):
		print(iname,ids,itimes)
		print("\n")
