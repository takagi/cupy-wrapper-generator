import os.path
import tempfile

import pycparser

import gen


def parse_headers(config):
    package_path = f'{gen.__path__[0]}/'
    versions = sorted(config['versions'], key=lambda x: x[0])
    filenames = config['headers']

    ret = []
    for version, include_path in versions:
        print(f'Parsing CUDA {version} header files in {include_path}...')
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_c_path = os.path.join(temp_dir, 'temp.c')
            with open(temp_c_path, 'w') as f:
                for filename in filenames:
                    f.write(f'#include <{filename}>\n')
            ast = pycparser.parse_file(temp_c_path, use_cpp=True, cpp_args=[
                f'-I{include_path}',
                f'-I{package_path}include/',  # for fake libc headers
                '-I/usr/local/cuda-11.4.1/include/',
                '-D __HIP_PLATFORM_AMD__',
                '-D __attribute__(n)=',
                '-D __inline__='])
        ret.append((version, ast))

    return ret
