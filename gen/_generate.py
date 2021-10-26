import re

from gen import _enum_decl
from gen import _environment
from gen import _expr
from gen import _func_decl
from gen import _opaque_decl
from gen import _pycparser
from gen import _return_spec
from gen import _type_decl
import gen.util


def generate_external_declaration(name, env):
    def argaux(arg_node, env):
        arg_name = _pycparser.argument_name(arg_node)
        arg_type_node = _pycparser.argument_type_node(arg_node)
        arg_type, is_array = _type_decl.cupy_type(arg_type_node, env)
        if arg_name is None:
            return arg_type  # when appears? solo void?
        if is_array:
            arg_name += '[]'
        return f'{arg_type} {arg_name}'
    func_node = _environment.environment_function_node(name, env)
    ret_type_node = _pycparser.function_ret_type_node(func_node)
    arg_nodes = _pycparser.function_arg_nodes(func_node)
    ret_type, is_array = _type_decl.cupy_type(ret_type_node, env)
    assert not is_array
    args = [argaux(arg_node, env) for arg_node in arg_nodes]
    return f'{ret_type} {name}({", ".join(args)})'


def _is_stream_arg_node(node):
    # Assuming an argument named 'stream' is a stream argument
    return 'stream' == _pycparser.argument_name(node)


def generate_wrapper_declaration(name, env):
    def argaux(arg_node, env):
        arg_name = _pycparser.argument_name(arg_node)
        arg_type_node = _pycparser.argument_type_node(arg_node)
        arg_type = _type_decl.erased_type(arg_type_node, env)
        if arg_name is None:
            return arg_type  # when apperas? solo void?
        return f'{arg_type} {arg_name}'
    func_node = _environment.environment_function_node(name, env)
    arg_nodes = _pycparser.function_arg_nodes(func_node)
    use_stream, fashion, _ = (
        _environment.environment_function_stream_spec(name, env))
    if use_stream and fashion == 'pass':
        # Remove the stream argument if the function takes it for async work
        stream_nodes, arg_nodes = gen.util.partition(
            lambda n: _is_stream_arg_node(n), arg_nodes)
        if len(stream_nodes) == 0:
            raise ValueError('Stream argument not found')
    ret_spec = _environment.environment_function_return_spec(name, env)
    if _return_spec.is_none(ret_spec):
        cupy_name = _func_decl.cupy_name(func_node, env)
        args = [argaux(arg_node, env) for arg_node in arg_nodes]
        return f'cpdef {cupy_name}({", ".join(args)})'
    elif _return_spec.is_transparent(ret_spec):
        ret_type_node = _pycparser.function_ret_type_node(func_node)
        ret_type = _type_decl.erased_type(ret_type_node, env)
        cupy_name = _func_decl.cupy_name(func_node, env)
        args = [argaux(arg_node, env) for arg_node in arg_nodes]
        return f'cpdef {ret_type} {cupy_name}({", ".join(args)})'
    elif _return_spec.is_single(ret_spec):
        out_name = _return_spec.single_return_spec(ret_spec)
        out_nodes, arg_nodes1 = gen.util.partition(
            lambda n: _pycparser.argument_name(n) == out_name, arg_nodes)
        assert len(out_nodes) == 1, f'`{out_name}` not found in API arguments'
        out_node = out_nodes[0]
        out_type_node = _pycparser.argument_type_node(out_node)
        ret_type_node = _pycparser.deref(out_type_node)
        ret_type = _type_decl.erased_type(ret_type_node, env)
        cupy_name = _func_decl.cupy_name(func_node, env)
        args = [argaux(arg_node, env) for arg_node in arg_nodes1]
        excpt = _environment.environment_function_except(name, env)
        return f'cpdef {ret_type} {cupy_name}({", ".join(args)}) {excpt}'
    elif _return_spec.is_multi(ret_spec):
        raise NotImplementedError()
    else:
        assert False


def _is_handle_arg_node(node):
    # Assuming an argument named 'handle' is a handle argument
    return 'handle' == _pycparser.argument_name(node)


