import re

from gen import _environment
from gen import _pycparser


def _collect_func_decls(headers, hip_headers, config):
    pattern = re.compile(config['cuda']['patterns']['function'])
    decls = {}
    skip_list = []
    for version, nodes in headers:
        for node in nodes:
            if not _pycparser.is_func_decl_node(node):
                continue

            name = _pycparser.function_name(node, strip_suffix=True)
            if pattern.fullmatch(name) is None:
                continue
            if name not in config['functions']:
                if name not in skip_list:
                    skip_list.append(name)
                    msg = (f"'{name}' does not appear in the configuration. "
                           'Skip.')
                    print(msg)
                continue

            func_config = config['functions'][name]
            if func_config == 'skip':
                if name not in skip_list:
                    skip_list.append(name)
                    print(f"Skip '{name}'")
                continue

            if name not in decls:
                decls[name] = {'node': None,
                               'versions': [],
                               'hip': 'not-supported'}
                for key in ['return', 'stream', 'except', 'except?', 'hip']:
                    if key in func_config:
                        decls[name][key] = func_config[key]
            decls[name]['node'] = node
            decls[name]['versions'].append(version)

    for name in config['functions']:
        if config['functions'][name] == 'skip':
            continue
        if name not in decls:
            msg = (f"'{name}' appears in the configuration, but does not in "
                   'the header files.')
            print(msg)

    versions = [version for version, _ in headers]
    for old, new in zip(versions[:-1], versions[1:]):
        for name, func in decls.items():
            versions = func['versions']
            if old not in versions and new in versions:
                print(f"'{name}' is added in version {new}")
            elif old in versions and new not in versions:
                print(f"'{name}' is removed in version {new}")

    hip_index = {}
    for name, func in decls.items():
        match = pattern.fullmatch(name)
        hip_name = 'hipblas' + match[1]  # FIXME: other HIP libraries
        hip_index[hip_name] = name, func
    for version, nodes in hip_headers:
        for node in nodes:
            if not _pycparser.is_func_decl_node(node):
                continue

            name = _pycparser.function_name(node)
            foo = hip_index.get(name)
            if foo is None:
                continue
            cuda_name, func = foo

            hip_config = config['functions'][cuda_name].get('hip')
            if hip_config is not None:
                continue
            if func['hip'] == 'not-supported':
                func['hip'] = {'node': None, 'versions': []}
            func['hip']['node'] = node
            func['hip']['versions'].append(version)

    return decls


def _collect_enum_decls(headers, hip_headers, config):
    pattern = re.compile(config['cuda']['patterns']['type'])
    decls = {}
    for version, nodes in headers:
        for node in nodes:
            if not _pycparser.is_enum_decl_node(node):
                continue

            name = _pycparser.enum_name(node)
            if pattern.fullmatch(name) is None:
                continue

            if name not in decls:
                decls[name] = dict(node=None, versions=[])
            decls[name]['node'] = node
            decls[name]['versions'].append(version)

    versions = [version for version, _ in headers]
    for old, new in zip(versions[:-1], versions[1:]):
        for name, enum in decls.items():
            versions = enum['versions']
            if old not in versions and new in versions:
                print(f"'{name}' is added in version {new}")
            if old in versions and new not in versions:
                print(f"'{name}' is removed in version {new}")

    hip_index = {}
    for name, enum in decls.items():
        match = pattern.fullmatch(name)
        hip_name = 'hipblas' + match[1] + '_t'
        hip_index[hip_name] = name, enum
    for version, nodes in hip_headers:
        for node in nodes:
            if not _pycparser.is_enum_decl_node(node):
                continue

            hip_name = _pycparser.enum_name(node)
            foo = hip_index.get(hip_name)
            if foo is None:
                continue
            cuda_name, enum = foo

            if 'hip' not in enum:
                enum['hip'] = {'node': None, 'versions': []}
            enum['hip']['node'] = node
            enum['hip']['versions'].append(version)

    return decls


def _collect_opaque_type_decls(headers, hip_headers, config):
    pattern = re.compile(config['cuda']['patterns']['type'])
    decls = {}
    for version, nodes in headers:
        for node in nodes:
            if not _pycparser.is_opaque_type_decl_node(node):
                continue

            name = _pycparser.opaque_type_name(node)
            if pattern.fullmatch(name) is None:
                continue

            if name not in decls:
                decls[name] = dict(node=None, versions=[])
            decls[name]['node'] = node
            decls[name]['versions'].append(version)

    versions = [version for version, _ in headers]
    for old, new in zip(versions[:-1], versions[1:]):
        for name, opaque in decls.items():
            versions = opaque['versions']
            if old not in versions and new in versions:
                print(f"'{name}' is added in version {new}")
            if old in versions and new not in versions:
                print(f"'{name}' is removed in version {new}")

    hip_index = {}
    for name, opaque in decls.items():
        match = pattern.fullmatch(name)
        hip_name = 'hipblas' + match[1] + '_t'
        hip_index[hip_name] = name, opaque
    for version, nodes in hip_headers:
        for node in nodes:
            if not _pycparser.is_opaque_type_decl_node(node):
                continue

            hip_name = _pycparser.opaque_type_name(node)
            foo = hip_index.get(hip_name)
            if foo is None:
                continue
            cuda_name, opaque = foo

            if 'hip' not in opaque:
                opaque['hip'] = {'node': None, 'versions': []}
            opaque['hip']['node'] = node
            opaque['hip']['versions'].append(version)

    return decls


def analyze_headers(headers, hip_headers, config):
    versions = [version for version, _ in headers]
    hip_versions = [version for version, _ in hip_headers]
    patterns = config['cuda']['patterns']

    print('Collecting functions...')
    func_decls = _collect_func_decls(headers, hip_headers, config)
    print(f'Collected {len(func_decls)} function(s)')

    print('Collecting opaque types...')
    opaque_type_decls = _collect_opaque_type_decls(
        headers, hip_headers, config)
    print(f'Collected {len(opaque_type_decls)} opaque type(s)')

    print('Collecting enums...')
    enum_decls = _collect_enum_decls(headers, hip_headers, config)
    print(f'Collected {len(enum_decls)} enum(s)')

    return _environment.make(
        versions, hip_versions, patterns, func_decls, enum_decls,
        opaque_type_decls)
