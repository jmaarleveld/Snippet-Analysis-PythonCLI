import json
import os
import warnings

import config

import git
import unidiff
import unidiff.errors
from config import *
from cache import cache


def ensure_diffs(repo, repo_name, context, diff_method, unicode_policy):
    """Ensure that the diff_tools from the specified repository with the
    specified context and diff method are present on the file system
    in their default directory.
    """
    if (repo, context, diff_method) not in cache:
        target_dir = get_diff_dir(os.path.split(repo)[1], context, diff_method)
        load_diffs(repo,
                   target_dir,
                   get_link_info(repo_name, context, diff_method),
                   context, diff_method, unicode_policy)
        #diffs_to_json(target_dir)
        cache.store(target_dir, repo, context, diff_method)
    else:
        location = cache.retrieve(repo, context, diff_method)


def load_diffs(source, target, link_file, ctx, algorithm, error_policy='strict'):
    """Load the history from a given repository and populate the
    given target directory with files containing the diff_tools
    from said repository.

    The ctx and algorithm parameters are used to configure
    the git algorithm.
    """
    print('Generating diffs')
    os.makedirs(target, exist_ok=True)
    repository = git.Repo(source)
    commits = list(repository.iter_commits('master'))
    commits.reverse()  # From oldest to newest
    prev = commits[0]
    skipped = 0
    link_info = {}
    for i, commit in enumerate(commits[1:]):
        name = f'{commit.authored_datetime}_{commit.hexsha}.txt'
        name = name.replace(':', '_').replace(' ', '__')
        with open(os.path.join(target, name), 'w', encoding='utf8', errors=error_policy) as fd:
            try:
                diff_text = repository.git.diff(prev, commit,
                                                f'-U{ctx}',
                                                f'--diff-algorithm={algorithm}')
                fd.write(fix_diff(diff_text))
            except UnicodeEncodeError as e:
                message = f'Skipped diffing commit due to unicode error: {commit.hexsha}'
                warnings.warn(message,
                              stacklevel=2)
                skipped += 1
            else:
                link_info[name] = {'old': prev.hexsha, 'new': commit.hexsha}
            print(f'{i + 1} / {len(commits) - 1}', end='\r')
        prev = commit
    with open(link_file, 'w') as file:
        json.dump(link_info, file)
    print()
    print(f'Generated Diffs (skipped {skipped})')


def fix_diff(diff_text: str):
    return '\n'.join(line for line in diff_text.splitlines(keepends=False) if line)


def diffs_to_json(directory, *, clean=False):
    """Convert all files in a directory (which are assumed to be diff_tools),
    into JSON representations of those diff_tools.

    If clean is True, all old files are removed after parsing.
    """
    diffs = list(os.listdir(directory))
    skipped = 0
    print(f'Converting {len(diffs)} files to JSON...')
    for i, diff in enumerate(diffs, start=1):
        print(f'{i} / {len(diffs)}', end='\r')
        diff_name, _ = os.path.splitext(diff)
        path = os.path.join(directory, diff)
        try:
            patch = unidiff.PatchSet.from_filename(path, encoding='utf8')
        except unidiff.errors.UnidiffParseError:
            message = (f'Skipped diff due to parsing error: {diff}\n'
                       'This error is typically caused by ambiguous new lines'
                       '(i.e. carriage returns)')
            warnings.warn(message, stacklevel=2)
            skipped += 1
            continue
        with open(os.path.join(directory, diff_name + '.json'), 'w') as fd:
            json.dump(patch_to_json(patch), fd, indent=4)
    if clean:
        print('Cleaning up diff files...')
        for file in diffs:
            os.remove(file)
    print()
    print(f'Finished converting (skipped {skipped})')


def patch_to_json(patch):
    return [file_to_json(file_patch) for file_patch in patch]


def file_to_json(file_patch):
    return {
        'old': file_patch.source_file,
        'new': file_patch.target_file,
        'is_new': file_patch.is_added_file,
        'is_removed': file_patch.is_removed_file,
        'is_modified': file_patch.is_modified_file,
        'is_binary': file_patch.is_binary_file,
        'hunks': [hunk_to_json(hunk) for hunk in file_patch]
    }


def hunk_to_json(hunk):
    return {
        'source_start': hunk.source_start,
        'source_length': hunk.source_length,
        'target_start': hunk.target_start,
        'target_length': hunk.target_length,
        'lines': [line_to_json(line) for line in hunk]
    }


def line_to_json(line):
    return {
        'is_added': line.is_added,
        'is_removed': line.is_removed,
        'is_shared': line.is_context,
        'content': line.value[:-1]  # Remove trailing newline
    }
