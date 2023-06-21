# MiSeqHashR
Create and store MD5 hashes of Illumina .fastq.gz files from sequencing runs

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/OLC-Bioinformatics/MiseqHashR/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/OLC-Bioinformatics/MiseqHashR/tree/main)
[![codecov](https://codecov.io/gh/OLC-Bioinformatics/MiseqHashR/branch/main/graph/badge.svg?token=WPYYBU8C6P)](https://codecov.io/gh/OLC-Bioinformatics/MiseqHashR)

### Installation

MiSeqHashR is available as a pip package:

`pip install MiSeqHashR`

### Running

MiseqHashR requires a single command line argument: the path to an Illumina MiSeq run

### Example command

`MiSeqHashR -f sequences/200101_M05722`

### Usage

```
usage: MiSeqHashR [-h] -f folder [-v VERBOSITY] [--version]

Create MD5 hashes for all FASTQ files in a MiSeq run

optional arguments:
  -h, --help            show this help message and exit
  -f folder, --folder folder
                        Name and path of sequencing folder.
  -v VERBOSITY, --verbosity VERBOSITY
                        Set the logging level. Options are debug, info, warning, error, and critical. Default is info.
  --version, --version  show program's version number and exit
  ```
