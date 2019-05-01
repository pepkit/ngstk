""" File inspection functions """

from collections import defaultdict, namedtuple
import subprocess

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"
__credits = ["Nathan Sheffield", "Andre Rendeiro", "Vince Reuter"]

__all__ = ["peek_read_lengths_and_paired_counts_from_bam", "samtools_view"]


PeekBamResult = namedtuple("PeekBamResult", ["read_lengths", "paired"])


def peek_read_lengths_and_paired_counts_from_bam(bam, sample_size):
    """
    Counting read lengths and paired reads in a sample from a BAM.

    :param str bam: path to BAM file to examine
    :param int sample_size: number of reads to look at for estimation
    :return defaultdict[int, int], int: read length observation counts, and
        number of paired reads observed
    :raise OSError:
    """
    try:
        p = subprocess.Popen(['samtools', 'view', bam], stdout=subprocess.PIPE)
        # Count paired alignments
        paired = 0
        read_lengths = defaultdict(int)
        for _ in range(sample_size):
            line = p.stdout.readline().decode().split("\t")
            flag = int(line[1])
            read_lengths[len(line[9])] += 1
            if 1 & flag:  # check decimal flag contains 1 (paired)
                paired += 1
        p.kill()
    except OSError:
        reason = "Note (samtools not in path): For NGS inputs, " \
                 "pep needs samtools to auto-populate " \
                 "'read_length' and 'read_type' attributes; " \
                 "these attributes were not populated."
        raise OSError(reason)

    return PeekBamResult(read_lengths, paired)


def samtools_view(file_name, param, prog_path, postpend=""):
    """
    Run samtools view, with flexible parameters and post-processing.

    This is used to implement the various read counting functions.

    :param str file_name: name/path of reads tile to use
    :param str param: String of parameters to pass to samtools view
    :param str prog_path: path to the samtools program
    :param str postpend: String to append to the samtools command;
        useful to add cut, sort, wc operations to the samtools view output.
    :return str: terminal-like text output
    """
    cmd = "{prog} view {opts} {f} {extra}".format(
            prog=prog_path, opts=param, f=file_name, extra=postpend)
    # in python 3, check_output returns a byte string which causes issues.
    # with python 3.6 we could use argument: "encoding='UTF-8'""
    return subprocess.check_output(cmd, shell=True).decode().strip()
