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

    ## psi per replicates
    for rep1 in controllist :
        rep1name = rep1.split('/')[-1].split('.')[0]
        psi1command = 'majiq psi '+rep1+' -n '+rep1name+' -o '+outputdir1+rep1name+'/'
        psi1run = subprocess.Popen(psi1command, shell=True, stdout=subprocess.PIPE)
        psi1run.communicate()

    for rep2 in testlist :
        rep2name = rep2.split('/')[-1].split('.')[0]
        psi2command = 'majiq psi '+rep2+' -n '+rep2name+' -o '+outputdir2+rep2name+'/'
        psi2run = subprocess.Popen(psi2command, shell=True, stdout=subprocess.PIPE)
        psi2run.communicate()

    controllist = ' '.join(controllist)
    testlist = ' '.join(testlist)

    ## Mean psi
    psi1command = 'majiq psi -o '+outputdir1+' -j 10 -n '+snakemake.params[0]+'_mean --min-experiments '+str(snakemake.params[2])+' '+controllist
    psi1run = subprocess.Popen(psi1command, shell=True, stdout=subprocess.PIPE)
    psi1run.communicate()

    psi2command = 'majiq psi -o '+outputdir2+' -j 10 -n '+snakemake.params[1]+'_mean --min-experiments '+str(snakemake.params[2])+' '+testlist
    psi2run = subprocess.Popen(psi2command, shell=True, stdout=subprocess.PIPE)
    psi2run.communicate()

if __name__ == "__main__":
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    majiqlist = glob.glob(scriptdir+'/../../results/MAJIQ/build_'+snakemake.params[0]+'_'+snakemake.params[1]+'/*.majiq')

    psi(scriptdir,majiqlist)