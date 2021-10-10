import math


def indent(string):
    return '\n'.join('    ' + x for x in string.splitlines())


def partition(pred, seq):
    a, b = [], []
    for item in seq:
        (a if pred(item) else b).append(item)
    return a, b


def _cuda_version(version):
    version = float(version)
    major = math.floor(version)
    minor = version - major
    return str(int(major * 1000 + minor * 100))


def compat_section_header(version, added_or_removed):
    version1 = _cuda_version(version)
    if added_or_removed == 'added':
        return f'''#if CUDA_VERSION < {version1}
// Added in CUDA {version}'''
    elif added_or_removed == 'removed':
        return f'''#if CUDA_VERSION >= {version1}
// Removed in CUDA {version}'''
    else:
        raise ValueError('Invalid value')


def compat_section_footer(version, added_or_removed):
    version1 = _cuda_version(version)
    if added_or_removed == 'added':
        return f'#endif  // #if CUDA_VERSION < {version1}'
    elif added_or_removed == 'removed':
        return f'#endif  // #if CUDA_VERSION >= {version1}'
    else:
        raise ValueError('Invalid value')
