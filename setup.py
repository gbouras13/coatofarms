import os
from setuptools import setup, find_packages


def get_version():
    with open(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "coatofarms",
            "coatofarms.VERSION",
        )
    ) as f:
        return f.readline().strip()


CLASSIFIERS = [
    "Environment :: Console",
    "Environment :: MacOS X",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT license",
    "Natural Language :: English",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS :: MacOS X",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
]

setup(
    name="coatofarms",
    packages=find_packages(),
    url="https://github.com/gbouras13/coatofarms",
    python_requires=">=3.7",
    description="ONT Long-read 16S quantification pSnakemake pipeline using Emu",
    version=get_version(),
    author="George Bouras",
    author_email="george.bouras@adelaide.edu.au",
    py_modules=["coatofarms"],
    install_requires=[
        "snakemake>=7.14.0",
        "pyyaml>=6.0",
        "Click>=8.1.3",
    ],
    entry_points={
        "console_scripts": [
            "coatofarms=coatofarms.__main__:main"
        ]
    },
    include_package_data=True,
)
