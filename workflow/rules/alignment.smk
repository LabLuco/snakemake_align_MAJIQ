rule alignment:
    params:
        nbrep = config['NbRep'],
        exp1 = config['Exp1'],
        exp2 = config['Exp2']
    input:
    output:
    script:
        "../scripts/alignment.py"