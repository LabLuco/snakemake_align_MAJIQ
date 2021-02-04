rule tpmcalculator:
    params:
        id = config['Samplesid'],
        gtf = config['Gtf']
    input:
        bamlist = expand('../../results/alignment/{id}/{id}_Aligned.out.sorted.bam', id = config['Samplesid'])
    output:
        directory(expand('../../results/TPM/{id}/',id = config['Samplesid']))
    script:
        "../scripts/tpmcalculator.py"