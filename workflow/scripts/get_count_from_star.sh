#!/bin/bash
gtf=$1
paste ../../results/alignment/*/*_ReadsPerGene.out.tab | grep -v "_" | awk '{{printf "%s\t", $1}}{{for (i=4;i<=NF;i+=4) printf "%s\t", $i; printf "\n" }}' > ../../results/Diff_Exp/tmp
sed -e "1igene_name\t$(ls ../../results/alignment/*/*_ReadsPerGene.out.tab | tr '\n' '\t' | sed 's/_ReadsPerGene.out.tab//g')" ../../results/Diff_Exp/tmp | cut -f1-7 > ../../results/Diff_Exp/raw_counts_matrix.tsv
rm ../../results/Diff_Exp/tmp
cat ${gtf} | awk -F "\t" 'BEGIN{{OFS="\t"}}{{if($3=="transcript"){{split($9, a, "\""); print a[4],a[2],a[8]}}}}' > ../../results/Diff_Exp/tx2gene.tsv