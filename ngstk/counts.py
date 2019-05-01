""" Line/read counting functions """

import os
import subprocess
from .filetypes import *
from .inspection import *

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"
__credits = ["Nathan Sheffield", "Andre Rendeiro", "Vince Reuter"]

__all__ = ["count_fail_reads", "count_flag_reads", "count_lines",
           "count_lines_zip", "count_reads"]


def count_fail_reads(file_name, paired_end, prog_path):
    """
    Count the number of reads that failed platform/vendor quality checks.

    :param str file_name: name/path to file to examine
    :param paired_end: this parameter is ignored; samtools automatically
        correctly responds depending on the data in the bamfile; we leave the
        option here just for consistency, since all the other counting
        functions require the parameter; this makes it easier to swap counting
        functions during pipeline development.
    :param str prog_path: path to main program/tool to use for the counting
    :return int: count of failed reads
    """
    return int(count_flag_reads(file_name, 512, paired_end, prog_path))


def count_flag_reads(file_name, flag, paired_end, prog_path):
    """
    Counts the number of reads with the specified flag.

    :param str file_name: name/path to file to examine
    :param str int | flag: SAM flag value to be read
    :param paired_end: this parameter is ignored; samtools automatically
        correctly responds depending on the data in the bamfile; we leave the
        option here just for consistency, since all the other counting
        functions require the parameter; this makes it easier to swap counting
        functions during pipeline development.
    :param str prog_path: path to main program/tool to use for the counting
    :return str: terminal-like text output
    """

    param = " -c -f" + str(flag)
    if file_name.endswith("sam"):
        param += " -S"
    return samtools_view(file_name, param=param, prog_path=prog_path)


def count_lines(file_name):
    """
    Uses the command-line utility wc to count the number of lines in a file.

    For MacOS, must strip leading whitespace from wc.

    :param str file_name: name of file whose lines are to be counted
    :return str: terminal-like text output
    """
    cmd = "wc -l " + file_name + " | sed -E 's/^[[:space:]]+//' | cut -f1 -d' '"
    return subprocess.check_output(cmd, shell=True).decode().strip()


def count_lines_zip(file_name):
    """
    Count number of lines in a zipped file.

    This function eses the command-line utility wc to count the number of lines
    in a file. For MacOS, strip leading whitespace from wc.

    :param str file_name: path to file in which to count lines
    :return str: terminal-like text output
    """
    cmd = "gunzip -c " + file_name + " | wc -l | sed -E 's/^[[:space:]]+//' | cut -f1 -d' '"
    return subprocess.check_output(cmd, shell=True).decode().strip()


def count_reads(file_name, paired_end, prog_path):
    """
    Count reads in a file.

    Paired-end reads count as 2 in this function.
    For paired-end reads, this function assumes that the reads are split
    into 2 files, so it divides line count by 2 instead of 4.
    This will thus give an incorrect result if your paired-end fastq files
    are in only a single file (you must divide by 2 again).

    :param str file_name: Name/path of file whose reads are to be counted.
    :param bool paired_end: Whether the file contains paired-end reads.
    :param str prog_path: path to main program/tool to use for the counting
    :return str: terminal-like text output (if input is SAM/BAM), or actual
        count value (if input isn't SAM/BAM)
    """

    _, ext = os.path.splitext(file_name)
    if not (is_sam_or_bam(file_name) or is_fastq(file_name)):
        # TODO: make this an exception and force caller to handle that
        # rather than relying on knowledge of possibility of negative value.
        return -1

    if is_sam_or_bam(file_name):
        param_text = "-c" if ext == ".bam" else "-c -S"
        return samtools_view(file_name, param=param_text, prog_path=prog_path)
    else:
        num_lines = count_lines_zip(file_name) \
                if is_gzipped_fastq(file_name) \
                else count_lines(file_name)
        divisor = 2 if paired_end else 4
        return int(num_lines) / divisor
