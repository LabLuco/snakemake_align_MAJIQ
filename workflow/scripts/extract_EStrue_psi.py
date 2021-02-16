# Extract LSVs ID with ES = TRUE in dpsi file (from MAJIQ dpsi) and concat all psi files (for all replicates per condition)
# Comparing the list to the Voila tsv file, to get only LSV with an ES junction
import os
import glob
import subprocess
import pandas

def findlsvES(dpsifile,psicond1,psicond2):
    dpsidf = pandas.read_csv(dpsifile, sep='\t', header=0)
    onlyES = dpsidf.loc[dpsidf['ES']==True]
    listlsv = onlyES['LSV ID']
    listlsv = pandas.DataFrame({'LSV ID':listlsv.values})

    for rep in psicond1 :
        lsvpsicond1 = pandas.read_csv(rep, sep='\t', header=0)
        listlsv = pandas.merge(listlsv,lsvpsicond1[['LSV ID']], how ='inner', on = ['LSV ID'])

    for rep in psicond1 :
        lsvpsicond2 = pandas.read_csv(rep, sep='\t', header=0)
        listlsv = pandas.merge(listlsv,lsvpsicond2[['LSV ID']], how ='inner', on = ['LSV ID'])

    return listlsv

def extractES(listlsv,dpsifile,voilafile):
    dpsidf = pandas.read_csv(dpsifile, sep='\t', header=0)
    voiladf = pandas.read_csv(voilafile, sep='\t', header=0, comment='#')
    substetvoila = voiladf.loc[voiladf['lsv_id'].isin(listlsv['LSV ID'])]

    merge = pandas.merge(substetvoila, dpsidf, how='left', left_on='lsv_id', right_on='LSV ID')
    merge = merge.drop(['gene_id', 'lsv_id', 'mean_dpsi_per_lsv_junction','probability_changing',
                'probability_non_changing', 'testunT5_mean_psi','testT5_mean_psi',
                'lsv_type', 'num_junctions', 'num_exons','de_novo_junctions', 'seqid',
                'junctions_coords','ir_coords','P(|dPSI|<=0.05) per LSV junction'], axis =1)
    cols = merge.columns.tolist()

    neworder = ['ucsc_lsv_link','gene_name','Gene ID','strand',
       'LSV ID', 'LSV Type', 'E(dPSI) per LSV junction',
       'P(|dPSI|>=0.20) per LSV junction', 'testunT5 E(PSI)', 'testT5 E(PSI)',
       'A5SS', 'A3SS', 'ES', 'Num. Junctions', 'Num. Exons',
       'Junctions coords','exons_coords','IR coords']
    merge = merge[neworder]

    newname = voilafile.split('.tsv')[0]+'.subsetES.tsv'
    merge.to_csv(newname,sep='\t', header=True, index=False)

def newpsifile(scriptdir,psicond1,psicond2,namecond1,namecond2,listlsv):
    psiconcat1 = pandas.DataFrame(listlsv, columns=['LSV ID'])
    psiconcat2 = pandas.DataFrame(listlsv, columns=['LSV ID'])
    psiconcat1 = concatpsifiles(scriptdir,psiconcat1,psicond1,namecond1)
    psiconcat2 = concatpsifiles(scriptdir,psiconcat2,psicond2,namecond2)
    
def concatpsifiles(scriptdir,dfconcat,psicond,namecond):
    print(psicond)
    for rep in psicond :
        namerep = os.path.basename(rep).split('.')[0]
        repdf = pandas.read_csv(rep, sep='\t', header=0)
        print('############## TEST PSI CONCAT ##############')
        print(repdf.columns)
        repdf.rename(columns = {'E(PSI) per LSV junction':namerep.upper()+' : E(PSI) per LSV junction','StDev(E(PSI)) per LSV junction': namerep.upper()+' : StDev(E(PSI)) per LSV junction'}, inplace = True)
        print(repdf.columns)
        dfconcat = pandas.merge(dfconcat, repdf[['LSV ID',namerep.upper()+' : E(PSI) per LSV junction',namerep.upper()+' : StDev(E(PSI)) per LSV junction']], how='left', on=['LSV ID'])
    
    print(dfconcat)
    outputdir = scriptdir+'/../../results/MAJIQ/'+namecond+'_PSI_concatenated/'
    mkdir = subprocess.Popen('mkdir '+outputdir, shell=True, stdout=subprocess.PIPE)
    mkdir.communicate()

    outname = namecond+'_PSI_all_rep.tsv'
    dfconcat.to_csv(outputdir+outname,sep='\t', header=True, index=False)

if __name__ == "__main__":
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    namecond1 = snakemake.params[0]
    namecond2 = snakemake.params[1]
    dpsifile = scriptdir+'/../../results/MAJIQ/dPSI_'+namecond1+'_'+namecond2+'/'+namecond1+'_'+namecond2+'.deltapsi.tsv'
    voilafile = scriptdir+'/../../results/Voila/'+namecond1+'_'+namecond2+'.tsv'

    psicond1 = glob.glob(scriptdir+'/../../results/MAJIQ/PSI_'+namecond1+'/*/*.psi.tsv')
    psicond2 = glob.glob(scriptdir+'/../../results/MAJIQ/PSI_'+namecond2+'/*/*.psi.tsv')

    listlsv = findlsvES(dpsifile,psicond1,psicond2)
    extractES(listlsv,dpsifile,voilafile)
    newpsifile(scriptdir,psicond1,psicond2,namecond1,namecond2,listlsv)
