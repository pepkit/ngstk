""" Tests for filetype utility functions """

import pytest
from ngstk.filetypes import *
from veracitools import ExpectContext

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


EXPECTATIONS_PARAMS_DATA = {
    get_input_ext: [
        ("test.bam", ".bam"),
        ("random.fastq", ".fastq"), ("random.fq", ".fastq"),
        ("arb.fq.gz", ".fastq.gz"), ("random.fastq.gz", ".fastq.gz"),
        ("test.bed", UnsupportedFiletypeException),
        ("arb.zip", UnsupportedFiletypeException),
        ("test.sam", UnsupportedFiletypeException),
        ("test.SAM", UnsupportedFiletypeException),
        ("test.BAM", UnsupportedFiletypeException),
    ],
    is_sam_or_bam: [
        ("test.sam", True), ("test.bam", True), ("test.SAM", False),
        ("test.BAM", False), ("random.fastq", False), ("random.fq", False),
        ("arb.fq.gz", False), ("random.fastq.gz", False), ("test.bed", False),
        ("arb.zip", False)
    ],
    is_fastq: [
        ("test.sam", False), ("test.bam", False), ("test.SAM", False),
        ("test.BAM", False), ("test.bed", False), ("arb.zip", False),
        ("random.fq", True), ("random.fastq", True),
        ("arb.fq.gz", True), ("random.fastq.gz", True)
    ],
    is_gzipped_fastq: [
        ("test.sam", False), ("test.bam", False),
        ("test.SAM", False), ("random.fq", False),
        ("test.BAM", False), ("random.fastq", False),
        ("arb.fq.gz", True), ("random.fastq.gz", True),
        ("test.bed", False), ("arb.zip", False)
    ],
    is_unzipped_fastq: [
        ("test.sam", False), ("test.bam", False),
        ("test.SAM", False), ("random.fq", True),
        ("test.BAM", False), ("random.fastq", True),
        ("arb.fq.gz", False), ("random.fastq.gz", False),
        ("test.bed", False), ("arb.zip", False)
    ]
}


@pytest.mark.parametrize(
    ["fun", "filename", "exp"],
    [(f, fn, exp) for f, params in EXPECTATIONS_PARAMS_DATA.items()
     for fn, exp in params])
def test_filename_based_determination_function(fun, filename, exp):
    """ Check result of application of filename-based function. """
    with ExpectContext(exp, fun) as f:
        f(filename)
