# Write the config files to run the Snakemake pipeline :
#     - config.yaml to get variables in the Snakemake pipeline (such as path of input files)

import argparse
import os
import glob
import pandas as pd
import datetime

def write_configsnakemake(scriptdir,fileabsdir):
    fastqlist = glob.glob(fileabsdir+'/*.fastq.gz')
    index = {}
    for file in fastqlist :
        id = file.split('/')[-1].split('.')[0]
        index[id] = file

    configfile = open(scriptdir+'/../../config/config.yaml','w')
    configfile.write('samples:\n')
    for sample in index.keys():
        configfile.write("  "+sample+" : '"+index[sample]+"'\n")


    date = datetime.datetime.now().strftime("%Y_%m_%d_%Hh%Mm%Ss")
    configfile.write("date : '"+date+"'")

    configfile.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-dir', help='target directory containing tsv files')
    args = parser.parse_args()

    fileabsdir = os.path.abspath(args.dir)
    scriptdir = os.path.dirname(os.path.realpath(__file__))

    write_configsnakemake(scriptdir,fileabsdir)