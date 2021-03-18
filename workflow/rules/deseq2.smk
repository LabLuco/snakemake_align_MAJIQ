rule deseq2:
    params:
        control = config['Control'],
        test = config['Test'],
        gtf = config['Gtf']
    input:
        expand('../../results/alignment/{id}/{id}_ReadsPerGene.out.tab', id = config['Samplesid']),
        expand('../../results/Voila/{control}_{test}.tsv', control=config['Control'], test=config['Test'] )
    output:
        '../../results/Diff_Exp/normalized_counts.tsv',
        '../../results/Diff_Exp/deseq2_results.tsv'
    shell:
        """
        mkdir -p ../../results/Diff_Exp/
        bash ../scripts/get_count_from_star.sh {params.gtf}
        python3 ./../scripts/samplesheet_and_keep_gene_interest.py
        Rscript ./../scripts/deseq2.R
        """