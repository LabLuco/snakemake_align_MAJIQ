# Execute TrimGalore v0.6.6 on paired end data given to the pipeline
import os
import glob
import subprocess

def execute_trim(rep,exp1,exp2,scriptdir):
    fastqlist = glob.glob(scriptdir+'/../../resources/fastq/*.fastq.gz')
    samples = {exp1 :{}, exp2:{}}
    for i in range(0,rep):
        samples[exp1]['REP'+str(i+1)] = []
        samples[exp2]['REP'+str(i+1)] = []

    for file in fastqlist :
        id = file.split('/')[-1].split('.')[0]
        condition = id.split('_')[0]

        for i in range(0,rep):
            if '_REP'+str(i+1)+'_' in id and id[-2:] in ['R1','R2']:
                samples[condition]['REP'+str(i+1)].append(file)

    for exp in samples.keys():
        print(exp)
        for namerep in samples[exp] :
            id = samples[exp][namerep][0].split('/')[-1].split('.')[0][:-3]
            print(samples[exp][namerep][0])
            if '_R1.f' in samples[exp][namerep][0] :
                fwd = samples[exp][namerep][0]
                rev = samples[exp][namerep][1]
            elif '_R2.f' in samples[exp][namerep][0] :
                fwd = samples[exp][namerep][1]
                rev = samples[exp][namerep][0]
            run = subprocess.Popen(('trim_galore --paired --fastqc --cores 4 --output_dir '+scriptdir+'/../../results/trim_galore/'+id+' '+fwd+' '+rev),shell=True, stdout=subprocess.PIPE)
            run.communicate()
if __name__ == "__main__":
    scriptdir = os.path.dirname(os.path.realpath(__file__))

    execute_trim(snakemake.params[0],snakemake.params[1],snakemake.params[2],scriptdir)