def _generate_stream_code(code, fashion, setter_name, arg_nodes):
    if fashion == 'set':
        pred = _is_handle_arg_node
        handle_node = next((n for n in arg_nodes if pred(n)), None)
        if handle_node is None:
            raise ValueError('Handle argument not found')
        handle_name = _pycparser.argument_name(handle_node)
        code.append(f'    {setter_name}({handle_name}, '
                    'stream_module.get_current_stream_ptr())')
    elif fashion == 'pass':
        pred = _is_stream_arg_node
        stream_node = next((n for n in arg_nodes if pred(n)), None)
        if stream_node is None:
            raise ValueError('Stream argument not found')
        stream_name = _pycparser.argument_name(stream_node)
        code.append(f'    cdef intptr_t {stream_name} = '
                    'stream_module.get_current_stream_ptr()')
    else:
        assert False


def _deref_var_name(name):
    m = re.fullmatch(r'p([A-Z].*)', name)
    if m is not None:
        name1 = m[1]
        return name1[0].lower() + name1[1:]
    else:
        return name


def generate_wrapper_definition(name, env):
    def argaux0(arg_node, env):
        arg_name = _pycparser.argument_name(arg_node)
        arg_type_node = _pycparser.argument_type_node(arg_node)
        arg_cupy_type, is_array = _type_decl.cupy_type(arg_type_node, env)
        if is_array:
            arg_cupy_type += '*'
        arg_erased_type = _type_decl.erased_type(arg_type_node, env)
        if arg_cupy_type == arg_erased_type:
            return arg_name
        else:
            return f'<{arg_cupy_type}>{arg_name}'

    def argaux1(arg_node, out_node, env):
        if arg_node is out_node:
            arg_name = _pycparser.argument_name(arg_node)
            ret_name = _deref_var_name(arg_name)
            return f'&{ret_name}'
        return argaux0(arg_node, env)

    code = []

    def_ = generate_wrapper_declaration(name, env) + ':'
    code.append(def_)

    func_node = _environment.environment_function_node(name, env)
    arg_nodes = _pycparser.function_arg_nodes(func_node)
    ret_spec = _environment.environment_function_return_spec(name, env)
    use_stream, fashion, setter_name = (
        _environment.environment_function_stream_spec(name, env))
    if _return_spec.is_none(ret_spec):
        if use_stream:
            _generate_stream_code(code, fashion, setter_name, arg_nodes)
        cuda_name = _func_decl.cuda_name(func_node)
        args = [argaux0(arg_node, env) for arg_node in arg_nodes]
        code.append('    with nogil:')
        code.append(f'        status = {cuda_name}({", ".join(args)})')
        code.append('    check_status(status)')
        return '\n'.join(code)
    elif _return_spec.is_transparent(ret_spec):
        if use_stream:
            _generate_stream_code(code, fashion, setter_name, arg_nodes)
        cuda_name = _func_decl.cuda_name(func_node)
        args = [argaux0(arg_node, env) for arg_node in arg_nodes]
        code.append(f'    return {cuda_name}({", ".join(args)})')
        return '\n'.join(code)
    elif _return_spec.is_single(ret_spec):
        if use_stream:
            _generate_stream_code(code, fashion, setter_name, arg_nodes)
        out_name = _return_spec.single_return_spec(ret_spec)
        out_nodes, _ = gen.util.partition(
            lambda n: _pycparser.argument_name(n) == out_name, arg_nodes)
        assert len(out_nodes) == 1, f'`{out_name}` not found in API arguments'
        out_node = out_nodes[0]
        out_type_node = _pycparser.argument_type_node(out_node)
        ret_name = _deref_var_name(out_name)
        ret_type_node = _pycparser.deref(out_type_node)
        ret_cupy_type, is_array = _type_decl.cupy_type(ret_type_node, env)
        assert not is_array
        ret_erased_type = _type_decl.erased_type(ret_type_node, env)
        cuda_name = _func_decl.cuda_name(func_node)
        args = [argaux1(arg_node, out_node, env) for arg_node in arg_nodes]
        code.append(f'    cdef {ret_cupy_type} {ret_name}')
        code.append('    with nogil:')
        code.append(f'        status = {cuda_name}({", ".join(args)})')
        code.append('    check_status(status)')
        if ret_cupy_type == ret_erased_type:
            code.append(f'    return {ret_name}')
        else:
            code.append(f'    return <{ret_erased_type}>{ret_name}')
        return '\n'.join(code)
    elif _return_spec.is_multi(ret_spec):
        if use_stream:
            _generate_stream_code(code, fashion, setter_name, arg_nodes)
        raise NotImplementedError()
    else:
        assert False


