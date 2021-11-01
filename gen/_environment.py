import re

from gen import _hip
from gen import _pycparser
from gen import _return_spec
import gen.util


# Constructor

def make(versions, hip_versions, pattern, func_decls, enum_decls,
         opaque_type_decls):
    env = {}
    env['versions'] = versions
    env['hip-versions'] = hip_versions
    env['patterns'] = {
        'function': re.compile(pattern['function']),
        'type': re.compile(pattern['type']),
    }
    env['functions'] = func_decls
    env['enums'] = enum_decls
    env['opaques'] = opaque_type_decls
    return env


# Versions

def versions(env):
    return env['versions']


def _hip_versions(env):
    return env['hip-versions']


# Patterns

def function_pattern(env):
    return env['patterns']['function']


def type_pattern(env):
    return env['patterns']['type']


# Functions

def functions(env):
    return env['functions'].keys()


def is_function(name, env):
    return name in env['functions']


def _function(name, env):
    try:
        return env['functions'][name]
    except KeyError:
        raise ValueError(f"'{name}' not found")


def function_node(name, env):
    return _function(name, env)['node']


def _function_versions(name, env):
    return _function(name, env)['versions']


def functions_diff(env, old_version, new_version):
    added = []
    removed = []
    for name in functions(env):
        versions = _function_versions(name, env)
        if old_version not in versions and new_version in versions:
            added.append(name)
        if old_version in versions and new_version not in versions:
            removed.append(name)
    return added, removed


# FIXME
def function_cupy_name(name, env):
    return None


def function_return_spec(name, env):
    try:
        return _function(name, env)['return']
    except KeyError:
        raise ValueError('Return spec required')


def function_stream_spec(name, env):
    def _ensure_stream_spec(spec):
        if spec == 'set':
            return 'set', 'setStream'
        else:
            return spec
    stream_spec = _ensure_stream_spec(_function(name, env).get('stream', None))
    if stream_spec is None:
        return False, None, None
    elif len(stream_spec) == 2 and stream_spec[0] == 'set':
        return True, 'set', stream_spec[1]
    elif stream_spec == 'pass':
        return True, 'pass', None
    else:
        raise ValueError('Invalid stream spec')


def function_except(name, env):
    ret_spec = function_return_spec(name, env)
    func = _function(name, env)
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

        # A default error return value if possible
        out_name = _return_spec.single_return_spec(ret_spec)
        arg_nodes = _pycparser.function_arg_nodes(func['node'])
        out_nodes, _ = gen.util.partition(
            lambda n: _pycparser.argument_name(n) == out_name, arg_nodes)
        assert len(out_nodes) == 1
        out_node = out_nodes[0]
        out_type_node = _pycparser.argument_type_node(out_node)
        out_base_type_node = _pycparser.type_base_type(out_type_node)
        out_base_type_name = _pycparser.type_name(out_base_type_node)
        if out_base_type_name == 'cudaStream_t':
            # TODO(takgi) Isn't 'except -1' enough for cudaStream_t?
            return f'except? 0'
        if is_opaque_type(out_base_type_name, env):
            return f'except? 0'
        if is_enum(out_base_type_name, env):
            # TODO(takagi) Sould it be 'except?' instead of 'except'? Some CUDA
            # enums have -1 as their actual values, though.
            return f'except? -1'

        raise ValueError("Either 'except?' or 'except' must be given")
    elif _return_spec.is_multi(ret_spec):
        assert 'except' not in func and 'except?' not in func
        raise NotImplementedError()
    else:
        assert False


def function_hip_node(name, env):
    func_hip = _function(name, env).get('hip')
    if func_hip is None:
        raise ValueError('HIP counterpart not found')
    return func_hip['node']


def _convert_hip_since(version):
    major, minor = map(int, version.split('.'))
    if major < 4 or major == 4 and minor < 4:
        return major * 100 + minor
    else:
        return major * 10000000 + minor * 100000


