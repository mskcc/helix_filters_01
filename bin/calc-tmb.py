#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to calculate TMB tumor mutational burden value

num_variants / bases_covered * 1,000,000 = TMB in Megabases
"""
import sys
import argparse
from cBioPortal_utils import MafReader

def calc_from_values(
    num_variants, # str | float | int
    genome_coverage, # str | float | int
    megabases = False,
    _print = False,
    output_file = None,
    func = None # dummy arg for parser
    ):
    """
    Simple calculation of TMB tumor mutation burden.

    Num variants / bases covered

    Report the result in variants/Megabases unless otherwise specified
    """

    num_variants = int(num_variants)
    genome_coverage = int(genome_coverage)

    if megabases:
        genome_coverage = genome_coverage * 1000000

    tmb = num_variants / genome_coverage

    if _print:
        """
        Need to deal with Python's printing of extremely small numbers;
        https://stackoverflow.com/questions/658763/how-to-suppress-scientific-notation-when-printing-float-values

        >>> x = 1.0 / 1000000000.0
        >>> numpy.format_float_positional(x)
        '0.000000001'
        >>> numpy.format_float_positional(0.25)
        '0.25'
        """
        import numpy
        print(numpy.format_float_positional(tmb))

    if output_file:
        import numpy
        with open(output_file, "w") as f:
            f.write(numpy.format_float_positional(tmb) + '\n')

    return(tmb)

def calc_from_file(
    input_file,
    output_file,
    genome_coverage, # str | float | int
    func = None # dummy arg for parser
    ):
    """
    Wrapper around TMB calc function to use for reading variants from file
    """
    # use some default values
    megabases = True
    _print = False
    # reader for variants in the file
    maf_reader = MafReader(input_file)
    num_variants = maf_reader.count()
    calc_from_values(
        num_variants = num_variants,
        output_file = output_file,
        genome_coverage = genome_coverage,
        megabases = megabases,
        _print = _print
        )

def parse():
    """
    Parse command line arguments to run the script
    """
    # top level CLI arg parser; args common to all output files go here
    parser = argparse.ArgumentParser(description = 'Calculate the TMB tumor mutational burden')

    # add sub-parsers for specific file outputs
    subparsers = parser.add_subparsers(help ='Sub-commands available')

    # parser to calculate TMB from raw values passed on the CLI
    from_values = subparsers.add_parser('from-values', help = 'Calculate the TMB in Megabases from values passed')
    from_values.add_argument('--num-variants', dest = 'num_variants', required = True, help = 'Number of variants')
    from_values.add_argument('--genome-coverage', dest = 'genome_coverage', required = True, help = 'Number of base pairs of the genome covered by the assay')
    from_values.add_argument('--raw', dest = 'megabases', action='store_false', help = 'Return the raw TMB value instead of the value in Megabases')
    from_values.add_argument('--no-print', dest = '_print', action='store_false', help = 'Dont print the output')
    from_values.add_argument('--output-file', dest = 'output_file', help = 'File to write values to')
    from_values.set_defaults(func = calc_from_values)

    # parser to calculate TMB from a variant file passed
    from_file = subparsers.add_parser('from-file', help = 'Calculate the TMB in Megabases from a variant file')
    from_file.add_argument('input_file', help = 'File to read variants from')
    from_file.add_argument('output_file', help = 'File to write TMB value to')
    from_file.add_argument('--genome-coverage', dest = 'genome_coverage', required = True, help = 'Number of base pairs of the genome covered by the assay')
    from_file.set_defaults(func = calc_from_file)


    args = parser.parse_args()
    args.func(**vars(args))

if __name__ == '__main__':
    parse()
