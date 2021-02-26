rule majiq_quantif_psi:
    params:
        control = config['Control'],
        test = config['Test'],
        nbrep = config['NbMaxRep']
    input:
        directory(expand('../../results/MAJIQ/build_{control}_{test}/', control=config['Control'], test=config['Test'])),
    output:
        directory(expand('../../results/MAJIQ/PSI_{control}/',control=config['Control'])),
        directory(expand('../../results/MAJIQ/PSI_{test}/',test=config['Test']))
    script:
        "../scripts/majiq_quantif_psi.py"