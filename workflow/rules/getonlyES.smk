rule getonlyES:
    params:
        exp1 = config['Exp1'],
        exp2 = config['Exp2']
    input:
        expand('../../results/Voila/{exp1}_{exp2}.tsv', exp1=config['Exp1'], exp2=config['Exp2']),
        directory(expand('../../results/MAJIQ/PSI_{exp1}/',exp1=config['Exp1'])),
        directory(expand('../../results/MAJIQ/PSI_{exp2}/',exp2=config['Exp2']))
    output:
        expand('../../results/Voila/{exp1}_{exp2}.subsetES.tsv', exp1=config['Exp1'], exp2=config['Exp2']),
        expand('../../results/MAJIQ/{exp1}_PSI_concatenated/{exp1}_PSI_all_rep.tsv', exp1=config['Exp1']),
        expand('../../results/MAJIQ/{exp2}_PSI_concatenated/{exp2}_PSI_all_rep.tsv', exp2=config['Exp2'])
    script:
        "../scripts/extract_EStrue_psi.py"