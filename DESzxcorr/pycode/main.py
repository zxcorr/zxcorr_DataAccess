import sys,os
from astropy.table import Table, join, hstack

import astroFunctions as astro

error = 0.00028
#path_new = sys.argv[3] 
#gama = Table.read(sys.argv[1])
#path_dir = sys.argv[2]

gama = Table.read('/home/rafael/Projetos/DESzxcorr/resultsOzDES_GRC_2018_12_07.fits')
path_dir = '/home/rafael/Projetos/DESzxcorr/FITS/64'
path_new = '/home/rafael/Projetos/DESzxcorr/results'


for i,filename in enumerate(os.listdir(path_dir)):
    #print(filename)
    name = 'match_' + filename # aux variable to test it exist the file
    #print(name) # in a directory
    if not astro.ver_file(path_new,name):# apply the test 
        file_ = Table.read(os.path.join(path_dir,filename))
        data = astro.match(gama, file_,'RA','RA','DEC','DEC',error)
        if len(data) != 0:
            data.add_column(1.5, name = 'random')
            for i in range(0, len(data)):
                data[i]['random'] = np.random.random()
    #if len(data['RA']) != 0:
        filename = 'match_' + filename
        data.write(os.path.join(path_new,filename))

t = astro.joinTables(path_new,'match.fits')
#astro.joinTables1(path_new,'match.fits')  #if the first function doesn't work


