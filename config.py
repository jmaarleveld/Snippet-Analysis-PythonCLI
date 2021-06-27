import os
import os.path


def __require_var_set(value, name, description):
    if value is not None:
        return
    print(f'Variable {name} is not set')
    msg = (
        f'In order to prevent this error, please provide a value'
        f' for the variable {name} in config.py.\n'
        f'Detailed variable description:\n{description}'
    )
    print(msg)


BASE_DIR = '.'
__require_var_set(BASE_DIR,
                  'BASE_DIR',
                  'directory in which all data will be stored')
JAVA_PATH = 'java'

DATA_DIR = os.path.join(BASE_DIR, 'data')
DIFF_DIR = os.path.join(BASE_DIR, 'diffs')
BENCH_DIR = os.path.join(BASE_DIR, 'benchmarks')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DIFF_DIR, exist_ok=True)
os.makedirs(BENCH_DIR, exist_ok=True)

CACHE_INFO = os.path.join(BASE_DIR, 'cacheinfo.json')

#RASCAL = os.path.join(BASE_DIR, r'rascal\rascal-shell-stable.jar')
RASCAL = None
__require_var_set(RASCAL,
                  'RASCAL',
                  'Path to a rascal JAR file')
#RASCAL_SOURCE_DIR = os.path.join(BASE_DIR, r'diff-splitter\src')
RASCAL_SOURCE_DIR = None
__require_var_set(RASCAL_SOURCE_DIR,
                  'RASCAL_SOURCE_DIR',
                  'Path to the source directory containing the rascal files'
                  'for the snippet parsing and benchmark program')
PARSER = os.path.join(RASCAL_SOURCE_DIR, 'Parser.rsc')
BENCHMARK = os.path.join(RASCAL_SOURCE_DIR, 'Benchmark.rsc')


def get_data_file(repo, context, algorithm, max_):
    return os.path.join(
        DATA_DIR,
        f'{repo}_context{context}_{algorithm}_m{max_}' + '.json'
    )


def get_bench_file(repo, context, algorithm, max_, top_level):
    suffix = '_top_level' if top_level else ''
    return os.path.join(
        BENCH_DIR,
        f'{repo}_context{context}_{algorithm}_m{max_}{suffix}' + '.json'
    )


def get_diff_dir(repo, context, algorithm):
    return os.path.join(DIFF_DIR, f'{repo}_context{context}_{algorithm}')


def get_link_info(repo, context, algorithm):
    return os.path.join(get_diff_dir(repo, context, algorithm), 'diff_info.json')

