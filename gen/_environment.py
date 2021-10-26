import re

from gen import _pycparser
from gen import _return_spec


# Constructor

def make_environment(
        versions, pattern, func_decls, enum_decls, opaque_type_decls):
    env = {}
    env['versions'] = versions
    env['patterns'] = {
        'function': re.compile(pattern['function']),
        'type': re.compile(pattern['type']),
    }
    env['functions'] = func_decls
    env['enums'] = enum_decls
    env['opaques'] = opaque_type_decls
    return env


# Versions

def environment_versions(env):
    return env['versions']


# Patterns

def environment_function_pattern(env):
    return env['patterns']['function']


def environment_type_pattern(env):
    return env['patterns']['type']


# Functions

def environment_functions(env):
    return env['functions'].keys()


def environment_is_function(name, env):
    return name in env['functions']


def _environment_function(name, env):
    try:
        return env['functions'][name]
    except KeyError:
        raise ValueError(f"'{name}' not found")


def environment_function_node(name, env):
    return _environment_function(name, env)['node']


def _environment_function_versions(name, env):
    return _environment_function(name, env)['versions']


def environment_functions_diff(env, old_version, new_version):
    added = []
    removed = []
    for name in environment_functions(env):
        versions = _environment_function_versions(name, env)
        if old_version not in versions and new_version in versions:
            added.append(name)
        if old_version in versions and new_version not in versions:
            removed.append(name)
    return added, removed


# FIXME
def environment_function_cupy_name(name, env):
    return None


def environment_function_return_spec(name, env):
    try:
        return _environment_function(name, env)['return']
    except KeyError:
        raise ValueError('Return spec required')


def environment_function_stream_spec(name, env):
    def _ensure_stream_spec(spec):
        if spec == 'set':
            return 'set', 'setStream'
        else:
            return spec
    stream_spec = _ensure_stream_spec(
        _environment_function(name, env).get('stream', None))
    if stream_spec is None:
        return False, None, None
    elif len(stream_spec) == 2 and stream_spec[0] == 'set':
        return True, 'set', stream_spec[1]
    elif stream_spec == 'pass':
        return True, 'pass', None
    else:
        raise ValueError('Invalid stream spec')


def environment_function_except(name, env):
    ret_spec = environment_function_return_spec(name, env)
    func = _environment_function(name, env)
    if _return_spec.is_none(ret_spec):
        assert 'except' not in func and 'except?' not in func
        return None
    elif _return_spec.is_transparent(ret_spec):
        assert 'except' not in func and 'except?' not in func
        return None
    elif _return_spec.is_single(ret_spec):
        excpt = func.get('except?')
        if excpt is not None:
            assert 'except' not in func  # either 'except?' or 'except'
            return f'except? {excpt}'
        excpt = func.get('except')
        if excpt is not None:
            return f'except {excpt}'
        assert "Either 'except?' or 'except' must be given"
    elif _return_spec.is_multi(ret_spec):
        assert 'except' not in func and 'except?' not in func
        raise NotImplementedError()
    else:
        assert False


def environment_function_hip_spec(name, env):
    func_hip = _environment_function(name, env).get('hip')
    if func_hip is None:
        return False, None, None
    # ...
    return True, None, None


def environment_function_hip_name(name, env):
    func_hip = _environment_function(name, env).get('hip')
    if func_hip is None:
        raise ValueError('HIP counterpart not found')
    return func_hip['name']


def environment_function_hip_guard(name, env):
    return None


# Enums

def environment_enums(env):
    return env['enums'].keys()


def environment_is_enum(name, env):
    return name in env['enums']


def _environment_enum(name, env):
    try:
        return env['enums'][name]
    except KeyError:
        raise ValueError(f"'{name}' not found")


def environment_enum_node(name, env):
    return _environment_enum(name, env)['node']


def _environment_enum_versions(name, env):
    return _environment_enum(name, env)['versions']


def environment_enums_diff(env, old_version, new_version):
    added = []
    removed = []
    for name in environment_enums(env):
        versions = _environment_enum_versions(name, env)
        if old_version not in versions and new_version in versions:
            added.append(name)
        if old_version in versions and new_version not in versions:
            removed.append(name)
    return added, removed


def environment_status_enum_node(env):
    for name in environment_enums(env):
        enum_node = environment_enum_node(name, env)
        if _pycparser.is_status_enum_decl_node(enum_node):
            return enum_node
    raise ValueError('Status enum not found')


_HIP_TRANSPARENT_ENUMS = [
    'hipblasStatus_t',
    'hipblasPointerMode_t',
    'hipblasAtomicsMode_t',
]


def environment_enum_hip_spec(name, env):
    enum_hip = _environment_enum(name, env).get('hip')
    if enum_hip is None:
        return False, False, None, None
    # ...
    hip_name = enum_hip['name']
    is_transparent = hip_name in _HIP_TRANSPARENT_ENUMS
    return True, is_transparent, None, None


def environment_enum_hip_name(name, env):
    enum_hip = _environment_enum(name, env).get('hip')
    if enum_hip is None:
        raise ValueError('HIP counterpart not found')
    return enum_hip['name']


def environment_status_enum_hip_not_supported(env):
    return 'HIPBLAS_STATUS_NOT_SUPPORTED'


# Opaque types

def environment_opaque_types(env):
    return env['opaques'].keys()


def environment_is_opaque_type(name, env):
    return name in env['opaques']


def _environment_opaque_type(name, env):
    try:
        return env['opaques'][name]
    except KeyError:
        raise ValueError(f"'{name}' not found")


def environment_opaque_type_node(name, env):
    return _environment_opaque_type(name, env)['node']


def _environment_opaque_type_versions(name, env):
    return _environment_opaque_type(name, env)['versions']


def environment_opaque_types_diff(env, old_version, new_version):
    added = []
    removed = []
    for name in environment_opaque_types(env):
        versions = _environment_opaque_type_versions(name, env)
        if old_version not in versions and new_version in versions:
            added.append(name)
        if old_version in versions and new_version not in versions:
            removed.append(name)
    return added, removed


def environment_opaque_type_hip_spec(name, env):
    opaque_hip = _environment_opaque_type(name, env).get('hip')
    if opaque_hip is None:
        return False, None, None
    # ...
    return True, None, None


def environment_opaque_type_hip_name(name, env):
    opaque_hip = _environment_opaque_type(name, env).get('hip')
    if opaque_hip is None:
        raise ValueError('HIP counterpart not found')
    return opaque_hip['name']
