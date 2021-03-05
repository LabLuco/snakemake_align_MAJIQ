import pandas
import numpy as np
import re

# LSV TYPE specified if it is about a target or a source exon such as : s|... or t|...
# LSV TYPE may be composed of various splicing events defined as : AeB.CoD
# LSV TYPE may contain an intro which is specified at the end such as : ...|i

def initdf(cond1,cond2):
    newdf = pandas.DataFrame(columns=['gene_name','gene_id','lsv_id',
            'mean_dpsi_per_lsv_junction','probability_changing',
            'probability_non_changing',cond1+'_mean_psi',
            cond2+'_mean_psi','de_novo_junctions',
            'strand','place_constitutive_exon','seqid','junctions_coords',
            'ES','A5SS','A3SS'])
    return newdf

def initdfIR(cond1,cond2):
    newdf = pandas.DataFrame(columns=['gene_name','gene_id','lsv_id',
            'mean_dpsi_per_lsv_junction','probability_changing',
            'probability_non_changing',cond1+'_mean_psi',
            cond2+'_mean_psi','de_novo_junctions',
            'strand','place_constitutive_exon','seqid',junctions_coords',
            'ir_coords','IR'])
    return newdf


def extract_events(voilatsv,cond1,cond2):
    fulldf = initdf(cond1,cond2)
    fulldfir = initdfIR(cond1,cond2)

    for index,row in voilatsv.iterrows():

        lsvtype = row['lsv_type']
        lsvsplit = lsvtype.split('|')
        target = lsvsplit[0]

        if 'na' in lsvsplit :
            continue

        if target == 't' :
            listB = []
            listC = []
            maxD = 1

            for event in lsvsplit :
                if event not in ['t','i']:
                    b = int(re.search('e(.*)\.',event).group(1))
                    listB.append(b)

                    d = int(re.search('o(.*)',event).group(1))
                    if d > maxD :
                        maxD = d

                    c = int(re.search('\.(.*)o',event).group(1))
                    listC.append(c)

            maxB = max(listB)

            for index in range (1,len(lsvsplit)) :
                if index == len(lsvsplit)-1 and lsvsplit[index] == 'i':
                    dfevent = initdfIR(cond1,cond2)
                    dfevent.loc[0,'ir_coords'] = row['ir_coords']
                    dfevent.loc[0,'IR'] = 'TRUE'
                else :
                    dfevent = initdf(cond1,cond2)
                    dfevent.loc[0,'ES'] = 'FALSE' # INIT VALUE
                    dfevent.loc[0,'A5SS'] = 'FALSE' # INIT VALUE
                    dfevent.loc[0,'A3SS'] = 'FALSE' # INIT VALUE

                dfevent.loc[0,'gene_name'] = row['gene_name']
                dfevent.loc[0,'gene_id'] = row['gene_id']
                dfevent.loc[0,'lsv_id'] = row['lsv_id']
                dfevent.loc[0,'mean_dpsi_per_lsv_junction'] = row['mean_dpsi_per_lsv_junction'].split(';')[index-1]
                dfevent.loc[0,'probability_changing'] = row['probability_changing'].split(';')[index-1]
                dfevent.loc[0,'probability_non_changing'] = row['probability_non_changing'].split(';')[index-1]
                dfevent.loc[0,cond1+'_mean_psi'] = row[cond1+'_mean_psi'].split(';')[index-1]
                dfevent.loc[0,cond2+'_mean_psi'] = row[cond2+'_mean_psi'].split(';')[index-1]
                dfevent.loc[0,'de_novo_junctions'] = row['de_novo_junctions'].split(';')[index-1] # A CHANGER EN BOOL PLUS TARD
                dfevent.loc[0,'strand'] = row['strand']
                dfevent.loc[0,'place_constitutive_exon'] = 'TARGET'
                dfevent.loc[0,'seqid'] = row['seqid']
                dfevent.loc[0,'junctions_coords'] = row['junctions_coords'].split(';')[index-1]

                if lsvsplit[index] != 'i':
                    a = int(re.search('^(.*)e',lsvsplit[index]).group(1))
                    b = int(re.search('e(.*)\.',lsvsplit[index]).group(1))
                    c = int(re.search('\.(.*)o',lsvsplit[index]).group(1))
                    d = int(re.search('o(.*)',lsvsplit[index]).group(1))

                    diffc = False
                    indexB = [i for i,value in enumerate(listB) if value==b]
                    for i in indexB :
                        if listC[i] != c :
                            diffc = True

                    if b != maxB :
                        dfevent.loc[0,'ES'] = 'TRUE'
                    if d != 1 and c != maxD and listB.count(b) > 1 and diffc == True :
                        dfevent.loc[0,'A5SS'] = 'TRUE'
                    if a != 1 :
                        dfevent.loc[0,'A3SS'] = 'TRUE'

                if index == len(lsvsplit)-1 and lsvsplit[index] == 'i':
                    fulldfir = pandas.concat([fulldfir,dfevent])
                else :
                    fulldf = pandas.concat([fulldf,dfevent])

        elif target == 's':
            maxA = 1
            listB = []
            listC = []

            for event in lsvsplit :
                if event not in ['s','i']:
                    a = int(re.search('(.*)e',event).group(1))
                    if a > maxA :
                        maxA = a

                    b = int(re.search('e(.*)\.',event).group(1))
                    listB.append(b)

                    c = int(re.search('\.(.*)o',event).group(1))
                    listC.append(c)

            for index in range (1,len(lsvsplit)) :
                if index == len(lsvsplit)-1 and lsvsplit[index] == 'i':
                    dfevent = initdfIR(cond1,cond2)
                    dfevent.loc[0,'ir_coords'] = row['ir_coords']
                    dfevent.loc[0,'IR'] = 'TRUE'
                else :
                    dfevent = initdf(cond1,cond2)
                    dfevent.loc[0,'ES'] = 'FALSE' # INIT VALUE
                    dfevent.loc[0,'A5SS'] = 'FALSE' # INIT VALUE
                    dfevent.loc[0,'A3SS'] = 'FALSE' # INIT VALUE

                dfevent.loc[0,'gene_name'] = row['gene_name']
                dfevent.loc[0,'gene_id'] = row['gene_id']
                dfevent.loc[0,'lsv_id'] = row['lsv_id']
                dfevent.loc[0,'mean_dpsi_per_lsv_junction'] = row['mean_dpsi_per_lsv_junction'].split(';')[index-1]
                dfevent.loc[0,'probability_changing'] = row['probability_changing'].split(';')[index-1]
                dfevent.loc[0,'probability_non_changing'] = row['probability_non_changing'].split(';')[index-1]
                dfevent.loc[0,cond1+'_mean_psi'] = row[cond1+'_mean_psi'].split(';')[index-1]
                dfevent.loc[0,cond2+'_mean_psi'] = row[cond2+'_mean_psi'].split(';')[index-1]
                dfevent.loc[0,'de_novo_junctions'] = row['de_novo_junctions'].split(';')[index-1] # A CHANGER EN BOOL PLUS TARD ?
                dfevent.loc[0,'strand'] = row['strand']
                dfevent.loc[0,'place_constitutive_exon'] = 'SOURCE'
                dfevent.loc[0,'seqid'] = row['seqid']
                dfevent.loc[0,'junctions_coords'] = row['junctions_coords'].split(';')[index-1]

                if lsvsplit[index] != 'i':
                    a = int(re.search('^(.*)e',lsvsplit[index]).group(1))
                    b = int(re.search('e(.*)\.',lsvsplit[index]).group(1))
                    c = int(re.search('\.(.*)o',lsvsplit[index]).group(1))
                    d = int(re.search('o(.*)',lsvsplit[index]).group(1))

                    diffc = False
                    indexB = [i for i,value in enumerate(listB) if value==b]
                    for i in indexB :
                        if listC[i] != c :
                            diffc = True

                    if b != 1 :
                        dfevent.loc[0,'ES'] = 'TRUE'
                    if a != maxA :
                        dfevent.loc[0,'A5SS'] = 'TRUE'
                    if d != 1 and c != 1 and listB.count(b) > 1 and diffc == True:
                        dfevent.loc[0,'A3SS'] = 'TRUE'

                if index == len(lsvsplit)-1 and lsvsplit[index] == 'i':
                    fulldfir = pandas.concat([fulldfir,dfevent])
                else :
                    fulldf = pandas.concat([fulldf,dfevent])
                    
    fulldf['junction_coords'] = fulldf[['seqid', 'junctions_coords']].agg(':'.join, axis=1)
    fulldfir['junction_coords'] = fulldfir[['seqid', 'junctions_coords']].agg(':'.join, axis=1)
    fulldf.drop(['seqid', 'junctions_coords'], axis=1)
    fulldfir.drop(['seqid', 'junctions_coords'], axis=1)
    return fulldf,fulldfir