def generate_opaque_type_declaration(name, env):
    opaque_node = _environment.environment_opaque_type_node(name, env)
    cupy_type = _opaque_decl.cupy_type(opaque_node, env)
    erased_type = _opaque_decl.erased_type(opaque_node)
    cuda_type = _opaque_decl.cuda_type(opaque_node)
    return f"ctypedef {erased_type} {cupy_type} '{cuda_type}'"


def generate_enum_declaration(name, env):
    enum_node = _environment.environment_enum_node(name, env)

    cupy_type = _enum_decl.cupy_type(enum_node, env)
    erased_type = _enum_decl.erased_type(enum_node)
    cuda_type = _enum_decl.cuda_type(enum_node)
    typedef = f"ctypedef {erased_type} {cupy_type} '{cuda_type}'"

    values = ['cpdef enum:']
    for name, value in _pycparser.enum_items(enum_node):
        if value is None:
            values.append(f'    {name}')
        else:
            value1 = _expr.gen_expr(value)
            values.append(f'    {name} = {value1}')

    return typedef, '\n'.join(values)


def generate_function_stub(name, env):
    func_node = _environment.environment_function_node(name, env)
    func_name = _pycparser.function_name(func_node)

    ret_type_node = _pycparser.function_ret_type_node(func_node)
    ret_type, is_array = _type_decl.cuda_type(ret_type_node)
    assert not is_array

    status_enum_node = _environment.environment_status_enum_node(env)
    status_enum_type = _pycparser.enum_name(status_enum_node)

    if ret_type == status_enum_type:
        ret_value, _ = _pycparser.status_enum_success(status_enum_node)
    elif ret_type == 'size_t':
        ret_value = 0
    else:
        raise ValueError('Unexpected return type')

    return f'''{ret_type} {func_name}(...) {{
    return {ret_value};
}}'''


def generate_opaque_type_stub(name, env):
    opaque_node = _environment.environment_opaque_type_node(name, env)
    cuda_type = _opaque_decl.cuda_type(opaque_node)
    return f'typedef void* {cuda_type};'


def generate_enum_stub(name, env):
    enum_node = _environment.environment_enum_node(name, env)
    if _pycparser.is_status_enum_decl_node(enum_node):
        status_type = _pycparser.enum_name(enum_node)
        success_name, success_expr = _pycparser.status_enum_success(enum_node)
        success_expr = _expr.gen_expr(success_expr)
        return f'''typedef enum {{
    {success_name} = {success_expr}
}} {status_type};'''
    else:
        cuda_type = _enum_decl.cuda_type(enum_node)
        return f'typedef enum{{}} {cuda_type};'


