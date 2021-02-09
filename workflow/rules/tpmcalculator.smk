rule tpmcalculator:
    params:
        gtf = config['Gtf']
    input:
        expand('../../results/alignment/{id}/{id}_Aligned.out.sorted.bam', id = config['Samplesid']),
        expand('../../results/alignment/{id}/{id}_Aligned.out.sorted.bam.bai', id = config['Samplesid'])
    output:
        directory(expand('../../results/TPM/{id}/',id = config['Samplesid']))
    script:
        "../scripts/tpmcalculator.py"