from diff_utils import ensure_diffs
from parsing import maybe_invoke_parser
from rascal import invoke_rascal, rascalize_path
from json_structures import *
from config import *

##############################################################################
##############################################################################
# Utility
##############################################################################


def get_repo_info(args):
    repo = os.path.abspath(os.path.normpath(args.directory))
    repo_name = os.path.split(repo)[1]
    return repo, repo_name


def ensure_one_context(args, operation):
    if len(args.context) != 1:
        raise ValueError(f'Operation {operation!r} expects exactly one context')


##############################################################################
##############################################################################
# Basic Diff Processing
##############################################################################


def create_diffs(args):
    repo, repo_name = get_repo_info(args)
    for context in args.context:
        ensure_diffs(repo, repo_name, context, args.diff_method, args.unicode_policy)


def parse_diffs(args):
    if args.skip_parsing:
        return
    repo, repo_name = get_repo_info(args)
    for context in args.context:
        maybe_invoke_parser(repo, repo_name, context, args.diff_method, args.max)


##############################################################################
##############################################################################
# Benchmarking
##############################################################################


def perform_benchmark(args):
    if not args.benchmark:
        return
    repo, repo_name = get_repo_info(args)
    for context in args.context:
        invoke_rascal(BENCHMARK,
                      target=rascalize_path(get_bench_file(repo_name, context, args.diff_method, args.max, args.top_level)),
                      source=rascalize_path(get_data_file(repo_name, context, args.diff_method, args.max)),
                      repo=rascalize_path(repo),
                      rounds=args.rounds,
                      useToplevel=args.top_level,
                      countAmbiguity=args.count_ambiguity)


##############################################################################
##############################################################################
# Data analysis
##############################################################################

def open_snippet_browser(args):
    if not args.details:
        return
    ensure_one_context(args, 'snippet_browser')
    repo, repo_name = get_repo_info(args)
    os.environ['KIVY_NO_ARGS'] = '1'
    import snippet_browser

    context = args.context[0]
    with open(get_data_file(repo_name, context, args.diff_method, args.max)) as file:
        data = json_util.read_json(file, JSON_STRUCTURE)
    snippet_browser.set_result(data)
    snippet_browser.run_app()

##############################################################################
##############################################################################
# Main function
##############################################################################


def main(args):
    create_diffs(args)
    parse_diffs(args)
    perform_benchmark(args)
    open_snippet_browser(args)

