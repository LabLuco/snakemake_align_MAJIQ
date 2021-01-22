# Write the config files to run the Snakemake pipeline :
#     - config.yaml to get variables in the Snakemake pipeline (such as path of input files)

import argparse
import os
import glob
import re
import yaml

def write_configsnakemake(scriptdir):
    fastqlist = glob.glob(scriptdir+'/../../resources/fastq/*.fastq.gz')
    conditionlist = []
    outfile = open(scriptdir+'/../../config/config.yaml', 'w')
    outfile.write('Samplespaired:\n')

    idlist=[]
    nbrep = []

    for file in fastqlist :
        id = file.split('/')[-1].split('.')[0]
        if id[:-3] not in idlist :
            idlist.append(id[:-3])
        namecheck = re.match("^.*_REP[0-9]_.*R[1-2].(fastq|fq).gz$", file.split('/')[-1])
        if bool(namecheck) == False :
            print('This file has a wrong name format and can not be taken for analysis : '+file)
            continue

        rep = re.search('_REP[0-9]_', id).group(0)
        if rep not in nbrep :
            nbrep.append(rep)

        condition = id.split('_')[0]
        if condition not in conditionlist:
            conditionlist.append(condition)
            if len(conditionlist)>2 :
                print('you have more than two conditions in your experiments. Please, re-consider your files.')
                continue
        outfile.write('    '+id+" : '"+file+"'\n")

    outfile.write('Samplesid:\n')
    for name in idlist :
        outfile.write('    - '+name+'\n')
    
    outfile.write('NbRep: '+str(len(nbrep))+'\n')
    outfile.write('Exp1: '+ conditionlist[0])
    outfile.write('\nExp2: '+ conditionlist[1]+'\n')

if __name__ == "__main__":
    scriptdir = os.path.dirname(os.path.realpath(__file__))

    write_configsnakemake(scriptdir)