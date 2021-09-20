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
