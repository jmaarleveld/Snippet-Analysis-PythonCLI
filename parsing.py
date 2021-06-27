from cache import cache
from rascal import *


def maybe_invoke_parser(repo, repo_name, context, method, max_):
    """Parse diffs from the given repo with the given settings.
    """
    invoke_rascal(PARSER,
                  dir=rascalize_path(cache.retrieve(repo, context, method)),
                  out=rascalize_path(get_data_file(repo_name, context, method, max_)),
                  max=max_,
                  links=rascalize_path(get_link_info(repo_name, context, method)))
