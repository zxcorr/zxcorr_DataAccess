from astropy.table import Table, join, hstack,vstack,QTable
from esutil import htm
import numpy as np
import random
import sys
import os



def ver_file(path,filename):
    'Function to verify a file in a directory'
    path = os.path.join(path,filename)
    return os.path.isfile(path)
    

def match(cat_1, cat_2, column_1, column_2, column_3, column_4,error):
    'Function to make the matching with two tables, using the esutil'
    h = htm.HTM(depth=10)
    m1, m2, d12 = h.match(np.array(cat_1[column_1]), 
                          np.array(cat_1[column_3]),
                          np.array(cat_2[column_2]), 
                          np.array(cat_2[column_4]),
                          error, maxmatch=1)
    
    submatched = cat_1[m1]
    manmatched = cat_2[m2]
    matched = hstack([submatched, manmatched])
      
    return matched
def add_randomcol(cat):
    """Input: 
    cat: DataFrame
    Output:
    DataFrame with a random column
    """
    cat['random'] = 1.5
    return cat

def joinTables(path,dest):
    '''Functio to read a variety of tables and then join into one'''
    tables = []
    for i,filename in enumerate(os.listdir(path)):
        tables.append(Table.read(os.path.join(path,filename)))
    table = vstack(tables)
    table.write(dest,overwrite = 'yes')
    return table
def joinTables1(path,dest):
    'Same as before, using if the previous does not work'
    tables = []
    for i,filename in enumerate(os.listdir(path)):
        df = Table.read(os.path.join(path,filename)).to_pandas()
        tables.append(df)
    match = pd.concat(tabels, axis=0, ignore_index=True)
    del l
    del df
    match = QTable.from_pandas(match)
    match.write(dest)
