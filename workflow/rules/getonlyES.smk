rule getonlyES:
    params:
        exp1 = config['Exp1'],
        exp2 = config['Exp2']
    input:
        expand('../../results/Voila/{exp1}_{exp2}.tsv', exp1=config['Exp1'], exp2=config['Exp2'] )
    output:
        expand('../../results/Voila/{exp1}_{exp2}.subsetES.tsv', exp1=config['Exp1'], exp2=config['Exp2'])
    script:
        "../scripts/extract_EStrue.py"