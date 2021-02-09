# Run TPMCalculator on the various replicates of experiments
# Software : TPMCalculator
import os
import glob
import subprocess

def tpmcalculator(scriptdir,bamlist):
    outputdir = scriptdir+'/../../results/TPM/'

    for bam in bamlist :
        id = bam.split('/')[-2]
        tpmcommand = 'TPMCalculator -b '+bam+' -g '+snakemake.params[0]+' -q 255 -e'
        print(tpmcommand)
        tpm = subprocess.Popen(tpmcommand, shell=True, stdout=subprocess.PIPE)
        tpm.communicate()
        mkdircommand = 'mkdir '+outputdir+id+'/'
        mkdir = subprocess.Popen(mkdircommand, shell=True, stdout=subprocess.PIPE)
        mkdir.communicate()
        mvcommand = 'mv *sorted_* '+outputdir+id+'/'
        mv = subprocess.Popen(mvcommand, shell=True, stdout=subprocess.PIPE)
        mv.communicate()

    # grp1list = []
    # grp2list = []
    # for i in majiqlist :
    #     if snakemake.params[0] in i :
    #         grp1list.append(i)
    #     if snakemake.params[1] in i :
    #         grp2list.append(i)
    
    # grp1list = ' '.join(grp1list)
    # grp2list = ' '.join(grp2list)

    # print(grp1list)
    # print(grp2list)

    # dpsicommand = '~/test_majiq/bin/majiq deltapsi --default-prior -grp1 '+grp1list+' -grp2 '+grp2list+' -j 4 -o'+outputdir+' -n '+snakemake.params[0]+' '+snakemake.params[1]
    # dpsirun = subprocess.Popen(dpsicommand, shell=True, stdout=subprocess.PIPE)
    # dpsirun.communicate()

if __name__ == "__main__":
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    bamlist = glob.glob(scriptdir+'/../../results/alignment/*/*_Aligned.out.sorted.bam')

    tpmcalculator(scriptdir,bamlist)