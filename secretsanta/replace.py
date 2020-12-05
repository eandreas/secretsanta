# AUTOGENERATED! DO NOT EDIT! File to edit: 02_replace.ipynb (unless otherwise specified).

__all__ = ['get_variables', 'replace_vars']

# Cell
import re

# Cell
def get_variables(s, key = '@@'):
    'Returns a set of variables found within string `s` and signed by heading and training `key`s.'
    return set(re.findall(fr'{key}(.*?){key}', s))

# Cell
def replace_vars(s, r, key = '@@'):
    '''A dictionary `r` is used to replace the dictionary keys(surrounded by `key`)
    by the dictionary values.'''
    for k, v in r.items():
        s = s.replace(key + k + key, v)
    return s