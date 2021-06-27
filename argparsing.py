import argparse
import collections


description = f"""
Git Diff Parser --- Command Line Interface

{'-' * 30}
Workflow

This command line tool can be used as a full pipeline to generate data
from Git repositories. Typical usage would 
be to specify a repository (using -d), the maximum amount of diffs to 
parse (-m), the diff algorithm (--diff-method) and the amount of 
context lines to include in diffs (-c, a list of numbers). 
The handling of unicode errors can be configured using the 
--unicode-policy argument.

If the parsing process has already been completed, but the data only
has to be processed further, then the --skip-parsing flag may be
supplied. This causes parsing to be skipped, and other data processing 
will be started.

The --details argument can be supplied in order to start the snippet
browser. This is a GUI in which one is able to browse through all 
parsed snippets, by classification category. Note that only one 
number is allowed to be passed for -c/--context if --details is 
given.

If one wishes to benchmark the snippet parsing, this should be done 
by explicitly enabling benchmarking by passing the --benchmark flag.
The --rounds parameter can be used to configure how often each snippet 
or file is parsed during the benchmark.
"""

parser = argparse.ArgumentParser(description=description,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('--skip-parsing', default=False, action='store_true',
                    help='Skip parsing of data. Only try to process existing files')
parser.add_argument('-d', '--directory', type=str, required=False,
                    help='Repository to pull diff_tools from')
parser.add_argument('-c', '--context', type=int, required=False, nargs='+',
                    help='Number of lines of context to include')
parser.add_argument('-m', '--max', type=int, required=False, default=100,
                    help='Number of files to process')
parser.add_argument('--diff-method', type=str, default='myers',
                    help='Git algorithm to use (default/myers, minimal, patience, histogram)')
parser.add_argument('--details', default=False, action='store_true',
                    help='View detailed output')
parser.add_argument('--unicode-policy', default='strict',
                    help=('Set unicode policy for diff generation. '
                          'Can be any unicode error handling supported by Python'))
parser.add_argument('--benchmark', default=False, action='store_true',
                    help='Perform benchmarking')
parser.add_argument('-r', '--rounds', default=5, required=False, type=int,
                    help='Amount of rounds to use for benchmarking')
