rule majiq_build:
    params:
        exp1 = config['Exp1'],
        exp2 = config['Exp2']
    input:
        gff = '../../resources/droso_melanogaster_genome/Drosophila_melanogaster.BDGP6.28.102.chr.gff3',
        settings = '../../resources/MAJIQ_conf/settings.ini',
        bamsorted = expand('../../results/alignment/{id}/{id}_Aligned.out.sorted.bam.bai', id = config['Samplesid'])
    output:
        directory(expand('../../results/MAJIQ/build_{exp1}_{exp2}/', exp1=config['Exp1'], exp2=config['Exp2']))
    shell:
        """
        source ~/test_majiq/bin/activate
        majiq build {input.gff} -c {input.settings} -j 4 -o ../../results/MAJIQ/build_{params.exp1}_{params.exp2}/
        """