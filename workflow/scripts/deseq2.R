setwd("./../../results/Diff_Exp/")

library(BiocGenerics, lib.loc='/usr/lib/R/library')
library(S4Vectors, lib.loc='/usr/lib/R/library')
library(DESeq2, lib.loc='/usr/lib/R/library')

sampletable <- read.table("samplesheet.tsv", header=T, sep="\t")
rownames(sampletable) <- sampletable$sample_name

tx2gene <- read.table("tx2gene.tsv",sep="\t",header=F)

# Option 1 that reads in a matrix (we will not do it here):

	# first read in the matrix
count_matrix <- read.delim("raw_counts_matrix.tsv", header=T, sep="\t", row.names=1)
# then create the DESeq object
    # countData is the matrix containing the counts
    # sampletable is the sample sheet / metadata we created
    # design is how we wish to model the data: what we want to measure here is the difference between the treatment times
se_star_matrix <- DESeqDataSetFromMatrix(countData = count_matrix,
                                  colData = sampletable,
                                  design = ~ condition)
se_star2 <- DESeq(se_star_matrix)

# normalized = TRUE: divide the counts by the size factors calculated by the DESeq function
norm_counts <- log2(counts(se_star2, normalized = TRUE)+1)

# add the gene symbols
norm_counts_symbols <- merge(unique(tx2gene[,2:3]), data.frame(ID=rownames(norm_counts), norm_counts), by=1, all=F)

# write normalized counts to text file
write.table(norm_counts_symbols, "normalized_counts.tsv", quote=F, col.names=T, row.names=F, sep="\t")

###### VISUALIZATION ######
vsd <- vst(se_star2,nsub=1)

### samples correlation ###
library(pheatmap)
# calculate between-sample distance matrix
sampleDistMatrix <- as.matrix(dist(t(assay(vsd))))
png("sample_distance_heatmap_star.png")
  pheatmap(sampleDistMatrix)
dev.off()

### PCA ###
png("PCA_star.png")
plotPCA(object = vsd,intgroup = "condition")
dev.off()

###### Diff Exp Analysis ######
se_star2
se_star2$condition
se_star2$condition <- relevel(se_star2$condition, ref = "control")
se_star2$condition
se_star2 <- nbinomWaldTest(se_star2)
resultsNames(se_star2)

# contrast: the column from the metadata that is used for the grouping of the samples, then the baseline and the group compared to the baseline
de <- results(object = se_star2, 
		name="condition_test_vs_control")
# processing the same results as above but including the log2FoldChange shrinkage
        # useful for visualization and gene ranking
de_shrink <- lfcShrink(dds = se_star2,
                 coef="condition_test_vs_control",
		 type="apeglm")

# check first rows of both results
head(de)
head(de_shrink)

# add the more comprehensive gene symbols to de_shrink
de_symbols <- merge(unique(tx2gene[,2:3]), data.frame(ID=rownames(de_shrink), de_shrink), by=1, all=F)

# write differential expression analysis result to a text file
write.table(de_symbols, "deseq2_results.tsv", quote=F, col.names=T, row.names=F, sep="\t")