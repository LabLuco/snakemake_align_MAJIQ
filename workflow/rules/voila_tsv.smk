rule voila_tsv:
    params:
        control = config['Control'],
        test = config['Test']
    input:
        directory(expand('../../results/MAJIQ/dPSI_{control}_{test}/', control=config['Control'], test=config['Test']))
    output:
        expand('../../results/Voila/{control}_{test}.tsv', control=config['Control'], test=config['Test'] )
    shell:
        """
        voila tsv ../../results/MAJIQ/build_{params.control}_{params.test}/splicegraph.sql ../../results/MAJIQ/dPSI_{params.control}_{params.test}/{params.control}_{params.test}.deltapsi.voila -f ../../results/Voila/{params.control}_{params.test}.tsv --threshold 0.1 --probability-threshold 0.9
        """