from gen import _environment
from gen import _pycparser


def cupy_name(node, env):
    cuda_name = _pycparser.function_name(node)
    cupy_name_ = _environment.environment_function_cupy_name(cuda_name, env)
    if cupy_name_ is not None:
        return cupy_name_
    pattern = _environment.environment_function_pattern(env)
    cupy_name_ = pattern.fullmatch(cuda_name)[1]
    return cupy_name_[0:2].lower() + cupy_name_[2:]


def cuda_name(node):
    return _pycparser.function_name(node)


def hip_name(node, env):
    cuda_name = _pycparser.function_name(node)
    hip_name_ = _environment.environment_function_hip_name(cuda_name, env)
    return hip_name_
