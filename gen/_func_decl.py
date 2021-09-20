from gen import _environment
from gen import _pycparser


def cupy_name(node, env):
    cuda_name = _pycparser.function_name(node)
    cupy_name = _environment.environment_function_cupy_name(cuda_name, env)
    if cupy_name is not None:
        return cupy_name
    pattern = _environment.environment_function_pattern(env)
    cupy_name = pattern.fullmatch(cuda_name)[1]
    return cupy_name[0:2].lower() + cupy_name[2:]


def cuda_name(node):
    return _pycparser.function_name(node)
