""" Tests for filetype utility functions """

import pytest
from ngstk.filetypes import *
from ubiquerg import ExpectContext

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


@pytest.mark.skip("not implemented")
@pytest.mark.parametrize(["file_name", "expected"], [])
def test_get_input_ext(file_name, expected):
    with ExpectContext(expected, get_input_ext) as f:
        f(file_name)


@pytest.mark.skip("not implemented")
@pytest.mark.parametrize(["file_name", "expected"], [])
def test_is_sam_or_bam(file_name, expected):
    pass


@pytest.mark.skip("not implemented")
@pytest.mark.parametrize(["file_name", "expected"], [])
def test_is_fastq(file_name, expected):
    pass


@pytest.mark.skip("not implemented")
@pytest.mark.parametrize(["file_name", "expected"], [])
def test_is_gzipped_fastq(file_name, expected):
    pass


@pytest.mark.skip("not implemented")
@pytest.mark.parametrize(["file_name", "expected"], [])
def test_is_unzipped_fastq(file_name, expected):
    pass