def remove_low_dpsi_and_proba(fulldf,threshholddpsi,threshholdproba):
    fulldf['mean_dpsi_per_lsv_junction'] = fulldf['mean_dpsi_per_lsv_junction'].astype(float)
    fulldf['probability_changing'] = fulldf['probability_changing'].astype(float)
    fulldf = fulldf[fulldf['mean_dpsi_per_lsv_junction'].abs() > threshholddpsi]
    fulldf = fulldf[fulldf['probability_changing'] > threshholdproba]
    return fulldf

def remove_duplicates(df):
    df = (df.assign(abs=df['mean_dpsi_per_lsv_junction'].abs()).sort_values(['junction_coords','abs'],ascending=[True, True]).drop('abs', 1))
    df = df.drop_duplicates(subset=['gene_name', 'junction_coords'], keep='first')
    return df

def get_only_X_event(cond1,cond2,fulldf1,fulldf2,eventtype,outputdir):
    if eventtype == 'ES' :
        dfES1 = fulldf1[fulldf1['ES'] == 'TRUE']
        dfES1 = remove_duplicates(dfES1)
        dfES1.to_csv(outputdir+'ES/'+control+'_'+test+'_ES_01.tsv',header=1, sep='\t',index=False)

        dfES2 = fulldf2[fulldf2['ES'] == 'TRUE']
        dfES2 = remove_duplicates(dfES2)
        dfES2.to_csv(outputdir+'ES/'+control+'_'+test+'_ES_02.tsv',header=1, sep='\t',index=False)
    elif eventtype == 'A5SS' :
        dfA5SS1 = fulldf1[fulldf1['A5SS'] == 'TRUE']
        dfA5SS1 = remove_duplicates(dfA5SS1)
        dfA5SS1.to_csv(outputdir+'A5SS/'+control+'_'+test+'_A5SS_01.tsv',header=1, sep='\t',index=False)

        dfA5SS2 = fulldf2[fulldf2['A5SS'] == 'TRUE']
        dfA5SS2 = remove_duplicates(dfA5SS2)
        dfA5SS2.to_csv(outputdir+'A5SS/'+control+'_'+test+'_A5SS_02.tsv',header=1, sep='\t',index=False)
        
    elif eventtype == 'A3SS' :
        dfA3SS1 = fulldf1[fulldf1['A3SS'] == 'TRUE']
        dfA3SS1 = remove_duplicates(dfA3SS1)
        dfA3SS1.to_csv(outputdir+'A3SS/'+control+'_'+test+'_A3SS_01.tsv',header=1, sep='\t',index=False)

        dfA3SS2 = fulldf2[fulldf2['A3SS'] == 'TRUE']
        dfA3SS2 = remove_duplicates(dfA3SS2)
        dfA3SS2.to_csv(outputdir+'A3SS/'+control+'_'+test+'_A3SS_02.tsv',header=1, sep='\t',index=False)
        
    elif eventtype == 'IR' :
        dfIR1 = fulldf1[fulldf1['IR'] == 'TRUE']
        dfIR1 = remove_duplicates(dfIR1)
        dfIR1.to_csv(outputdir+'IR/'+control+'_'+test+'_IR_01.tsv',header=1, sep='\t',index=False)

        dfIR2 = fulldf2[fulldf2['IR'] == 'TRUE']
        dfIR2 = remove_duplicates(dfIR2)
        dfIR2.to_csv(outputdir+'IR/'+control+'_'+test+'_IR_02.tsv',header=1, sep='\t',index=False)

if __name__ == "__main__":
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    control = snakemake.params[0]
    test = snakemake.params[1]
    voilafile = scriptdir+'/../../results/Voila/'+control+'_'+test+'.tsv'
    voilatsv = pandas.read_csv(voilafile, header=0, comment='#', sep='\t')

    fulldf,fulldfir = extract_events(voilatsv,control,test)

    fulldf1 = remove_low_dpsi_and_proba(fulldf,0.1,0.9)
    fulldf2 = remove_low_dpsi_and_proba(fulldf,0.2,0.9)

    fulldfir1 = remove_low_dpsi_and_proba(fulldfir,0.1,0.9)
    fulldfir2 = remove_low_dpsi_and_proba(fulldfir,0.2,0.9)

    outputdir = scriptdir+'/../../results/Clean_AS_Event/'

    get_only_X_event(control,test,fulldf1,fulldf2,'ES',outputdir)
    get_only_X_event(control,test,fulldf1,fulldf2,'A5SS',outputdir)
    get_only_X_event(control,test,fulldf1,fulldf2,'A3SS',outputdir)

    get_only_X_event(control,test,fulldfir1,fulldfir2,'IR',outputdir)