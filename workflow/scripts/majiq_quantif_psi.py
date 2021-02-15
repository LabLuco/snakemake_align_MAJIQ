# Run PSI quantification between the two different experiments
# Software : MAJIQ
import os
import glob
import subprocess

def psi(scriptdir,majiqlist):
    outputdir1 = scriptdir+'/../../results/MAJIQ/PSI_'+snakemake.params[0]+'/'
    outputdir2 = scriptdir+'/../../results/MAJIQ/PSI_'+snakemake.params[1]+'/'

    # test1 = 'testT5'
    # test2 = 'testunT5'

    # outputdir1 = scriptdir+'/exMAJIQPSI/PSI_'+test1+'/'
    # outputdir2 = scriptdir+'/exMAJIQPSI/PSI_'+test2+'/'

    grp1list = []
    grp2list = []
    
    for i in majiqlist :
        if snakemake.params[0] in i.split('/')[-1] :
            grp1list.append(i)
        if snakemake.params[1] in i.split('/')[-1] :
            grp2list.append(i)

    # print(majiqlist)
    # for i in majiqlist :
    #     if test1 in i.split('/')[-1] :
    #         grp1list.append(i)
    #     if test2 in i.split('/')[-1] :
    #         grp2list.append(i)
    
    grp1list = ' '.join(grp1list)
    grp2list = ' '.join(grp2list)

    print(grp1list)
    # print(grp2list)

    # majiq = '/home/elsa/Documents/softs/env-majiq/bin/majiq'

    # psi1command = majiq+' psi '+grp1list+' -n '+test1+' -o'+outputdir1
    # psi1run = subprocess.Popen(psi1command, shell=True, stdout=subprocess.PIPE)
    # psi1run.communicate()

    # psi2command = majiq+' psi '+grp2list+' -n '+test2+' -o'+outputdir2
    # psi2run = subprocess.Popen(psi2command, shell=True, stdout=subprocess.PIPE)
    # psi2run.communicate()

    psi1command = 'majiq psi '+grp1list+' -n '+snakemake.params[0]+' -o'+outputdir1
    psi1run = subprocess.Popen(psi1command, shell=True, stdout=subprocess.PIPE)
    psi1run.communicate()

    psi2command = 'majiq psi '+grp2list+' -n '+snakemake.params[1]+' -o'+outputdir2
    psi2run = subprocess.Popen(psi2command, shell=True, stdout=subprocess.PIPE)
    psi2run.communicate()

if __name__ == "__main__":
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    majiqlist = glob.glob(scriptdir+'/../../results/MAJIQ/build_'+snakemake.params[0]+'_'+snakemake.params[1]+'/*.majiq')
    # majiqlist = glob.glob(scriptdir+'/test_results_MAJIQ/build_testunT5_testT5/*.majiq')

    psi(scriptdir,majiqlist)