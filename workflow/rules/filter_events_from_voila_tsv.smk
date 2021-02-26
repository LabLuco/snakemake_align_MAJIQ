rule filter_events:
    params:
        control = config['Control'],
        test = config['Test']
    input:
        expand('../../results/Voila/{control}_{test}.tsv', control=config['Control'], test=config['Test']),
        directory(expand('../../results/MAJIQ/PSI_{control}/',control=config['Control'])),
        directory(expand('../../results/MAJIQ/PSI_{test}/',test=config['Test']))
    output:
        expand('../../results/Clean_AS_Event/ES/{control}_{test}_ES_01.tsv', control=config['Control'], test=config['Test']),
        expand('../../results/Clean_AS_Event/ES/{control}_{test}_ES_02.tsv', control=config['Control'], test=config['Test']),
        expand('../../results/Clean_AS_Event/A5SS/{control}_{test}_A5SS_01.tsv', control=config['Control'], test=config['Test']),
        expand('../../results/Clean_AS_Event/A5SS/{control}_{test}_A5SS_02.tsv', control=config['Control'], test=config['Test']),
        expand('../../results/Clean_AS_Event/A3SS/{control}_{test}_A3SS_01.tsv', control=config['Control'], test=config['Test']),
        expand('../../results/Clean_AS_Event/A3SS/{control}_{test}_A3SS_02.tsv', control=config['Control'], test=config['Test']),
        expand('../../results/Clean_AS_Event/IR/{control}_{test}_IR_01.tsv', control=config['Control'], test=config['Test']),
        expand('../../results/Clean_AS_Event/IR/{control}_{test}_IR_02.tsv', control=config['Control'], test=config['Test'])
    script:
        "../scripts/filter_events_from_voila_tsv.py"