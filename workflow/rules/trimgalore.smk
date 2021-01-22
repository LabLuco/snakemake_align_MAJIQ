rule trimgalore:
    params:
        nbrep = config['NbRep'],
        exp1 = config['Exp1'],
        exp2 = config['Exp2']
    input:
        expand('../../resources/fastq/{idpaired}.fastq.gz', idpaired = config['Samplespaired'])
    output:
        expand('../../results/trim_galore/{id}/*_val*', id = config['Samplesid'])
    script:
        "../scripts/trimgalore.py"