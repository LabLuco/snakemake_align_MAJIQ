rule trimgalore:
    params:
        nbrep = config['NbMaxRep'],
        control = config['Control'],
        test = config['Test']
    input:
        expand('../../resources/fastq/{idpaired}.fastq.gz', idpaired = config['Samplespaired'])
    output:
        expand('../../results/trim_galore/{id}/{id}_R1_val_1.fq.gz', id = config['Samplesid']),
        expand('../../results/trim_galore/{id}/{id}_R2_val_2.fq.gz', id = config['Samplesid'])
    script:
        "../scripts/trimgalore.py"