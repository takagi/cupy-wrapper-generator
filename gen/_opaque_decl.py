from gen import _environment
from gen import _pycparser


def cupy_type(node, env):
    name = _pycparser.opaque_type_name(node)
    pattern = _environment.environment_type_pattern(env)
    return pattern.fullmatch(name)[1]


def erased_type(node):
    assert _pycparser.is_opaque_type_decl_node(node)
    return 'void*'


def cuda_type(node):
    return _pycparser.opaque_type_name(node)


def hip_type(node, env):
    cuda_name = _pycparser.opaque_type_name(node)
    hip_node = _environment.environment_opaque_type_hip_node(cuda_name, env)
    return _pycparser.opaque_type_name(hip_node)
