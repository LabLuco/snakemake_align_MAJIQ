rule voila_tsv:
    params:
        exp1 = config['Exp1'],
        exp2 = config['Exp2']
    input:
        directory(expand('../../results/MAJIQ/dPSI_{exp1}_{exp2}/', exp1=config['Exp1'], exp2=config['Exp2']))
    output:
        expand('../../results/Voila/{exp1}_{exp2}.tsv', exp1=config['Exp1'], exp2=config['Exp2'] )
    shell:
        """
        voila tsv ../../results/MAJIQ/build_{params.exp1}_{params.exp2}/splicegraph.sql ../../results/MAJIQ/dPSI_{params.exp1}_{params.exp2}/{params.exp1}_{params.exp2}.deltapsi.voila -f ../../results/Voila/{params.exp1}_{params.exp2}.tsv --threshold 0.00 --probability-threshold 0.00
        """