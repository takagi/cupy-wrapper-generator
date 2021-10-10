import re

from gen import _environment
from gen import _pycparser


def _collect_func_decls(headers, config):
    pattern = re.compile(config['patterns']['function'])
    decls = {}
    skip_list = []
    for version, nodes in headers:
        for node in nodes:
            if not _pycparser.is_func_decl_node(node):
                continue

            name = _pycparser.function_name(node)
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
                decls[name] = dict(node=None, versions=[], **func_config)
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

    return decls


def _collect_enum_decls(headers, config):
    pattern = re.compile(config['patterns']['type'])
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

    return decls


def _collect_opaque_type_decls(headers, config):
    pattern = re.compile(config['patterns']['type'])
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

    return decls


def analyze_headers(headers, config):
    versions = [version for version, _ in headers]
    patterns = config['patterns']

    print('Collecting functions...')
    func_decls = _collect_func_decls(headers, config)
    print(f'Collected {len(func_decls)} function(s)')

    print('Collecting opaque types...')
    opaque_type_decls = _collect_opaque_type_decls(headers, config)
    print(f'Collected {len(opaque_type_decls)} opaque type(s)')

    print('Collecting enums...')
    enum_decls = _collect_enum_decls(headers, config)
    print(f'Collected {len(enum_decls)} enum(s)')

    return _environment.make_environment(
        versions, patterns, func_decls, enum_decls, opaque_type_decls)
