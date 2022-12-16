#!/usr/bin/env python3

import pandas as pd

def prep_krona(abundance_file, readcount_file, output):
    abundance_df = pd.read_csv(abundance_file, delimiter= '\t', index_col=False)

    with open(readcount_file, 'r') as f:
      read_count = f.read()
    # get the read count
    abundance_df["matching_reads"] = round(abundance_df["abundance"] * int(read_count))
    # format for use with ktText
    abundance_df["species"] = "s__" + abundance_df["species"]
    abundance_df["genus"] = "g__" + abundance_df["genus"]
    abundance_df["family"] = "f__" + abundance_df["family"]
    abundance_df["order"] = "o__" + abundance_df["order"]
    abundance_df["class"] = "c__" + abundance_df["class"]
    abundance_df["phylum"] = "p__" + abundance_df["phylum"]
    abundance_df["superkingdom"] = "k__" + abundance_df["superkingdom"]
    abundance_df = abundance_df[['matching_reads', 'superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']]

    # all the kingdoms

    abundance_df.to_csv(output, sep="\t", index=False, header=False)

prep_krona(snakemake.input[0], snakemake.input[1], snakemake.output[0])
