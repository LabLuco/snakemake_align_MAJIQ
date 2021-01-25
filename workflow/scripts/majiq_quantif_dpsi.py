# Run DeltaPSI quantification between the two different experiments
# Software : MAJIQ
import os
import glob
import subprocess

def deltapsi(scriptdir,majiqlist):
    outputdir = scriptdir+'/../../results/MAJIQ/dPSI_'+snakemake.params[0]+'_'+snakemake.params[1]+'/'

    grp1list = []
    grp2list = []
    for i in majiqlist :
        if snakemake.params[0] in i :
            grp1list.append(i)
        if snakemake.params[1] in i :
            grp2list.append(i)
    
    grp1list = ' '.join(grp1list)
    grp2list = ' '.join(grp2list)

    print(grp1list)
    print(grp2list)

    dpsicommand = '~/test_majiq/bin/majiq deltapsi --default-prior -grp1 '+grp1list+' -grp2 '+grp2list+' -j 4 -o'+outputdir+' -n '+snakemake.params[0]+' '+snakemake.params[1]
    dpsirun = subprocess.Popen(dpsicommand, shell=True, stdout=subprocess.PIPE)
    dpsirun.communicate()

if __name__ == "__main__":
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    majiqlist = glob.glob(scriptdir+'/../../results/MAJIQ/build_'+snakemake.params[0]+'_'+snakemake.params[1]+'/*.majiq')

    deltapsi(scriptdir,majiqlist)