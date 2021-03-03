# Run PSI quantification between the two different experiments
# Software : MAJIQ
import os
import glob
import subprocess
import re

def psi(scriptdir,majiqlist):
    outputdir1 = scriptdir+'/../../results/MAJIQ/PSI_'+snakemake.params[0]+'/'
    outputdir2 = scriptdir+'/../../results/MAJIQ/PSI_'+snakemake.params[1]+'/'

    controllist = []
    testlist = []
    
    for i in majiqlist :
        if re.match('^'+snakemake.params[0]+'_', i.split('/')[-1]):
            controllist.append(i)
        if re.match('^'+snakemake.params[1]+'_', i.split('/')[-1]):
            testlist.append(i)

    controllist = ' '.join(controllist)
    testlist = ' '.join(controllist)

    psi1command = 'majiq psi -o '+outputdir1+' -j 10 -n '+snakemake.params[0]+' --min-experiments '+str(snakemake.params[2])+' '+controllist
    psi1run = subprocess.Popen(psi1command, shell=True, stdout=subprocess.PIPE)
    psi1run.communicate()

    psi2command = 'majiq psi -o '+outputdir1+' -j 10 -n '+snakemake.params[1]+' --min-experiments '+(snakemake.params[2])+' '+testlist
    psi2run = subprocess.Popen(psi2command, shell=True, stdout=subprocess.PIPE)
    psi2run.communicate()

if __name__ == "__main__":
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    majiqlist = glob.glob(scriptdir+'/../../results/MAJIQ/build_'+snakemake.params[0]+'_'+snakemake.params[1]+'/*.majiq')

    psi(scriptdir,majiqlist)