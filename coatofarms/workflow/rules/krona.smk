rule read_count:
    input:
        os.path.join(PROCESSING,"{sample}_filtlong.fastq.gz")
    output:
        os.path.join(READCOUNT,'{sample}_readcount.txt')
    threads:
        1
    resources:
        mem_mb=SmallJobMem,
        time=SmallTime
    shell:
        '''
        echo $(cat {input}|wc -l)/4|bc > {output}
        '''

rule krona_input:
    input:
        abundance = os.path.join(EMU,'{sample}_rel-abundance.tsv'),
        reads = os.path.join(READCOUNT,'{sample}_readcount.txt')
    output:
        reads = os.path.join(KRONA,'{sample}.txt')
    conda:
        os.path.join('..', 'envs','krona.yaml')
    threads:
        1
    resources:
        mem_mb=SmallJobMem,
        time=SmallTime
    script:
        '../Scripts/create_tsv_for_krona.py'

rule krona:
    input:
        os.path.join(KRONA,'{sample}.txt')
    output:
        os.path.join(KRONA,'{sample}.html')
    conda:
        os.path.join('..', 'envs','krona.yaml')
    threads:
        1
    resources:
        mem_mb=SmallJobMem,
        time=MediumTime
    shell:
        '''
        ktImportText {input} -o {output}
        '''

rule aggr_krona_flag:
    input:
        expand(os.path.join(KRONA,'{sample}.html'), sample = SAMPLES)
    output:
        os.path.join(FLAGS, "aggr_krona.txt")
    threads:
        1
    resources:
        mem_mb=SmallJobMem,
        time=SmallTime
    shell:
        """
        touch {output[0]}
        """