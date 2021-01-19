rule trimgalore:
    params:
        nbrep = config['NbRep'],
        exp1 = config['Exp1'],
        exp2 = config['Exp2']
    input:
        expand('../../resources/fastq/{id}.fastq.gz', id = config['Samplespaired'])
    output:
        directory(expand('../../results/trim_galore/{name}/', name = config['Samplesname']))
    script:
        # "../scripts/exec_trimgalore.py -nbrep {{params.nbrep}} -exp1 {{params.exp1}} -exp2 {{params.exp2}}"
        "../scripts/exec_trimgalore.py"