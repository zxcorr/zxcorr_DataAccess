import os,argparse
import numpy as np
###############################################################################
#You can modify any options in the parameters.ini file by the command terminal
###############################################################################
parser = argparse.ArgumentParser()
parser.add_argument('--nside', action = 'store', dest = 'nside', default = 64     , help = 'Nside of the directory')
parser.add_argument( '--spix', action = 'store', dest =  'spix', default = 0 , help = '')
parser.add_argument( '--epix', action = 'store', dest =  'epix', default = 50, help = '')
###############################################################################
#Variables
###############################################################################
arguments = parser.parse_args()
nside = int(arguments.nside)
spix  = int(arguments.spix)
epix  = int(arguments.epix)
###############################################################################
###############################################################################
path = os.getcwd()
path = os.path.join(path,"FITS",str(nside))

files  = os.listdir(path)
pixs = []
for file_ in files:
    file_ = file_.split(".")[0]
    file_ = file_.split("_")[-1]
    pixs.append(file_)

listp  = np.arange(spix,epix+1)
pixs   = np.sort(np.asarray(pixs,dtype=np.int))

dpixs  = np.intersect1d(listp,pixs)
ndpixs = np.setdiff1d(listp,pixs)

#print("Pixels downloaded:")
#print(dpixs)
print("Pixels not downloaded:")
print(ndpixs)
