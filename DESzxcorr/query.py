import numpy as np
import healpy as hp
import os, sys, re
import json
from astropy.io import ascii, fits
from astropy.table import Table, join, hstack, vstack, QTable
import easyaccess as ea

def parameters(nside,pixel):
    radius = hp.pixelfunc.max_pixrad(nside,degrees=True)*3600
    angles = hp.pix2ang(nside,int(pixel),nest=False, lonlat=True)
    return angles , radius


# Não sei se é necessário
def fixcolnames(tab):
    """Fix column names returned by the casjobs query
    
    Parameters
    ----------
    tab (astropy.table.Table): Input table

    Returns reference to original table with column names modified"""

    pat = re.compile(r'\[(?P<name>[^[]+)\]')
    for c in tab.colnames:
        m = pat.match(c)
        if not m:
            raise ValueError("Unable to parse column name '{}'".format(c))
        newname = m.group('name')
        tab.rename_column(c,newname)
    return tab

def query_string(params):
        query = """
        SELECT
            *
        FROM
            dr1_main
        WHERE
            ( (CASE WHEN spread_model_i + 3.*spreaderr_model_i > 0.005 THEN 1 ELSE 0 END) +
            (CASE WHEN spread_model_i + 1.*spreaderr_model_i > 0.003 THEN 1 ELSE 0 END) +
            (CASE WHEN spread_model_i - 1.*spreaderr_model_i > 0.003 THEN 1 ELSE 0 END) ) = 3
            AND spread_model_i BETWEEN -0.05 AND 0.05
            AND imaflags_iso_i = 0
            AND hpix_"""+str(params['NSIDE'])+""" = """+str(params['pixel'])+"""
        """
        return query


def query_function(params):
    con = ea.connect('desdr')
    DF = con.query_to_pandas(query_string(params))
    DF = QTable.from_pandas(DF)
    return DF

def query_pix(params):

    query = """SELECT count(dr1.MAG_AUTO_I) COUNT,avg(dr1.MAG_AUTO_I) AVERAGE,dr1.HPIX_"""+str(params['NSIDE'])+"""
                FROM DR1_MAIN dr1
                where
                dr1.WAVG_SPREAD_MODEL_I + 3.0*dr1.WAVG_SPREADERR_MODEL_I > 0.005 and
                dr1.WAVG_SPREAD_MODEL_I + 1.0*dr1.WAVG_SPREADERR_MODEL_I > 0.003 and
                dr1.WAVG_SPREAD_MODEL_I - 1.0*dr1.WAVG_SPREADERR_MODEL_I > 0.001 and
                dr1.WAVG_SPREAD_MODEL_I > -1 and
                dr1.IMAFLAGS_ISO_I = 0 and
                dr1.MAG_AUTO_I < """+str(params['MAG'])+"""
                group by dr1.HPIX_"""+str(params['NSIDE'])+"""

            """
    con = ea.connect('desdr')
    DF = con.query_to_pandas(query)
    #DF = QTable.from_pandas(DF)
    np.savetxt('PIXELS/PixelList.txt',DF['HPIX_'+str(params['NSIDE'])],)
    return DF['HPIX_'+str(params['NSIDE'])] 