rule emu:
    input:
        fastqs = os.path.join(PROCESSING,"{sample}_filtlong.fastq.gz")
    params:
        db = EMUDBDIR,
        out_dir = EMU,
        min_abundance = MIN_ABUNDANCE,
        
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


rule aggr_emu:
    input:
        expand(os.path.join(EMU,'{sample}_rel-abundance.tsv'), sample = SAMPLES)
    params:
        EMU
    output:
        os.path.join(EMU_COMBINED,'emu-combined-species.tsv'),
        version = os.path.join(VERSION, 'emu.version')
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
        emu --version > {output.version}
        '''



rule aggr_emu_flag:
    input:
        expand(os.path.join(EMU,'{sample}_rel-abundance.tsv'), sample = SAMPLES),
        os.path.join(EMU_COMBINED,'emu-combined-species.tsv'),
        os.path.join(VERSION, 'emu.version')
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
