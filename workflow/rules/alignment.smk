rule alignment:
    params:
        nbrep = config['NbRep'],
        exp1 = config['Exp1'],
        exp2 = config['Exp2']
    input:
        expand('../../results/trim_galore/{id}/*_val*', id = config['Samplesid'])
    output:
        expand('../../results/alignment/{id}/{id}_Aligned.out.sam', id = config['Samplesid'])
    script:
        "../scripts/alignment.py"