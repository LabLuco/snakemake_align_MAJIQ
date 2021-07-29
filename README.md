# Snakemake workflow: snakemake_align_MAJIQ

[![Snakemake](https://img.shields.io/badge/snakemake-≥5.7.0-brightgreen.svg)](https://snakemake.bitbucket.io)

## Authors

* Elsa CLAUDE (https://github.com/ElsaClaude)

## About the pipeline

This is the snakemake pipeline in order to process RNAseq paired-end fastq files to analyze splicing events using MAJIQ software (https://majiq.biociphers.org/).
The pipeline involves use of :
* FastQC
* Trimgalore
* STAR alignment
* DESEQ2
* MAJIQ
* Voila software (link to MAJIQ results)

All of this is wrap in the pipeline using python/bash/R scripts. Check workflow/rules and workflow/scripts to better understand how it processed.

To be able to reproduce results, the pipeline have been included in a singularity container. See : https://github.com/LabLuco/build_singularity_MAJIQ

## Steps to run the pipeline
### 1. Pull img

Create a batch file to pull the img automatically.
Example on the genotoul bioinfo servers : 
```bash
#!/bin/bash
#SBATCH -J pull_img
#SBATCH -o pull_img.out
#SBATCH -e pull_img.out
#SBATCH -t 00:20:00
#SBATCH --mem=8G
module load system/singularity-3.0.1
cd /home/eclaude/work
singularity pull library://labluco/default/quality_align_majiq:latest
```

### 2. Prepare the data

Put your RNA-seq paire-end raw_data (fastq.gz) in a folder.
Same with an indexed genome with STAR. (check archive2/common/Elsa/ folder to get one)

### 3. Run the pipeline

Create a batch file to execute the singularity image to run the pipeline. Here is a minimal one.

```bash
#!/bin/bash
#SBATCH -t 03:00:00
#SBATCH --mem=20G
module load system/singularity-3.7.3
cd /home/eclaude/work
cp quality_align_majiq_latest.sif tmp_$1
mkdir $1
cd $1/
singularity run --bind $2:/softwares/snakemake_align_MAJIQ/resources/fastq --bind $3:/softwares/snakemake_align_MAJIQ/resources/genome ../tmp_$1
rm ../tmp_$1
```

This script allows you to :
* load the singularity module
* create a folder for the new analysis
* copy/paste the singularity img to be able to run multiple analysis in parallel
* run the singularity container with binded folders (raw data and genome)

The script needs arguments. The associated bash command line can be :

```bash
sbatch --error=name_test.err --output=name_test.err --job-name=name_test majiq.sh "name_test" "/home/eclaude/work/raw_data/" "/home/eclaude/work/genome/"
```
### 4. Get the results
All results will be stored in the newly created folder /snakemake_align_MAJIQ/results/.
Check the Clean_AS_Event folder for clean results files.

## Notes and warnings

The container copy all files to a path that can be modified. You can of course change that way of doing (which is really heavy) in the singularity building file (https://github.com/LabLuco/build_singularity_MAJIQ).

Unfortunatly, the pipeline has not been optimized to support single-end data. Some changes might be needed.
Also, some parameters might be pass by the user instead of being hard coded in the pipeline (check workflow/rules and workflow/scripts files) :
* number of thread to use (set to 10 for now in some scripts as STAR and MAJIQ analysis)

The pipeline is supposed to work on any servers. It only needs a recent version of singularity ( >= 3.7 if possible).
The pipeline has been used on the Genotoul Bioinfo servers. Tests have been made on the IGH Lakitu server but there are conflicts with the R libraries (they are aware of it, maybe it will be fixed ?)
