def get_input_fastqs(wildcards):
    return dictReads[wildcards.sample]["LR"]

rule filtlong:
    input:
        get_input_fastqs
    output:
        os.path.join(PROCESSING,"{sample}_filtlong.fastq.gz")
    params:
        min_read_size = MIN_LENGTH,
        max_read_size = MAX_LENGTH,
        max_q_score = MIN_QUALITY
    resources:
        mem_mb=SmallJobMem,
        time=MediumTime
    conda:
        os.path.join('..', 'envs','filtlong.yaml')
    threads:
        1
    shell:
        '''
        filtlong --min_length {params.min_read_size} --max_length {params.max_read_size} --min_mean_q {params.max_q_score} {input} | gzip > {output}
        '''

rule nanoplot:
    input:
        os.path.join(PROCESSING,"{sample}_filtlong.fastq.gz")
    output:
        os.path.join(NANOPLOT,"{sample}", "passNanoStats.txt")
    params:
        directory(os.path.join(NANOPLOT,"{sample}"))
    resources:
        mem_mb=SmallJobMem,
        time=MediumTime
    conda:
        os.path.join('..', 'envs','nanoplot.yaml')
    threads:
        BigJobCpu
    shell:
        '''
        NanoPlot --prefix pass --fastq {input} -t {threads} -o {params}
        '''

    
rule aggr_qc:
    input:
        expand( os.path.join(PROCESSING,"{sample}_filtlong.fastq.gz"), sample = SAMPLES),
        expand( os.path.join(NANOPLOT,"{sample}", "passNanoStats.txt"), sample = SAMPLES)
    output:
        os.path.join(FLAGS, "aggr_qc.txt")
    threads:
        1
    resources:
        mem_mb=SmallJobMem,
        time=SmallTime
    shell:
        """
        touch {output[0]}
        """
