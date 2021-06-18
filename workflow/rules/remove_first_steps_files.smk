rule clean_directories:
    input:
        expand('../../results/Clean_AS_Event/ES/{control}_{test}_ES_02.tsv', control=config['Control'], test=config['Test'])
    output:
        '../../results/finished.txt'
    shell:
        """
        rm -r -f ../../resources/fastq/
        rm -r -f ../../resources/genome/
        touch ../../results/finished.txt
        """