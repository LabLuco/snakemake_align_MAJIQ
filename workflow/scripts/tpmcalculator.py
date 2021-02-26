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

if __name__ == "__main__":
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    bamlist = glob.glob(scriptdir+'/../../results/alignment/*/*_Aligned.out.sorted.bam')

    tpmcalculator(scriptdir,bamlist)