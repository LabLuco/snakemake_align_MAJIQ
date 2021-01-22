# Write the config files to run MAJIQ Build :
# Need info in config.yaml -> Be sure to write the snakemake config file before runningthis script

import argparse
import os
import glob
import re
import yaml

def write_majiq_configfile(scriptdir):
    bamlist = glob.glob(scriptdir+'/../../results/alignment/*/*_Aligned.out.sorted.bam')
    bamdirlist=[]
    for i, path in enumerate(bamlist):
        bamdirlist.append('/'.join(bamlist[i].split('/')[:-1])+'/')

    for i, bam in enumerate(bamlist) :
        bamlist[i] = bam.split('/')[-1].split('.bam')[0]

    bamdirlist = ','.join(bamdirlist)
    exps = []
    with open(scriptdir+'/../../config/config.yaml','r') as snakemakeconfig :
        lines = snakemakeconfig.read().splitlines()
        for line in lines :
            if re.search('Exp1: ', line) or  re.search('Exp2: ', line):
                exp = line.split(': ')[1]
                exps.append(exp)

    bamexp1 = []
    bamexp2 = []
    for id in bamlist :
        if exps[0] in id :
            bamexp1.append(id)
        elif exps[1] in id :
            bamexp2.append(id)
    bamexp1 = ','.join(bamexp1)
    bamexp2 = ','.join(bamexp2)

    with open(scriptdir+'/../../resources/MAJIQ_conf/settings.ini','w') as file:
        file.write('[info]\n')
        file.write('bamdirs='+bamdirlist+'\n')
        file.write('genome=hg38\n')
        file.write('[experiments]\n')
        file.write(exps[0]+'='+bamexp1+'\n')
        file.write(exps[1]+'='+bamexp2)

if __name__ == "__main__":
    scriptdir = os.path.dirname(os.path.realpath(__file__))

    write_majiq_configfile(scriptdir)