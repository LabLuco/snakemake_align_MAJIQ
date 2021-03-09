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

        paste ../../results/alignment/*/*_ReadsPerGene.out.tab | grep -v "_" | awk '{printf "%s\t", $1}{for (i=4;i<=NF;i+=4) printf "%s\t", $i; printf "\n" }' > ../../results/Diff_Exp/tmp
        sed -e "1igene_name\t$(ls ../../results/alignment/*/*_ReadsPerGene.out.tab | tr '\n' '\t' | sed 's/_ReadsPerGene.out.tab//g')" ../../results/Diff_Exp/tmp | cut -f1-7 > ../../results/Diff_Exp/raw_counts_matrix.tsv
        rm ../../results/Diff_Exp/tmp
        cat {params.gtf} | awk -F "\t" 'BEGIN{OFS="\t"}{if($3=="transcript"){split($9, a, "\""); print a[4],a[2],a[8]}}' > ../../results/Diff_Exp/tx2gene.tsv
        python3 ./../scripts/samplesheet_and_keep_gene_interest.py
        Rscript ./../scripts/deseq2.R
        """