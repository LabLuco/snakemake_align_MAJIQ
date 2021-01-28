rule tpmcalculator:
    params:
        id = config['Samplesid']
    input:
        bamlist = expand('../../results/alignment/{id}/{id}_Aligned.out.sorted.bam', id = config['Samplesid']),
        gtf = '../../resources/chr1_human/Homo_sapiens.GRCh38.102.chr.gtf'
    output:
        directory(expand('../../results/TPM/{id}/',id = config['Samplesid']))
    script:
        "../scripts/tpmcalculator.py"