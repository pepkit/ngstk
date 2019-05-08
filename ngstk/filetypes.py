""" Functions related to file type """

import os

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"
__credits = ["Nathan Sheffield", "Andre Rendeiro", "Vince Reuter"]


__all__ = ["get_input_ext", "is_fastq", "is_gzipped_fastq", "is_sam_or_bam",
           "is_unzipped_fastq", "parse_ftype", "UnsupportedFiletypeException"]


def get_input_ext(input_file):
    """
    Get the extension of the input_file.

    This function assumes you're using .bam, .fastq/.fq, or .fastq.gz/.fq.gz.

    :param str input_file: name/path of file for which to get extension
    :return str: standardized extension
    :raise ubiquerg.ngs.UnsupportedFiletypeException: if the given file name
        or path has an extension that's not supported
    """
    if input_file.endswith(".bam"):
        return ".bam"
    elif input_file.endswith(".fastq.gz") or input_file.endswith(".fq.gz"):
        return ".fastq.gz"
    elif input_file.endswith(".fastq") or input_file.endswith(".fq"):
        return ".fastq"
    errmsg = "'{}'; this pipeline can only deal with .bam, .fastq, " \
             "or .fastq.gz files".format(input_file)
    raise UnsupportedFiletypeException(errmsg)


def is_fastq(file_name):
    """
    Determine whether indicated file appears to be in FASTQ format.

    :param str file_name: Name/path of file to check as FASTQ.
    :return bool: Whether indicated file appears to be in FASTQ format, zipped
        or unzipped.
    """
    return is_unzipped_fastq(file_name) or is_gzipped_fastq(file_name)


def is_gzipped_fastq(file_name):
    """
    Determine whether indicated file appears to be a gzipped FASTQ.

    :param str file_name: Name/path of file to check as gzipped FASTQ.
    :return bool: Whether indicated file appears to be in gzipped FASTQ format.
    """
    parts = file_name.split(".")
    return parts[-2:] in [["fq", "gz"], ["fastq", "gz"]]


def is_sam_or_bam(file_name):
    """
    Determine whether a file appears to be in a SAM format.

    :param str file_name: Name/path of file to check as SAM-formatted.
    :return bool: Whether file appears to be SAM-formatted
    """
    _, ext = os.path.splitext(file_name)
    return ext in [".bam", ".sam"]


def is_unzipped_fastq(file_name):
    """
    Determine whether indicated file appears to be an unzipped FASTQ.

    :param str file_name: Name/path of file to check as unzipped FASTQ.
    :return bool: Whether indicated file appears to be in unzipped FASTQ format.
    """
    _, ext = os.path.splitext(file_name)
    return ext in [".fastq", ".fq"]


def parse_ftype(input_file):
    """
    Checks determine filetype from extension.

    :param str input_file: String to check.
    :return str: filetype (extension without dot prefix)
    :raises UnsupportedFiletypeException: if file does not appear of a
        supported type
    """
    if input_file.endswith(".bam"):
        return "bam"
    elif input_file.endswith(".fastq") or \
            input_file.endswith(".fq") or \
            input_file.endswith(".fq.gz") or \
            input_file.endswith(".fastq.gz"):
        return "fastq"
    else:
        raise UnsupportedFiletypeException(
            "Input file extension is neither BAM- nor FASTQ-like: {}".
            format(input_file))


class UnsupportedFiletypeException(Exception):
    """ Restrict domain of file types. """
    # Use superclass ctor to allow file name/path or extension to pass
    # through as the message for why this error is occurring.
    pass
