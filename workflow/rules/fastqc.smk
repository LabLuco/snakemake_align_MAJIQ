rule fastqc:
    params :
        id = lambda wildcards: config['samples'][wildcards.id]
    input:
        expand("../../resources/{id}.fastq.gz", id = config['samples'])
    output:
        expand("../../results/FastQC/{{id}}/{{id}}_fastqc.zip", id = config['samples'])
    shell:
        """
        echo "FastQC on {wildcards.id} data" &&\
        fastqc --extract --threads 24 --outdir ../../results/FastQC/{wildcards.id}/ {params.id}
        """