def _convert_hip_until(version):
    major, minor = map(int, version.split('.'))
    if major < 4 or major == 4 and minor < 3:
        return major * 100 + minor
    else:
        return major * 10000000 + minor * 100000


def _compute_hip_since_until(versions, env):
    all_versions = _hip_versions(env)
    since, until = None, None
    if versions[0] != all_versions[0]:
        since = _convert_hip_since(versions[0])
    if versions[-1] != all_versions[-1]:
        index = all_versions.find(versions[-1])
        until = _convert_hip_until(all_versions[index + 1])
    return since, until


def function_hip_spec(name, env):
    func_hip = _function(name, env)['hip']
    if func_hip == 'skip':
        return True, None, None, None
    elif func_hip == 'not-supported':
        return False, False, None, None
    else:
        versions = func_hip['versions']
        since, until = _compute_hip_since_until(versions, env)
        return False, True, since, until


# Enums

def enums(env):
    return env['enums'].keys()


def is_enum(name, env):
    return name in env['enums']


def _enum(name, env):
    try:
        return env['enums'][name]
    except KeyError:
        raise ValueError(f"'{name}' not found")


def enum_node(name, env):
    return _enum(name, env)['node']


def _enum_versions(name, env):
    return _enum(name, env)['versions']


def enums_diff(env, old_version, new_version):
    added = []
    removed = []
    for name in enums(env):
        versions = _enum_versions(name, env)
        if old_version not in versions and new_version in versions:
            added.append(name)
        if old_version in versions and new_version not in versions:
            removed.append(name)
    return added, removed


def status_enum_node(env):
    for name in enums(env):
        enum_node_ = enum_node(name, env)
        if _pycparser.is_status_enum_decl_node(enum_node_):
            return enum_node_
    raise ValueError('Status enum not found')


def status_enum_name(env):
    node = status_enum_node(env)
    return _pycparser.enum_name(node)


def status_enum_success(env):
    node = status_enum_node(env)
    return _pycparser.status_enum_success(node)


def enum_hip_node(name, env):
    enum_hip = _enum(name, env).get('hip')
    if enum_hip is None:
        raise ValueError('HIP counterpart not found')
    return enum_hip['node']


def enum_hip_spec(name, env):
    enum_hip = _enum(name, env).get('hip')
    if enum_hip is None:
        return False, None, None, None
    hip_node = enum_hip['node']
    hip_name = _pycparser.enum_name(hip_node)
    is_transparent = hip_name in _hip.HIP_TRANSPARENT_ENUMS
    versions = enum_hip['versions']
    since, until = _compute_hip_since_until(versions, env)
    return True, is_transparent, since, until


def status_enum_hip_not_supported(env):
    # FIXME: other HIP libraries
    return 'HIPBLAS_STATUS_NOT_SUPPORTED'


# Opaque types

def opaque_types(env):
    return env['opaques'].keys()


def is_opaque_type(name, env):
    return name in env['opaques']


def _opaque_type(name, env):
    try:
        return env['opaques'][name]
    except KeyError:
        raise ValueError(f"'{name}' not found")


def opaque_type_node(name, env):
    return _opaque_type(name, env)['node']


def _opaque_type_versions(name, env):
    return _opaque_type(name, env)['versions']


def opaque_types_diff(env, old_version, new_version):
    added = []
    removed = []
    for name in opaque_types(env):
        versions = _opaque_type_versions(name, env)
        if old_version not in versions and new_version in versions:
            added.append(name)
        if old_version in versions and new_version not in versions:
            removed.append(name)
    return added, removed


def opaque_type_hip_node(name, env):
    opaque_hip = _opaque_type(name, env).get('hip')
    if opaque_hip is None:
        raise ValueError('HIP counterpart not found')
    return opaque_hip['node']


def opaque_type_hip_spec(name, env):
    opaque_hip = _opaque_type(name, env).get('hip')
    if opaque_hip is None:
        return False, None, None
    versions = opaque_hip['versions']
    since, until = _compute_hip_since_until(versions, env)
    return True, since, until
