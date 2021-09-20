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
