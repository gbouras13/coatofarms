# instantiate the EMU_DB_DIR

EMUDBDIR = config['database']

if not os.path.exists(os.path.join(EMUDBDIR)):
    os.makedirs(os.path.join(EMUDBDIR))


rule all:
    input:
        os.path.join(EMUDBDIR,"taxonomy.tsv"),
        os.path.join(EMUDBDIR,"species_taxid.fasta")

rule get_db:
    params:
        emu_db = EMUDBDIR
    output:
        os.path.join(EMUDBDIR,"taxonomy.tsv"),
        os.path.join(EMUDBDIR,"species_taxid.fasta")
    conda:
        os.path.join('..', 'envs','emu.yaml')
    shell:
        """
        cd ${params.emu_db}
        osf -p 56uf7 fetch osfstorage/emu-prebuilt/emu.tar
        tar -xvf emu.tar
        """


