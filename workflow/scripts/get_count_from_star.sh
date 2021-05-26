#!/bin/bash
gtf=$1
paste ../../results/alignment/*/*_ReadsPerGene.out.tab | grep -v "_" | awk '{{printf "%s\t", $1}}{{for (i=4;i<=NF;i+=4) printf "%s\t", $i; printf "\n" }}' > ../../results/Diff_Exp/tmp
echo -n -e "gene_name\t" > ../../results/Diff_Exp/tmpheader| for file in ../../results/alignment/*/*_ReadsPerGene.out.tab; do basename $file _ReadsPerGene.out.tab | tr '\n' '\t' >> ../../results/Diff_Exp/tmpheader ; done
echo -n -e "\n" >> ../../results/Diff_Exp/tmpheader
sed -i -e '1 { r ../../results/Diff_Exp/tmpheader' -e 'N; }' ../../results/Diff_Exp/tmp
awk -F'\t' 'BEGIN { OFS = FS }; NF { NF -= 1}; 1' < ../../results/Diff_Exp/tmp > ../../results/Diff_Exp/tmp2
mv ../../results/Diff_Exp/tmp2 ../../results/Diff_Exp/raw_counts_matrix.tsv
rm ../../results/Diff_Exp/tmpheader
rm ../../results/Diff_Exp/tmp
rm ../../results/Diff_Exp/tmp2
cat ${gtf} | awk -F "\t" 'BEGIN{{OFS="\t"}}{{if($3=="transcript"){{split($9, a, "\""); print a[4],a[2],a[8]}}}}' > ../../results/Diff_Exp/tx2gene.tsv
