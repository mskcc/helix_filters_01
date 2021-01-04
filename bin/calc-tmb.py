#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to calculate TMB tumor mutational burden value

num_variants / bases_covered * 1,000,000 = TMB in Megabases
"""
import sys
import argparse

def calc_from_values(num_variants, genome_coverage, megabases = False, _print = False, func = None):
    """
    """
    # print(num_variants, genome_coverage, megabases, _print)
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

    return(tmb)

def parse():
    """
    Parse command line arguments to run the script
    """
    # top level CLI arg parser; args common to all output files go here
    parser = argparse.ArgumentParser(description = 'Calculate the TMB tumor mutational burden')

    # add sub-parsers for specific file outputs
    subparsers = parser.add_subparsers(help ='Sub-commands available')

    from_values = subparsers.add_parser('from-values', help = 'Calculate the TMB in Megabases from values passed')
    from_values.add_argument('--num-variants', dest = 'num_variants', required = True, help = 'Number of variants')
    from_values.add_argument('--genome-coverage', dest = 'genome_coverage', required = True, help = 'Number of base pairs of the genome covered by the assay')
    from_values.add_argument('--raw', dest = 'megabases', action='store_false', help = 'Return the raw TMB value instead of the value in Megabases')
    from_values.add_argument('--no-print', dest = '_print', action='store_false', help = 'Dont print the output')
    from_values.set_defaults(func = calc_from_values)

    args = parser.parse_args()
    args.func(**vars(args))

if __name__ == '__main__':
    parse()
