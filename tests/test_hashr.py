"""
Tests to ensure that the code is functioning properly
"""

# Standard imports
import argparse
import os
import shutil
from unittest.mock import patch

# Third-party imports
import pytest

# Local imports
from hashr.miseq_hashr import (
    cli,
    HashR
    )

__author__ = 'adamkoziol'
__author__ = 'LargeKowalski888'
__author__ = 'noorshu'


@pytest.fixture(name='variables', scope='module')
def setup():
    """
    Pytest fixture to create class variables
    """
    class Variables:
        """
        Create class variables to be used in tests
        """
        def __init__(self):
            self.test_path = os.path.abspath(os.path.dirname(__file__))
            self.file_path = os.path.join(self.test_path, 'files', '200101_M05722')
            self.fake_file_path = os.path.join(self.test_path, 'fake')
            
    return Variables()


def test_fastq_folder_present(variables):
    """
    Test that the script correctly returns the FASTQ files in the supplied folder
    """
    variables.fastq_files = HashR.confirm_fastq_present(sequence_folder=variables.file_path)
    assert os.path.basename(variables.fastq_files[0]) == '2018-CAL-0033_S1_L001_R1_001.fastq.gz'


def test_fastq_folder_absent(variables):
    """
    Test that the script correctly raises a SystemExit when a folder without FASTQ files is provided
    """
    with pytest.raises(SystemExit):
        HashR.confirm_fastq_present(sequence_folder=variables.fake_file_path)


def test_create_hash_folder(variables):
    """
    Test that the folder to store the hash files can be created
    """
    variables.hash_folder = HashR.create_hash_folder(sequence_folder=variables.file_path)
    assert os.path.isdir(variables.hash_folder)


def test_create_hashes(variables):
    """
    Test that the test file contents are hashed properly 
    """
    variables.fastq_hashes = HashR.create_hashes(fastq_files=variables.fastq_files)
    assert variables.fastq_hashes[
        '2018-CAL-0033_S1_L001_R1_001.fastq'] == '7fa54e3f40ea84ce3371d3a8d04fc31f'


def test_create_hashes_empty():
    """
    Test that the create_hashes method fails when provided with an empty list
    """
    with pytest.raises(SystemExit):
        HashR.create_hashes(fastq_files=[])

def test_create_hashes_no_file():
    """
    Tests to ensure that the method fails if the file doesn't exist
    """
    with pytest.raises(FileNotFoundError):
        HashR.create_hashes(fastq_files=['2018-CAL-0033_S1_L001_R1_001'])

def test_write_hashes(variables):
    """
    Test that the hashes are being written to file
    """
    HashR.write_hashes(
        hash_folder=variables.hash_folder,
        fastq_hashes=variables.fastq_hashes
    )
    assert os.path.isfile(
        os.path.join(variables.hash_folder, '2018-CAL-0033_S1_L001_R1_001.fastq.txt')
        )

def test_write_hashes_illegal(variables):
    """
    Tests that the method fails when an illegal path is provided
    """
    with pytest.raises(FileNotFoundError):
        HashR.write_hashes(
            hash_folder='/not/a/real/folder',
            fastq_hashes=variables.fastq_hashes
        )

def test_cleanup(variables):
    """
    Delete the test folder following the completion of all the tests
    """
    shutil.rmtree(variables.hash_folder)
    assert not os.path.isdir(variables.hash_folder)

@patch('argparse.ArgumentParser.parse_args')
def test_hashr_integration(mock_args, variables):
    """
    Run the integration tests
    """
    mock_args.return_value = argparse.Namespace(
        folder=variables.file_path,
        verbosity='info'
    )
    cli()
    assert os.path.isdir(variables.hash_folder)

def test_cleanup_integration(variables):
    """
    Delete the test folder following the completion of all the tests
    """
    shutil.rmtree(variables.hash_folder)
    assert not os.path.isdir(variables.hash_folder)
