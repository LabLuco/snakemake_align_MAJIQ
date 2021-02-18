# Map paired end data to genome hg38 version
# Alignment software : STAR
import os
import glob
import subprocess

def align(scriptdir,genomedir,namelist):
    for name in namelist :
        id = name.split('/')[-2]
        outfileprefix = scriptdir+'/../../results/alignment/'+id+'/'+id+'_'
        fwd = name+'*1.fq.gz'
        rev = name+'*2.fq.gz'
        # starcommand = 'STAR --runThreadN 3 --genomeDir '+genomedir+' --outFileNamePrefix '+outfileprefix+' --readFilesIn '+fwd+' '+rev+' --readFilesCommand zcat --outSAMtype BAM SortedByCoordinate'
        starcommand = 'STAR --runThreadN 10 --genomeDir '+genomedir+' --outFileNamePrefix '+outfileprefix+' --readFilesIn '+fwd+' '+rev+' --readFilesCommand zcat'
        subprocess.run((starcommand),stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True,shell=True)

if __name__ == "__main__":
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    # genomedir = scriptdir+'../../resources/human_genome/'
    genomedir = scriptdir+'/../../resources/genome/'
    namelist = glob.glob(scriptdir+'/../../results/trim_galore/*/')

    align(scriptdir,genomedir,namelist)