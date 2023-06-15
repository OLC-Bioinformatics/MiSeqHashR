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

# Local imports
from hashr.version import __version__

__author__ = 'adamkoziol'
__author__ = 'LargeKowalski888'
__author__ = 'noorshu'


class HashR:

    """
    Finds a Illumina MiSeq sequencing run, ensures that FASTQ files are present, creates MD5 hashes
    for each file, and saves each hash to file
    """

    def main(self):
        """
        Runs the HashR methods
        """
        self.hash_folder = HashR.create_hash_folder(sequence_folder=self.sequence_folder)
        self.fastq_hashes = HashR.create_hashes(fastq_files=self.fastq_files)
        HashR.write_hashes(
            hash_folder=self.hash_folder,
            fastq_hashes=self.fastq_hashes
        )

    @staticmethod
    def confirm_fastq_present(sequence_folder: str):
        """
        Ensures that FASTQ files are present in the supplied sequencing run
        :param str sequence_folder: Name and path of MiSeq sequencing run
        :return fastq_files: List of all FASTQ files in sequencing run
        """
        # As Illumina nests the FASTQ files within the sequence folder, add the nesting
        nested_folder = os.path.join(sequence_folder, 'Data', 'Intensities', 'BaseCalls')
        # The FASTQ files have a .fastq.gz extension. Find all files that match this with glob
        fastq_files = sorted(glob(os.path.join(nested_folder, '*.fastq.gz')))
        # Ensure that there are FASTQ files in the folder
        try:
            assert fastq_files
        except AssertionError as exc:
            logging.error(
                'Could not find any FASTQ files in the supplied sequence folder: %s', 
                sequence_folder)
            raise SystemExit from exc
        return fastq_files

    @staticmethod
    def create_hash_folder(sequence_folder: str):
        """
        Create a folder into which hash files will be written
        :param str sequence_folder: Name and path of MiSeq sequencing run
        :return hash_folder: Name and path of folder into which FASTQ hashes are to be written
        """
        hash_folder = os.path.join(sequence_folder, 'hashes')
        # Makes the folder hashes within the directory listed below
        os.makedirs(
                hash_folder,
                exist_ok=True
                )
        logging.debug('Hashes will be written to: %s', hash_folder)
        return hash_folder


    @staticmethod
    def create_hashes(fastq_files: list):
        """
        Create MD5 hashes for each FASTQ file
        :param list fastq_files: List of all FASTQ files in sequencing run
        :return fastq_hashes: Dictionary of sample_name: FASTQ hash
        """
        fastq_hashes = {}
        for fastq in fastq_files:
            # Extract the base name of the FASTQ file by splitting off the path and extension
            fastq_name = os.path.splitext(os.path.basename(fastq))[0]
            # Use hashlib.md5 to create a MD5 hash for the FASTQ file
            md5_hash = hashlib.md5(open(fastq,'rb').read()).hexdigest()
            # Add the hash to the list of hashes
            fastq_hashes[fastq_name] = md5_hash
        try:
            assert fastq_hashes
        except AssertionError as exc:
            logging.error('Could not create hashes from files')
            raise SystemExit from exc
        logging.debug('Calculated hashes: %s', fastq_hashes)
        return fastq_hashes

    @staticmethod
    def write_hashes(hash_folder: str,
                     fastq_hashes: dict):
        """
        Write the hashes to file
        :param str hash_folder: Name and path of folder into which hashes are to be written
        :param dict fastq_hashes: Dictionary of sample_name: FASTQ hash
        """
        for fastq_name, fastq_hash in fastq_hashes.items():
            # Set the name of the hash file
            hash_file = os.path.join(hash_folder, f'{fastq_name}.txt')
            # Write the hash to the text file
            with open(hash_file, 'w', encoding='utf-8') as text_hash:
                text_hash.write(fastq_hash)

    def __init__(self, sequence_folder):
        self.sequence_folder = sequence_folder
        self.fastq_files = HashR.confirm_fastq_present(sequence_folder=self.sequence_folder)
        logging.debug('FASTQ files:\n%s', '\n'.join(self.fastq_files))
        self.hash_folder = str()
        self.fastq_hashes = []


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
    parser.add_argument(
        '--version', '--version',
        action='version',
        version='%(prog)s commit {}'.format(__version__)
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
