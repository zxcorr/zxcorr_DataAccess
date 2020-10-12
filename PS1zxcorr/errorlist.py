import os,argparse

###############################################################################
#You can modify any options in the parameters.ini file by the command terminal
###############################################################################
parser = argparse.ArgumentParser()
parser.add_argument(      '--nside', action = 'store', dest =                 'nside', default = 64     , help = 'Nside of the directory')
parser.add_argument('--count_epixs', action = 'store', dest =     'count_errorpixels', default = "TRUE" , help = '')
parser.add_argument( '--list_epixs', action = 'store', dest =      'list_errorpixels', default = "FALSE", help = '')
parser.add_argument('--count_cpixs', action = 'store', dest = 'count_completedpixels', default = "TRUE" , help = '')
parser.add_argument( '--list_cpixs', action = 'store', dest =  'list_completedpixels', default = "FALSE", help = '')
parser.add_argument(  '--save_pixs', action = 'store', dest =           'save_pixels', default = "TRUE" , help = '')
###############################################################################
#Variables
###############################################################################
arguments = parser.parse_args()
nside  = int(arguments.nside)
list_epixs  = str(arguments.list_errorpixels)
count_epixs = str(arguments.count_errorpixels)
list_cpixs  = str(arguments.list_completedpixels)
count_cpixs = str(arguments.count_completedpixels)
save_pixs   = str(arguments.save_pixels)
###############################################################################
###############################################################################
path = os.getcwd()
path = os.path.join(path,"ERRORS",str(nside))

if count_epixs=="TRUE": print(" There are {0} error pixels.".format(len(os.listdir(path))))

files  = os.listdir(path)
files_ = []
for file_ in files:
    file_ = file_.split(".")[0]
    file_ = file_.split("_")[1]
    files_.append(file_)
files_ = np.asarray(files_,dtype=np.int).T

if list_epixs=="TRUE":
        print(files_)

if save_pixs=="TRUE":
    f = open("error_pixs.txt","w")
    f.close()
    np.savetxt("error_pixs.txt",list(files_), fmt="%i")
###############################################################################
###############################################################################
path = os.getcwd()
path = os.path.join(path,"FITS",str(nside))

if count_cpixs=="TRUE": print(" There are {0} completed pixels.".format(len(os.listdir(path))))

files  = os.listdir(path)
files_ = []
for file_ in files:
    file_ = file_.split(".")[0]
    file_ = file_.split("_")[-1]
    files_.append(file_)
files_ = np.asarray(files_,dtype=np.int).T
    
if list_cpixs =="TRUE":
        print(files_)
        
if save_pixs=="TRUE":
    f = open("completed_pixs.txt","w")
    f.close()
    np.savetxt("completed_pixs.txt",list(files_), fmt="%i")
