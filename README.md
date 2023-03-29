# coatofarms

ONT Long-read 16S Snakemake and [Snaketool](https://github.com/beardymcjohnface/Snaketool) pipeline using [Emu](https://gitlab.com/treangenlab/emu)

```
git clone "https://github.com/gbouras13/coatofarms.git"
cd coatofarms/
pip install -e .
coatofarms --help
coatofarms install --help
coatofarms run --help
```

coatofarms is a simple pipeline to conduct ONT 16S quantification that essentially just wraps [Emu](https://gitlab.com/treangenlab/emu) for many samples, along with QC and visualisation using Krona plots. It leverages the embarassingly parallel power of HPC and Snakemake profiles. 

Downstream analysis (alpha diversities etc) not included.


Pipeline
==========

1. Long-read QC: filtlong to keep all reads between 1300 and 1700 bp and above a minimum Quality (these can be changed in the config file) (qc.smk).
2. Nanoplot QC for each input file (nanoplot.smk).
3. Runs Emu on each sample and combine the output at the species level (emu.smk). 
4. Visualise the Emu output for each sample using Krona (krona.smk).


Input
=======

* coatofarms requires an input csv file with 2 columns 
* Each row is a sample
* Column 1 is the sample name, column 2 is the long read ONT fastq file of 16S reads.
* No headers

e.g.


sample1,sample1_long_read.fastq.gz

sample2,sample2_long_read.fastq.gz


Usage
=======

First, you need to specify a species and an output directory to install the default Emu database.

```
coatofarms install --directory EmuDatabase 
```

After that has finished, run the pipeline, specifying the minimum detectable abundance and reference directory:

```
coatofarms run --input <input.csv> --output <output_dir> --threads <threads> --abundance <min abundance of species for Emu> --directory EmuDatabase 
```


I would highly highly recommend running hybracter using a Snakemake profile. Please see this blog [post](https://fame.flinders.edu.au/blog/2021/08/02/snakemake-profiles-updated) for more details. I have included an example slurm profile in the profile directory, but check out this [link](https://github.com/Snakemake-Profiles) for more detail on other HPC job scheduler profiles. 

```
coatofarms run --input <input.csv> --output <output_dir> --threads <threads>   --directory EmuDatabase  --profile profiles/coatofarms
```

Output
=====

All relevant outputs are in the EMU and KRONA directories.
