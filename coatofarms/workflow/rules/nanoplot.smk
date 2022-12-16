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


rule aggr_nanoplot:
    input:
        expand( os.path.join(NANOPLOT,"{sample}", "passNanoStats.txt"), sample = SAMPLES)
    output:
        os.path.join(FLAGS, "aggr_nanoplot.txt")
    threads:
        1
    resources:
        mem_mb=SmallJobMem,
        time=SmallTime
    shell:
        """
        touch {output[0]}
        """
