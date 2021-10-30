import itertools
import re

from gen import _environment
from gen import _pycparser


def _hip_name(name, prefix, pattern):
    match = pattern.fullmatch(name)
    assert match
    return prefix + match[1]


def _mutually_disjoint(*others):
    return all(a.isdisjoint(b) for a, b in itertools.combinations(others, 2))


def _difference1(A, B, func):
    # S = { a \in A | \forall a' \in f(a) : a' \notin B }
    return {a for a in A if not any(a1 in B for a1 in func(a))}


def _analyze_func_decls(cuda_nodes, hip_nodes, config):
    pattern = re.compile(config['cuda']['patterns']['function'])

    # Collect function configuration, where `conf_map1` has the same items as
    # `conf_map` but the generic '<t>' is expanded.
    conf_map = config['functions']
    conf_map1 = {}
    for name, value in conf_map.items():
        if '<t>' in name:
            for x in 'SDCZ':
                name1 = name.replace('<t>', x)
                conf_map1[name1] = value
        else:
            conf_map1[name] = value
    conf_set, conf_list = set(conf_map), list(conf_map)
    conf_set1, conf_list1 = set(conf_map1), list(conf_map1)  # NOQA

    # Collect CUDA functions
    cuda_headers = config['cuda']['headers']
    cuda_lib_name = re.fullmatch(r'([a-z]+)[_.].*', cuda_headers[0])[1]
    cuda_map = {}
    for version, nodes in cuda_nodes:
        for node in nodes:
            if not _pycparser.is_func_decl_node(node):
                continue

            # Choose functions declared in header files of the library.
            if cuda_lib_name not in str(node.coord):
                continue

            name = _pycparser.function_name(node, strip_suffix=True)
            match = pattern.fullmatch(name)
            if match is None:
                continue

            if name not in cuda_map:
                cuda_map[name] = dict(node=None, versions=[])
            cuda_map[name]['node'] = node
            cuda_map[name]['versions'].append(version)
    cuda_set, cuda_list = set(cuda_map), list(cuda_map)

    # Collect HIP functions
    hip_headers = config['hip']['headers']
    hip_lib_name = re.fullmatch(r'([a-z]+)[_.].*', hip_headers[0])[1]
    hip_map = {}
    for version, nodes in hip_nodes:
        for node in nodes:
            if not _pycparser.is_func_decl_node(node):
                continue

            # Choose functions declared in header files of the library.
            if hip_lib_name not in str(node.coord):
                continue

            name = _pycparser.function_name(node)
            if name not in hip_map:
                hip_map[name] = dict(node=None, versions=[])
            hip_map[name]['node'] = node
            hip_map[name]['versions'].append(version)
    hip_set, hip_list = set(hip_map), list(hip_map)  # NOQA

    # For information, show CUDA functions added or removed in the range of
    # supplied versions
    versions = [version for version, _ in config['cuda']['versions']]
    for old, new in zip(versions[:-1], versions[1:]):
        def pred_added(name, old, new):
            versions_ = cuda_map[name]['versions']
            return old not in versions_ and new in versions_
        s = {x for x in cuda_set if pred_added(x, old, new)}
        for name in sorted(s, key=cuda_list.index):
            print(f"'{name}' is added in version {new}")

        def pred_removed(name, old, new):
            versions_ = cuda_map[name]['versions']
            return old in versions_ and new not in versions_
        s = {x for x in cuda_set if pred_removed(x, old, new)}
        for name in sorted(s, key=cuda_list.index):
            print(f"'{name}' is removed in version {new}")

    # For information, show functions which appear in the configuration only
    def aux1(name):
        if '<t>' in name:
            return {name.replace('<t>', x) for x in 'SDCZ'}
        else:
            return {name}
    s = _difference1(conf_set, cuda_set, aux1)
    for name in sorted(s, key=conf_list.index):
        msg = (f"'{name}' appears in the configuration, but does not in the "
               'header files.')
        print(msg)

    # Inversely, show functions which appear in the CUDA headers only
    s = cuda_set - conf_set1
    for name in sorted(s, key=cuda_list.index):
        print(f"'{name}' does not appear in the configuration. Skip.")

    # Make the returning dictionary having the information of the functions
    s = cuda_set & conf_set1
    ret_map = {}
    for name in sorted(s, key=cuda_list.index):
        if conf_map1[name] == 'skip':
            print(f"Skip '{name}'")
            continue
        ret_map[name] = {
            'node': cuda_map[name]['node'],
            'versions': cuda_map[name]['versions'],
        }
        for key in ['return', 'stream', 'except', 'except?']:
            if key in conf_map1[name]:
                ret_map[name][key] = conf_map1[name][key]
    ret_set, ret_list = set(ret_map), list(ret_map)  # NOQA

    # Update the returning dictionary to have the information about HIP
    s1 = {x for x in ret_set if conf_map1[x].get('hip') == 'skip'}
    s2 = {x for x in ret_set if conf_map1[x].get('hip') == 'not-supported'}
    s3 = {x for x in ret_set if conf_map1[x].get('hip') is None}
    def aux2(name):
        # FIXME: other HIP libraries
        hip_name = _hip_name(name, 'hipblas', pattern)
        return {hip_name}
    s4 = _difference1(s3, hip_set, aux2)
    s5 = s3 - s4
    assert s1 | s2 | s4 | s5 == ret_set
    assert _mutually_disjoint(s1, s2, s4, s5)

    for name in s1:
        ret_map[name]['hip'] = 'skip'

    for name in s2:
        ret_map[name]['hip'] = 'not-supported'

    for name in s4:
        ret_map[name]['hip'] = 'not-supported'

    for name in s5:
        # FIXME: other HIP libraries
        hip_name = _hip_name(name, 'hipblas', pattern)
        ret_map[name]['hip'] = {
            'node': hip_map[hip_name]['node'],
            'versions': hip_map[hip_name]['versions'],
        }

    return ret_map


def _collect_enum_decls(headers, hip_headers, config):
    pattern = re.compile(config['cuda']['patterns']['type'])
    cuda_headers = config['cuda']['headers']
    decls = {}
    for version, nodes in headers:
        for node in nodes:
            if not _pycparser.is_enum_decl_node(node):
                continue

            # Assuming the letters before the first appearance of `_` or `.`
            # make the library name.
            lib_name = re.fullmatch(r'([a-z]+)[_.].*', cuda_headers[0])[1]
            if lib_name not in str(node.coord):
                continue

            name = _pycparser.enum_name(node)
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
    cuda_headers = config['cuda']['headers']
    decls = {}
    for version, nodes in headers:
        for node in nodes:
            if not _pycparser.is_opaque_type_decl_node(node):
                continue

            # Assuming the letters before the first appearance of `_` or `.`
            # make the library name.
            lib_name = re.fullmatch(r'([a-z]+)[_.].*', cuda_headers[0])[1]
            if lib_name not in str(node.coord):
                continue

            name = _pycparser.opaque_type_name(node)
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
        if match is not None:
            hip_name = 'hipblas' + match[1] + '_t'
        else:
            hip_name = name
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
    func_decls = _analyze_func_decls(headers, hip_headers, config)
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
