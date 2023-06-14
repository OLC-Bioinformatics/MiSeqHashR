"""
Tests to ensure that the code is functioning properly
"""

# Standard imports
import os

# Third-party imports
import pytest

# Local imports
from hashr.miseq_hashr import HashR

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

