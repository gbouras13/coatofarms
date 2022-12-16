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
    shell:
        """
        wget "https://gitlab.com/treangenlab/emu/-/archive/v3.0.0/emu-v3.0.0.tar.gz"
        mkdir -p {params.emu_db}
        tar -xf emu-v3.0.0.tar.gz -C {params.emu_db}
        mv {params.emu_db}/emu-v3.0.0/emu_database/* {params.emu_db}
        rm -rf {params.emu_db}/emu-v3.0.0
        rm emu-v3.0.0.tar.gz
        """


