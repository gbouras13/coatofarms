"""
Entrypoint for coatofarms
Check out the wiki for a detailed look at customising this file:
https://github.com/beardymcjohnface/Snaketool/wiki/Customising-your-Snaketool
"""

import os
import click

from .util import (
    snake_base,
    print_version,
    default_to_output,
    copy_config,
    run_snakemake,
    OrderedCommands,
    print_citation,
)


def common_options(func):
    """Common command line args
    Define common command line args here, and include them with the @common_options decorator below.
    """
    options = [
        click.option(
            "--output",
            help="Output directory",
            type=click.Path(dir_okay=True, writable=True, readable=True),
            default="coatofarms.out",
            show_default=True,
        ),
        click.option(
            "--configfile",
            default="config.yaml",
            show_default=False,
            callback=default_to_output,
            help="Custom config file [default: (outputDir)/config.yaml]",
        ),
        click.option(
            "--threads", help="Number of threads to use", default=1, show_default=True
        ),
        click.option(
            "--use-conda/--no-use-conda",
            default=True,
            help="Use conda for Snakemake rules",
            show_default=True,
        ),
        click.option(
            "--conda-prefix",
            default=snake_base(os.path.join("workflow", "conda")),
            help="Custom conda env directory",
            type=click.Path(),
            show_default=False,
        ),
        click.option(
            "--snake-default",
            multiple=True,
            default=[
                "--rerun-incomplete",
                "--printshellcmds",
                "--nolock",
                "--show-failed-logs",
                "--conda-frontend conda",
            ],
            help="Customise Snakemake runtime args",
            show_default=True,
        ),
        click.option(
            "--log",
            default="coatofarms.log",
            callback=default_to_output,
            hidden=True,
        ),
        click.argument("snake_args", nargs=-1),
    ]
    for option in reversed(options):
        func = option(func)
    return func


@click.group(
    cls=OrderedCommands, context_settings=dict(help_option_names=["-h", "--help"])
)
def cli():
    """For more options, run:
    coatofarms command --help"""
    pass


help_msg_extra = """
\b
CLUSTER EXECUTION:
coatofarms run ... --profile [profile]
For information on Snakemake profiles see:
https://snakemake.readthedocs.io/en/stable/executing/cli.html#profiles
\b
RUN EXAMPLES:
Required:           coatofarms run --input [file]
Specify threads:    coatofarms run ... --threads [threads]
Disable conda:      coatofarms run ... --no-use-conda 
Change defaults:    coatofarms run ... --snake-default="-k --nolock"
Add Snakemake args: coatofarms run ... --dry-run --keep-going --touch
Specify targets:    coatofarms run ... all print_targets
Available targets:
    all             Run everything (default)
    print_targets   List available targets
"""


help_msg_install = """
\b
CLUSTER EXECUTION:
coatofarms install ... 
\b
RUN EXAMPLES:
Required:           coatofarms install --database [directory]
"""

@click.command(
    epilog=help_msg_extra,
    context_settings=dict(
        help_option_names=["-h", "--help"], ignore_unknown_options=True
    ),
)
@click.option("--input", "_input", help="Input file/directory", type=str, required=True)
@click.option('--database', 'database', help='DB directory', show_default=True,  default='Database')
@click.option('--abundance', 'abundance', help='minimum relative abundance for Emu. Defaults to 0.001 (=0.1%)', show_default=True,  default='0.001 ')
@common_options
def run(_input, output, database, threads, log, abundance, **kwargs):
    """Run coatofarms"""
    # Config to add or update in configfile
    merge_config = {"input": _input, "output": output, "database": database, "threads": threads, "abundance": abundance, "log": log}
    # run!
    run_snakemake(
        # Full path to Snakefile
        snakefile_path=snake_base(os.path.join("workflow", "Snakefile")),
        merge_config=merge_config,
        log=log,
        **kwargs
    )


# install

@click.command(
    epilog=help_msg_install,
    context_settings=dict(
        help_option_names=["-h", "--help"], ignore_unknown_options=True
    ))
@click.option(
            "--use-conda/--no-use-conda",
            default=True,
            help="Use conda for Snakemake rules",
            show_default=True,
        )
@click.option(
            "--snake-default",
            multiple=True,
            default=[
                "--rerun-incomplete",
                "--printshellcmds",
                "--nolock",
                "--show-failed-logs",
                "--conda-frontend conda"
            ],
            help="Customise Snakemake runtime args",
            show_default=True,
        )
@click.option('--database', 'database', help='DB directory', show_default=True,  default='Database')
@common_options
def download(database, log, output,  **kwargs):
    """Install EMU Database"""
    # Config to add or update in configfile
    merge_config = {  "database": database, 'output': output, "log": log }
    """Install databases"""
    run_snakemake(
        snakefile_path=snake_base(os.path.join('workflow','InstallDB.smk')),
        merge_config=merge_config,
        **kwargs)


@click.command()
@common_options
def config(configfile, **kwargs):
    """Copy the system default config file"""
    copy_config(configfile)


@click.command()
def citation(**kwargs):
    """Print the citation(s) for this tool"""
    print_citation()


cli.add_command(run)
cli.add_command(download)
cli.add_command(config)
cli.add_command(citation)


def main():
    print_version()
    cli()


if __name__ == "__main__":
    main()