# Get index BAI file from BAM mapping file for each sample
# Software : samtools
import os
import glob
import subprocess

def index(scriptdir,namelist):
    for name in namelist :
        newname = name[:-4]+'.sorted.bam'
        samtoolssort = 'samtools sort '+name+' > '+newname
        sort = subprocess.Popen(samtoolssort, shell=True, stdout=subprocess.PIPE)
        sort.communicate()

        sortedbam = newname
        samtoolsindex = 'samtools index -b '+newname
        index = subprocess.Popen(samtoolsindex, shell=True, stdout=subprocess.PIPE)
        index.communicate()

if __name__ == "__main__":
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    namelist = glob.glob(scriptdir+'/../../results/alignment/*/*_Aligned.out.sam')

    index(scriptdir,namelist)