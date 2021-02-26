rule majiq_build:
    params:
        control = config['Control'],
        test = config['Test'],
        gff3 = config['Gff3'],
        genomename = config['Genome'],
        nbrep = config['NbMaxRep']
    input:
        expand('../../results/alignment/{id}/{id}_Aligned.out.sorted.bam', id = config['Samplesid']),
        expand('../../results/alignment/{id}/{id}_Aligned.out.sorted.bam.bai', id = config['Samplesid'])
    output:
        directory(expand('../../results/MAJIQ/build_{control}_{test}/', control=config['Control'], test=config['Test']))
    shell:
        """
        python3 ./../scripts/write_MAJIQ_configfile.py -g {params.genomename} -control {params.control} -test {params.test}
        majiq build {params.gff3} -c ../../resources/MAJIQ_conf/settings.ini -j 4 -o ../../results/MAJIQ/build_{params.control}_{params.test}/ --min-experiments {params.nbrep}
        """