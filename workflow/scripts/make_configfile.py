# Write the config files to run the Snakemake pipeline :
#     - config.yaml to get variables in the Snakemake pipeline (such as path of input files)

import argparse
import os
import glob
import re
import yaml

def write_configsnakemake(scriptdir,fileabsdir,rep):
    fastqlist = glob.glob(fileabsdir+'/*.fastq.gz')
    index = {}

    for file in fastqlist :
        id = file.split('/')[-1].split('.')[0]
        namecheck = re.match("^.*_REP[0-9]_.*R[1-2].(fastq|fq).gz$", file.split('/')[-1])
        if bool(namecheck) == False :
            print('This file has a wrong name format and can not be taken for analysis : '+file)
            continue

        condition = id.split('_')[0]

        if condition not in index.keys():
            index[condition] = {}

        for i in range(0,rep):
            if 'REP'+str(i+1) not in index[condition].keys():
                index[condition]['REP'+str(i+1)] = []

        for i in range(0,rep):
            if '_REP'+str(i+1)+'_' in id and id[-2:] in ['R1','R2'] and len(index[condition]['REP'+str(i+1)]) < 3 :
                index[condition]['REP'+str(i+1)].append(file)

    with open(scriptdir+'/../../config/config.yaml', 'w') as outfile:
        outfile.write('NbRep: '+str(rep))
        outfile.write('\nExp1: '+ list(index.keys())[0])
        outfile.write('\nExp2: '+ list(index.keys())[1]+'\n')
        yaml.dump(index, outfile, default_flow_style=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-dir', help='Target directory containing paired-end raw fastq.gz files')
    parser.add_argument('-rep', help='Number of replicats',type=int)
    args = parser.parse_args()

    fileabsdir = os.path.abspath(args.dir)
    scriptdir = os.path.dirname(os.path.realpath(__file__))

    write_configsnakemake(scriptdir,fileabsdir,args.rep)