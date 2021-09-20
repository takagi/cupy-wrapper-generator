import os.path
import tempfile

import pycparser

import gen


def _parse_headers(filenames, include_path, cuda_or_hip):
    package_path = f'{gen.__path__[0]}/'
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_c_path = os.path.join(temp_dir, 'temp.c')
        with open(temp_c_path, 'w') as f:
            for filename in filenames:
                f.write(f'#include <{filename}>\n')
        cpp_args = [f'-I{include_path}',
                    f'-I{package_path}include/',  # for fake libc headers
                    '-D __attribute__(n)=',
                    '-D __inline__=']
        if cuda_or_hip == 'hip':
            cpp_args.append('-D __HIP_PLATFORM_HCC__')  # 4.1 or earlier
            cpp_args.append('-D __HIP_PLATFORM_AMD__')
        ast = pycparser.parse_file(
            temp_c_path, use_cpp=True, cpp_args=cpp_args)
        return ast


def parse_headers(config, cuda_or_hip):
    if cuda_or_hip not in ['cuda', 'hip']:
        raise ValueError('Invalid value')

    versions = sorted(config['versions'], key=lambda x: x[0])
    filenames = config['headers']

    ret = []
    for version, include_path in versions:
        print(f'Parsing {cuda_or_hip.upper()} {version} header files '
              f'in {include_path}...')
        ast = _parse_headers(filenames, include_path, cuda_or_hip)
        ret.append((version, ast))

    return ret
