rule majiq_build:
    params:
        exp1 = config['Exp1'],
        exp2 = config['Exp2'],
        gff3 = config['Gff3'],
        genomename = config['Genome']
    input:
        # settings = '../../resources/MAJIQ_conf/settings.ini',
        bamsorted = expand('../../results/alignment/{id}/{id}_Aligned.out.sorted.bam.bai', id = config['Samplesid'])
    output:
        directory(expand('../../results/MAJIQ/build_{exp1}_{exp2}/', exp1=config['Exp1'], exp2=config['Exp2']))
    shell:
        """
        python3 ./../scripts/write_MAJIQ_configfile.py -g {params.genomename}
        majiq build {params.gff3} -c ../../resources/MAJIQ_conf/settings.ini -j 4 -o ../../results/MAJIQ/build_{params.exp1}_{params.exp2}/
        """