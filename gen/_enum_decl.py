from gen import _environment
from gen import _pycparser


def cupy_type(node, env):
    name = _pycparser.enum_name(node)
    pattern = _environment.environment_type_pattern(env)
    return pattern.fullmatch(name)[1]


def erased_type(node):
    assert _pycparser.is_enum_decl_node(node)
    return 'int'


def cuda_type(node):
    return _pycparser.enum_name(node)


def hip_type(node, env):
    cuda_name = _pycparser.enum_name(node)
    hip_node = _environment.environment_enum_hip_node(cuda_name, env)
    return _pycparser.enum_name(hip_node)
