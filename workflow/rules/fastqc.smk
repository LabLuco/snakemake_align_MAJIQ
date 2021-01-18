rule fastqc:
    params:
        id1 = lambda wildcards : list(config['Samples'][config['Exp1']].values()),
        id2 = lambda wildcards : list(config['Samples'][config['Exp2']].values())
    input:
        expand("{id1}", id1 = ','.join(config['Samples'][config['Exp1']].values())),
        expand("{id2}", id2 = ','.join(config['Samples'][config['Exp2']].values()))
    output:
        expand("../../results/FastQC/{id1}_fastqc.zip", id1 = list(config['Samples'][config['Exp1']].values())),
        expand("../../results/FastQC/{id2}_fastqc.zip", id2 = list(config['Samples'][config['Exp2']].values()))
    shell:
        """
        echo "FastQC on {{id1}} data" &&\
        fastqc --extract --threads 24 --outdir ../../results/FastQC/ {params.id1}
        echo "FastQC on {{id2}} data" &&\
        fastqc --extract --threads 24 --outdir ../../results/FastQC/ {params.id2}
        """