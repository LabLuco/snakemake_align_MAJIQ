rule samtools_index:
    input:
        expand('../../results/alignment/{id}/{id}_Log.final.out', id = config['Samplesid'])
    output:
        expand('../../results/alignment/{id}/{id}_Aligned.out.sorted.bam', id = config['Samplesid']),
        expand('../../results/alignment/{id}/{id}_Aligned.out.sorted.bam.bai', id = config['Samplesid'])
    script:
        "../scripts/samtools_index.py"