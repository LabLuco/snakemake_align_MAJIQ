import glob
import re
import pandas as pd

def write_samplesheet(scriptdir,totest):
    samples = {'sample_name':[],'condition':[]} 
    samplesfile = glob.glob(scriptdir+'/../../results/alignment/*/*_ReadsPerGene.out.tab')
    for file in samplesfile :
        samples['sample_name'].append(file.split('/')[-1].split('_ReadsPerGene.out.tab')[0])
        if 'control' in file.split('/')[-1].split('_ReadsPerGene.out.tab')[0] :
            samples['condition'].append('control')
        else :
            samples['condition'].append('test')
    samplesdf = pd.DataFrame.from_dict(samples)

    order = totest.columns.tolist()[1:]
    samplesdf=samplesdf.set_index(['sample_name']).reindex(order).reset_index()
    samplesdf.to_csv(scriptdir+'/../../results/Diff_Exp/samplesheet.tsv',header=1,sep='\t',index=False)

def extract_gene_interest(scriptdir,interest,totest):
    exist = ~totest['gene_name'].isin(interest['gene_id'])
    totest.drop(totest[exist].index, inplace = True)
    totest.to_csv(scriptdir+'/../../results/Diff_Exp/raw_counts_matrix.filtered.tsv',header=1,sep='\t',index=False)

if __name__ == "__main__":
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    interest = pd.read_csv(scriptdir+'/../../results/Voila/'+snakemake.params[0]+'_'+snakemake.params[1]+'.tsv',header=0,sep='\t',comment='#')
    totest = pd.read_csv(scriptdir+'/../../results/Diff_Exp/raw_counts_matrix.tsv',header=0,sep='\t')

    write_samplesheet(scriptdir,totest)
    extract_gene_interest(interest,totest)