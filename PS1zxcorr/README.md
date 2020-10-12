 ### This code was created by Alessandro Marins (University of Sao Paulo) and Filipe Abdalla (University College London) 
 ### and is owned by BINGO Telescope

 ### Its use is to extract optical data from Pan-STARRS1 telescope

 ### Any question about your operation, please, contact me in alessandro.marins@usp.br

## INSTALL
That code use python2.

It is necessary you have healpy (>=1.13), astropy (>=2.0.16), wheel, six python packages. Also, it is necessary you to install casjobs and mastcasjobs packages, both with 0.0.1 version. For these one, follow the steps below:

$ git clone http://github.com/rlwastro/mastcasjobs.git
$ pip install git+git://github.com/dfm/casjobs@master
$ cd mastcasjobs
$ git checkout 3c27f7ff7aff933694058b5204abd72527115244
$ python setup.py install --user

Check if you installed right. 

$ pip show casjobs
$ pip show mastcasjobs

It should show you that version is 0.0.1.

## Personal Computer
If you want only running the code in your personal computer you should do not worry with "PS1_" codes, that are by cluster running. Just choose between "part" or "pixels" method, adaptaded it in ".ini" file and run the "run_" respectively code (ps: all variables in "ini" file can be change on terminal). For example, running "pixel" method:

$ python run_pixels_PS1zxcorr.py 


## Cluster Computer
Here there are some codes for SPLINTER cluster (UCL's cluster). PS1_create_pixels_sbatch.py and PS1_create_sbatch.py codes will create the jobs files in another directory (sbatch_pixels_files and sbatch_files, respectively. If these one not exist, it will create.). The ".sh" files will be identified by your pixels or part number. You should put which pixel range you want. For example:

$ python PS1_create_pixels_sbatch.py --nside 64 --spix 0 --epix 10000

Ps: 0 <= spix <= epix <= 12*nside*2

It is necessary to adapt the lines 55, 56, 57, 58 and 59 for your directories and conda environment. See I created a output directory called by "output_files" for the terminal outputs.



After you to create files, you should copy the respective "PS1_run" to the directory. For example:

$ cp PS1_run_pixels_sbatch.py /sbatch_pixels_files
or
$ cp PS1_run_sbatch.py /sbatch_files

And move yourself to the same directory

$ cd sbatch_pixels_files
or
$ cd sbatch_files

In that, you can run one job and set N jobs on hold. For example, assume that the first is the pixel 300 and you want set 100 other jobs on hold. Then, you should do

$ python PS1_run_pixels_sbatch.py --spix 300 --epix 401


You can also want to check your jobs that are running. For that you can use hwjobs.py code.


## hwjobs.py
It is used in SPLINTER (UCL cluster) and it show jobs running with your username. To run just write in shell, for example

$ python hwjobs.py --show True --user amarins


## listepixs.py
This code list the pixels do not download in a pixel range at a specific nside (standard: 64). To use it just write, for example:

$ python listepixs.py --nside 1024 --spix 0 --epix 1000



There are two groups of codes that are differents for how will download fits file: with "_pixels_" word and without it. The codes with that one work separate the total sky range in (almost) equal number of pixels called "part". The group without that word work for each pixel, the user should give which pixels it want to download.
