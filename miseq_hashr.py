#!/usr/bin/env python3

"""
Takes a user-provided Illumina MiSeq sequencing folder, creates MD5 hashes for each FASTQ file, and 
saves the MD5 file to a new folder
"""

# Standard imports
from argparse import ArgumentParser
from glob import glob
import hashlib
import logging
import os


class HashR:
  
    """
    Finds a Illumina MiSeq sequencing run, ensures that FASTQ files are present, creates MD5 hashes
    for each file, and saves each hash to file
    """

    def main(self):
        """
        Runs the HashR methods
        """

    @staticmethod
    def confirm_fastq_present(sequence_folder: str):
        """
        Ensures that FASTQ files are present in the supplied sequencing run
        :param str sequence_folder: Name and path of MiSeq sequencing run
        """
        # As Illumina nests the FASTQ files within the sequence folder, add the nesting
        nested_folder = os.path.join(sequence_folder, 'Data', 'Intensities', 'BaseCalls')
        # The FASTQ files have a .fastq.gz extension. Find all files that match this with glob
        fastq_files = glob(os.path.join(nested_folder, '*.fastq.gz'))
        # Ensure that there are FASTQ files in the folder
        try:
            assert fastq_files
        except AssertionError as exc:
            logging.error(
                'Could not find any FASTQ files in the supplied sequence folder: %s', 
                sequence_folder)
            raise SystemExit from exc
        return fastq_files


    def __init__(self, sequence_folder):
        self.sequence_folder = sequence_folder
        self.fastq_files = HashR.confirm_fastq_present(sequence_folder=self.sequence_folder)
        logging.debug('FASTQ files:\n%s', '\n'.join(self.fastq_files))


# Sets optional arguements for python file in command prompt
def cli():
    """
    Collect command line arguments
    """
    parser = ArgumentParser(description='Create MD5 hashes for all FASTQ files in a MiSeq run')
    parser.add_argument(
        '-f', '--folder',
        metavar='folder',
        required=True,
        type=str,
        help='Name and path of sequencing folder.')
    parser.add_argument(
        '-v', '--verbosity',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        metavar='VERBOSITY',
        default='info',
        help='Set the logging level. Options are debug, info, warning, error, and critical. '
             'Default is info.'
    )
    args = parser.parse_args()
    logging.basicConfig(
        level=args.verbosity.upper(),
        format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('Processing sequencing folder: %s', args.folder)
    hashr = HashR(
        sequence_folder=args.folder
    )
    hashr.main()


if __name__ == '__main__':
    cli()
