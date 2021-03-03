# Run DeltaPSI quantification between the two different experiments
# Software : MAJIQ
import os
import glob
import subprocess
import re

def deltapsi(scriptdir,majiqlist):
    outputdir = scriptdir+'/../../results/MAJIQ/dPSI_'+snakemake.params[0]+'_'+snakemake.params[1]+'/'

    controllist = []
    testlist = []
    for i in majiqlist :
        if re.match('^'+snakemake.params[0]+'_', i.split('/')[-1]):
            controllist.append(i)
        elif re.match('^'+snakemake.params[1]+'_', i.split('/')[-1]) :
            testlist.append(i)
    
    controllist = ' '.join(controllist)
    testlist = ' '.join(testlist)

    dpsicommand = 'majiq deltapsi -grp1 '+testlist+' -grp2 '+controllist+' -j 10 --min-experiments '+str(snakemake.params[2])+' -o '+outputdir+' -n '+snakemake.params[1]+' '+snakemake.params[0]
    dpsirun = subprocess.Popen(dpsicommand, shell=True, stdout=subprocess.PIPE)
    dpsirun.communicate()

if __name__ == "__main__":
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    majiqlist = glob.glob(scriptdir+'/../../results/MAJIQ/build_'+snakemake.params[0]+'_'+snakemake.params[1]+'/*.majiq')

    deltapsi(scriptdir,majiqlist)