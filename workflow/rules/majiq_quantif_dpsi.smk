rule majiq_quantif_dpsi:
    params:
        control = config['Control'],
        test = config['Test'],
        nbrep = config['NbMaxRep']
    input:
        directory(expand('../../results/MAJIQ/build_{control}_{test}/', control=config['Control'], test=config['Test'])),
    output:
        directory(expand('../../results/MAJIQ/dPSI_{control}_{test}/', control=config['Control'], test=config['Test']))
    script:
        "../scripts/majiq_quantif_dpsi.py"