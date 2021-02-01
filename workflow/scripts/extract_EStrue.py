# Extract LSVs ID with ES = TRUE in dpsi file (from MAJIQ dpsi)
# Comparing the list to the Voila tsv file, to get only LSV presenting an ES junction
import os
import glob
import subprocess
import pandas

def extractES(dpsifile):
    dpsidf = pandas.read_csv(dpsifile, sep='\t', header=0)
    onlyES = dpsidf.loc[dpsidf['ES']==True]
    listlsv = onlyES['LSV ID']
    return listlsv

def newdata(listlsv,voilafile,scriptdir):
    voiladf = pandas.read_csv(voilafile, sep='\t', header=0, comment='#')
    substetvoila = voiladf.loc[voiladf['lsv_id'].isin(listlsv)]

    newname = voilafile.split('.tsv')[0]+'.subsetES.tsv'
    substetvoila.to_csv(newname,sep='\t', header=True, index=False)

if __name__ == "__main__":
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    dpsifile = scriptdir+'/../../results/MAJIQ/dPSI_'+snakemake.params[0]+'_'+snakemake.params[1]+'/'+snakemake.params[0]+'_'+snakemake.params[1]+'.deltapsi.tsv'
    voilafile = scriptdir+'/../../results/Voila/'+snakemake.params[0]+'_'+snakemake.params[1]+'.tsv'

    listlsv = extractES(dpsifile)
    newdata(listlsv,voilafile,scriptdir)
