#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess as sp
from argparse import RawTextHelpFormatter
import pandas as pd
import os
import pathlib 

def combine_outputs(dir_path, rank, split_files=False, count_table=False):
    """ Combines multiple Emu output relative abundance tables into a single table.
        Inlcudes all .tsv files with 'rel-abundance' in the filename in the provided dir_path.

        dir_path(str): path of directory containing Emu output files to combine
        rank(str): taxonomic rank to combine files on
        return(df): Pandas df of the combined relative abundance files
    """
    keep_ranks = ['tax_id', 'lineage']
    df_combined_full = pd.DataFrame(columns=keep_ranks, dtype=str)
    metric = 'abundance'
    if count_table:
        metric = 'estimated counts'
    for file in os.listdir(dir_path):
        file_extension = pathlib.Path(file).suffix
        if file_extension == '.tsv' and 'rel-abundance' in file:
            name = pathlib.Path(file).stem
            name = name.replace('_rel-abundance', '')
            df_sample = pd.read_csv(os.path.join(dir_path, file), sep='\t', dtype=str)
            df_sample[[metric]] = df_sample[[metric]].apply(pd.to_numeric)
            if rank in df_sample.columns and metric in df_sample.columns:
                keep_ranks_sample = [value for value in keep_ranks if value in set(df_sample.columns)] #check which keep_ranks are in df_sample
                if df_sample.at[len(df_sample.index)-1, 'tax_id'] == 'unassigned':
                    df_sample.at[len(df_sample.index)-1, rank] = 'unassigned'
                df_sample_reduced = df_sample[keep_ranks_sample + [metric]].rename(columns={metric: name})
                df_sample_reduced = df_sample_reduced.groupby(keep_ranks_sample, dropna=False).sum().reset_index() #sum metric within df_sample_reduced if same tax lineage
                df_sample_reduced = df_sample_reduced.astype(object)
                df_sample_reduced[[name]] = df_sample_reduced[[name]].apply(pd.to_numeric)
                df_combined_full = pd.merge(df_combined_full, df_sample_reduced, how='outer')
    df_combined_full = df_combined_full.set_index(rank).sort_index().reset_index()
    filename_suffix = ""
    if count_table:
        filename_suffix = "-counts"
    if split_files:
        abundance_out_path = os.path.join(dir_path, "emu-combined-abundance-{}{}.tsv".format(rank, filename_suffix))
        tax_out_path = os.path.join(dir_path, "emu-combined-taxonomy-{}.tsv".format(rank))
        #stdout.write("Combined taxonomy table generated: {}\n".format(tax_out_path))
        df_combined_full[keep_ranks].to_csv(tax_out_path, sep='\t', index=False)
        keep_ranks.remove(rank)
        df_combined_full.drop(columns=keep_ranks).to_csv(abundance_out_path, sep='\t', index=False)
        #stdout.write("Combined abundance table generated: {}\n".format(abundance_out_path))
    else:
        out_path = os.path.join(dir_path, "emu-combined-{}{}.tsv".format(rank, filename_suffix))
        df_combined_full.to_csv(out_path, sep='\t', index=False)
        #stdout.write("Combined table generated: {}\n".format(out_path))
    return df_combined_full

def get_input():
    parser = argparse.ArgumentParser(
        description="parses and combines silva format from EMU. See this issue https://gitlab.com/treangenlab/emu/-/issues/37.",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "-d", "--directory", action="store", help="path to directory containing Emu output files.", required=True
    )
    args = parser.parse_args()
    return args

def main():
    # get the args
    args = get_input()

    combine_outputs(args.directory, "lineage")


if __name__ == "__main__":
    main()