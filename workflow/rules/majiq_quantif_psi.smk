rule majiq_quantif_psi:
    params:
        exp1 = config['Exp1'],
        exp2 = config['Exp2']
    input:
        directory(expand('../../results/MAJIQ/build_{exp1}_{exp2}/', exp1=config['Exp1'], exp2=config['Exp2'])),
    output:
        directory(expand('../../results/MAJIQ/PSI_{exp1}/',exp1=config['Exp1'])),
        directory(expand('../../results/MAJIQ/PSI_{exp2}/',exp2=config['Exp2']))
    script:
        "../scripts/majiq_quantif_psi.py"