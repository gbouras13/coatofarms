rule emu:
    input:
        fastqs = os.path.join(PROCESSING,"{sample}_filtlong.fastq.gz")
    params:
        db = EMUDBDIR,
        out_dir = EMU,
        min_abundance = MIN_ABUNDANCE
    output:
        abundance = os.path.join(EMU,'{sample}_rel-abundance.tsv')
    threads:
        BigJobCpu
    resources:
        mem_mb=BigJobMem,
        time=BigTime
    conda:
        os.path.join('..', 'envs','emu.yaml')
    shell:
        '''
        emu abundance {input.fastqs} --threads {threads} --min-abundance {params.min_abundance} --db {params.db} --output-dir {params.out_dir} --output-basename {wildcards.sample}
        '''

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
        os.path.join('..', 'envs','emu.yaml')
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
        os.path.join('..', 'envs','emu.yaml')
    threads:
        1
    resources:
        mem_mb=SmallJobMem,
        time=MediumTime
    shell:
        '''
        ktImportText {input} -o {output}
        '''

rule aggr_emu:
    input:
        expand(os.path.join(EMU,'{sample}_rel-abundance.tsv'), sample = SAMPLES)
    params:
        EMU
    output:
        os.path.join(EMU_COMBINED,'emu-combined-species.tsv')
    conda:
        os.path.join('..', 'envs','emu.yaml')
    threads:
        1
    resources:
        mem_mb=SmallJobMem,
        time=MediumTime
    shell:
        '''
        emu combine-outputs {params[0]} 'species'
        '''



rule aggr_emu_flag:
    input:
        expand(os.path.join(EMU,'{sample}_rel-abundance.tsv'), sample = SAMPLES),
        expand(os.path.join(KRONA,'{sample}.html'), sample = SAMPLES),
        os.path.join(EMU_COMBINED,'emu-combined-species.tsv')
    output:
        os.path.join(FLAGS, "aggr_emu.txt")
    threads:
        1
    resources:
        mem_mb=SmallJobMem,
        time=SmallTime
    shell:
        """
        touch {output[0]}
        """
