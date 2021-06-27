import os
import subprocess
import shlex

from config import *


def rascalize_path(path, typ='file'):
    """Convert a path so that it can be passed to rascal as an argument."""
    path = path.replace("\\", '/')
    return f'"{typ}:///{path}"'


def _rascalize(x):
    if isinstance(x, bool):
        return 'true' if x else 'false'
    if isinstance(x, int):
        return x
    return x


def invoke_rascal(file, **kwargs):
    base_command = f'{JAVA_PATH} -Xmx1G -Xss32m -jar "{RASCAL}"'
    args = ' '.join(f'-{key} {_rascalize(value)}' for key, value in kwargs.items())
    old_dir = os.getcwd()
    path, file = os.path.split(file)
    os.chdir(path)
    command = f'{base_command} {file} {args}'
    print('Invoking rascal with:')
    print(command)
    code = subprocess.call(shlex.split(command))
    os.chdir(old_dir)
    if code != 0:
        raise RuntimeError('Call to Rascal failed')
