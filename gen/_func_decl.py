from gen import _environment
from gen import _pycparser
from gen import util


def cupy_name(node, env):
    cuda_name = _pycparser.function_name(node, strip_suffix=True)
    cupy_name_ = _environment.environment_function_cupy_name(cuda_name, env)
    if cupy_name_ is not None:
        return cupy_name_
    pattern = _environment.environment_function_pattern(env)
    cupy_name_ = pattern.fullmatch(cuda_name)[1]
    return cupy_name_[0:2].lower() + cupy_name_[2:]


def cuda_name(node):
    return _pycparser.function_name(node, strip_suffix=True)


def hip_name(node, env):
    cuda_name = _pycparser.function_name(node, strip_suffix=True)
    hip_node = _environment.environment_function_hip_node(cuda_name, env)
    hip_name_ = _pycparser.function_name(hip_node)
    return hip_name_