def generate_function_hip(name, env):
    def aux_cuda_declarator(hip_yes, name, env):
        def argaux(arg_node, env):
            arg_name = _pycparser.argument_name(arg_node)
            arg_type_node = _pycparser.argument_type_node(arg_node)
            arg_type, is_array = (
                _type_decl.cuda_type(arg_type_node, strip_cv=False))
            if is_array:
                arg_name += '[]'
            return f'{arg_type} {arg_name}'
        func_node = _environment.environment_function_node(name, env)
        ret_type_node = _pycparser.function_ret_type_node(func_node)
        arg_nodes = _pycparser.function_arg_nodes(func_node)
        ret_type, is_array = _type_decl.cuda_type(ret_type_node)
        assert not is_array
        args = [argaux(arg_node, env) for arg_node in arg_nodes]
        if hip_yes:
            return f'{ret_type} {name}({", ".join(args)})'
        else:
            return f'{ret_type} {name}(...)'

    def aux_hip_call(name, env):
        def argaux(arg_node, env):
            arg_name = _pycparser.argument_name(arg_node)
            arg_type_node = _pycparser.argument_type_node(arg_node)
            map_kind, map_arg = _type_decl.hip_mapping(arg_type_node, env)
            if map_kind == 'transparent':
                assert map_arg is None
                return arg_name
            elif map_kind == 'reinterpret-cast':
                # `map_arg` contains the HIP-side type casting to
                return f'reinterpret_cast<{map_arg}>({arg_name})'
            elif map_kind == 'convert-hip':
                # `map_arg` contains the name of a conversion function
                return f'{map_arg}({arg_name})'
            elif map_kind == 'convert-cuda':
                raise NotImplementedError
            else:
                assert False

        func_node = _environment.environment_function_node(name, env)
        arg_nodes = _pycparser.function_arg_nodes(func_node)
        hip_name = _func_decl.hip_name(func_node, env)
        args = [argaux(arg_node, env) for arg_node in arg_nodes]
        return f'{hip_name}({", ".join(args)})'

    hip_yes, hip_since, hip_until = (
        _environment.environment_function_hip_spec(name, env))
    assert hip_until is None

    code = []
    cuda_decl = aux_cuda_declarator(hip_yes, name, env)
    code.append(f'{cuda_decl} {{')

    hip_not_supported = (
        _environment.environment_status_enum_hip_not_supported(env))
    if hip_yes:
        hip_call = aux_hip_call(name, env)
        hip_gurad = _environment.environment_function_hip_guard(name, env)
        if hip_since is None:
            if hip_gurad is not None:
                code.append(gen.util.indent(hip_gurad))
            code.append(f'    return {hip_call};')
        else:
            code.append(f'    #if HIP_VERSION < {hip_since}')
            code.append(f'    return {hip_not_supported};')
            code.append('    #else')
            if hip_gurad is not None:
                code.append(gen.util.indent(hip_gurad))
            code.append(f'    return {hip_call};')
            code.append('    #endif')
    else:
        code.append(f'    return {hip_not_supported};')
    code.append('}')

    return '\n'.join(code)


def generate_opaque_type_hip(name, env):
    opaque_node = _environment.environment_opaque_type_node(name, env)
    hip_yes, hip_since, hip_until = (
        _environment.environment_opaque_type_hip_spec(name, env))
    assert hip_until is None
    cuda_type = _opaque_decl.cuda_type(opaque_node)
    if hip_yes:
        hip_type = _opaque_decl.hip_type(opaque_node, env)
        if hip_since is None:
            return f'typedef {hip_type} {cuda_type};'
        else:
            return f'''#if HIP_VERSION < {hip_since}
typedef enum {{}} {cuda_type};
#else
typedef {hip_type} {cuda_type};
#endif'''
    else:
        return f'typedef enum {{}} {cuda_type};'


def generate_enum_hip(name, env):
    enum_node = _environment.environment_enum_node(name, env)
    hip_yes, hip_is_transparent, hip_since, hip_until = (
        _environment.environment_enum_hip_spec(name, env))
    assert hip_until is None
    cuda_type = _enum_decl.cuda_type(enum_node)
    if hip_yes and hip_is_transparent:
        hip_type = _enum_decl.hip_type(enum_node, env)
        if hip_since is None:
            return f'typedef {hip_type} {cuda_type};'
        else:
            return f'''#if HIP_VERSION < {hip_since}
typedef enum {{}} {cuda_type};
#else
typedef {hip_type} {cuda_type};
#endif'''
    else:
        return f'typedef enum {{}} {cuda_type};'

    return f'typdef enum {{}} {cuda_type}'
