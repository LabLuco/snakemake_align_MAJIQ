# Write the config files to run MAJIQ Build :
# Need info in config.yaml -> Be sure to write the snakemake config file before runningthis script

import argparse
import os
import glob
import re
import yaml

def write_majiq_configfile(scriptdir,genome,control,test):
    bamlist = glob.glob(scriptdir+'/../../results/alignment/*/*_Aligned.out.sorted.bam')
    bamdirlist=[]
    for i, path in enumerate(bamlist):
        bamdirlist.append('/'.join(bamlist[i].split('/')[:-1])+'/')
    for i, bam in enumerate(bamlist) :
        bamlist[i] = bam.split('/')[-1].split('.bam')[0]
    bamdirlist = ','.join(bamdirlist)

    # exps = []
    # with open(scriptdir+'/../../config/config.yaml','r') as snakemakeconfig :
    #     lines = snakemakeconfig.read().splitlines()
    #     for line in lines :
    #         if re.search('Control: ', line) or  re.search('Test: ', line):
    #             exp = line.split(': ')[1]
    #             exps.append(exp)

    bamcontrol = []
    bamtest = []
    for id in bamlist :
        if re.match('^'+control+'_', id):
            bamcontrol.append(id)
        elif re.match('^'+test+'_', id) :
            bamtest.append(id)
    bamcontrol = ','.join(bamcontrol)
    bamtest = ','.join(bamtest)

    with open(scriptdir+'/../../resources/MAJIQ_conf/settings.ini','w') as file:
        file.write('[info]\n')
        file.write('bamdirs='+bamdirlist+'\n')
        file.write('genome='+genome+'\n')
        file.write('[experiments]\n')
        file.write(control+'='+bamcontrol+'\n')
        file.write(test+'='+bamtest)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", help="Name of genome used for mapping")
    parser.add_argument("-control", help="Name of control condition")
    parser.add_argument("-test", help="Name of test condition")

    args = parser.parse_args()

    scriptdir = os.path.dirname(os.path.realpath(__file__))

    write_majiq_configfile(scriptdir,args.g,args.control,args.test)