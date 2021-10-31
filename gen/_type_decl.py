from gen import _environment
from gen import _pycparser


_special_types = {
    'cudaDataType': {
        'cupy_type': 'DataType',
        'erased_type': 'size_t',
    },
    'cudaDataType_t': {
        'cupy_type': 'DataType',
        'erased_type': 'size_t',
    },
    'libraryPropertyType': {
        'cupy_type': 'LibraryPropertyType',
        'erased_type': 'int',
    },
    'cudaStream_t': {
        'cupy_type': 'Stream',
        'erased_type': 'size_t',
    },
}


def _special_type_cupy_type(name):
    special_type = _special_types.get(name)
    if special_type is None:
        return None
    return special_type['cupy_type']


def _special_type_erased_type(name):
    special_type = _special_types.get(name)
    if special_type is None:
        return None
    return special_type['erased_type']


def _special_type_cuda_type(name):
    special_type = _special_types.get(name)
    if special_type is None:
        return None
    return name


def cupy_type(node, env):
    def aux(name, env):
        # Special types (e.g. cudaDataType)
        cupy_name = _special_type_cupy_type(name)
        if cupy_name is not None:
            return cupy_name
        # Opaque types
        if _environment.is_opaque_type(name, env):
            pattern = _environment.type_pattern(env)
            match = pattern.fullmatch(name)
            if match is not None:
                return match[1]
        # Enumerators
        if _environment.is_enum(name, env):
            pattern = _environment.type_pattern(env)
            match = pattern.fullmatch(name)
            if match is not None:
                return match[1]
        # Otherwise (e.g. int)
        return name

    if _pycparser.is_raw_type_decl_node(node):
        name = _pycparser.type_name(node)
        quals = _pycparser.type_qualifiers(node)
        cupy_name = aux(name, env)
        return ' '.join(quals + [cupy_name]), False
    elif _pycparser.is_pointer_type_decl_node(node):
        base_type = _pycparser.type_base_type(node)
        quals = _pycparser.type_qualifiers(node)
        base_cupy_name, is_array = cupy_type(base_type, env)
        assert not is_array
        return ' '.join([base_cupy_name + '*'] + quals), False
    elif _pycparser.is_array_type_decl_node(node):
        base_type = _pycparser.type_base_type(node)
        base_cupy_name, is_array = cupy_type(base_type, env)
        assert not is_array
        return base_cupy_name, True
    else:
        raise TypeError('Invalid type')


def erased_type(node, env):
    def aux(name, env):
        # Special types (e.g. cudaDataType)
        erased_name = _special_type_erased_type(name)
        if erased_name is not None:
            return erased_name
        # Opaque types
        if _environment.is_opaque_type(name, env):
            return 'intptr_t'
        # Enumerators
        if _environment.is_enum(name, env):
            return 'int'
        # Otherwise (e.g. int)
        return name

    if _pycparser.is_raw_type_decl_node(node):
        name = _pycparser.type_name(node)
        return aux(name, env)
    elif _pycparser.is_pointer_type_decl_node(node):
        return 'intptr_t'
    elif _pycparser.is_array_type_decl_node(node):
        return 'intptr_t'
    else:
        raise TypeError('Invalid type')


def cuda_type(node, strip_cv=False):
    if _pycparser.is_raw_type_decl_node(node):
        name = _pycparser.type_name(node)
        if strip_cv:
            return name, False
        else:
            quals = _pycparser.type_qualifiers(node)
            return ' '.join(quals + [name]), False
    elif _pycparser.is_pointer_type_decl_node(node):
        base_type = _pycparser.type_base_type(node)
        base_name, is_array = cuda_type(base_type, strip_cv=strip_cv)
        assert not is_array
        if strip_cv:
            return base_name + '*', False
        else:
            quals = _pycparser.type_qualifiers(node)
            return ' '.join([base_name + '*'] + quals), False
    elif _pycparser.is_array_type_decl_node(node):
        base_type = _pycparser.type_base_type(node)
        base_name, is_array = cuda_type(base_type, strip_cv=strip_cv)
        assert not is_array
        return base_name, True
    else:
        raise TypeError('Invalid type')


def hip_type(cuda_node, hip_node, env):
    def aux(cuda_node, hip_node, env):
        if _pycparser.is_raw_type_decl_node(cuda_node):
            cuda_name = _pycparser.type_name(cuda_node)
            hip_name = _pycparser.type_name(hip_node)
            cuda_quals = _pycparser.type_qualifiers(cuda_node)
            hip_quals = _pycparser.type_qualifiers(hip_node)
            needs_const_cast = cuda_quals != hip_quals
            return (' '.join(hip_quals + [hip_name]),
                    ' '.join(hip_quals + [cuda_name]),
                    needs_const_cast,
                    False)
        elif _pycparser.is_pointer_type_decl_node(cuda_node):
            cuda_base_type = _pycparser.type_base_type(cuda_node)
            hip_base_type = _pycparser.type_base_type(hip_node)
            (base_hip_name, base_const_cast_name, base_needs_const_cast,
             base_is_array) = aux(cuda_base_type, hip_base_type, env)
            assert not base_is_array
            cuda_quals = _pycparser.type_qualifiers(cuda_node)
            hip_quals = _pycparser.type_qualifiers(hip_node)
            needs_const_cast = (
                base_needs_const_cast or cuda_quals != hip_quals)
            return (' '.join([base_hip_name + '*'] + hip_quals),
                    ' '.join([base_const_cast_name + '*'] + hip_quals),
                    needs_const_cast,
                    False)
        elif _pycparser.is_array_type_decl_node(cuda_node):
            cuda_base_type = _pycparser.type_base_type(cuda_node)
            hip_base_type = _pycparser.type_base_type(hip_node)
            (base_hip_name, base_const_cast_name, base_needs_const_cast,
             base_is_array) = aux(cuda_base_type, hip_base_type, env)
            assert not base_is_array
            return (base_hip_name,
                    base_const_cast_name,
                    base_needs_const_cast,
                    True)
        else:
            raise TypeError('Invalid type')

    hip_name, const_cast_name, needs_const_cast, is_array = (
        aux(cuda_node, hip_node, env))
    if needs_const_cast:
        return hip_name, const_cast_name, is_array
    else:
        return hip_name, None, is_array


def hip_mapping(cuda_node, hip_node, env):
    if _pycparser.is_raw_type_decl_node(cuda_node):
        cuda_name = _pycparser.type_name(cuda_node)
        # Special types
        if cuda_name == 'cudaDataType':
            # FIXME: other HIP libraries
            return 'convert-hip', 'convert_hipblasDatatype_t'
        if cuda_name == 'cudaDataType_t':
            # FIXME: other HIP libraries
            return 'convert-hip', 'convert_hipblasDatatype_t'
        if cuda_name == 'libraryProperType':
            assert False
        if cuda_name == 'cudaStream_t':
            return 'transparent', None
        if cuda_name == 'cuComplex':
            raise NotImplementedError
        if cuda_name == 'cuDoubleComplex':
            raise NotImplementedError
        # Opaque types
        if _environment.is_opaque_type(cuda_name, env):
            return 'transparent', None
        # Enumerators
        if _environment.is_enum(cuda_name, env):
            _, is_transparent, _, _ = (
                _environment.enum_hip_spec(cuda_name, env))
            assert is_transparent is not None
            if is_transparent:
                return 'transparent', None
            else:
                hip_name = _pycparser.type_name(hip_node)
                return 'convert-hip', f'convert_{hip_name}'
        # Otherwise (e.g. int)
        return 'transparent', None
    elif _pycparser.is_pointer_type_decl_node(cuda_node):
        root_type = _pycparser.type_root_type(cuda_node)
        root_name = _pycparser.type_name(root_type)
        # Special types
        if root_name == 'cudaDataType':
            assert False
        if root_name == 'cudaDataType_t':
            assert False
        if root_name == 'libraryProperType':
            assert False
        if root_name == 'cudaStream_t':
            return 'transparent', None
        if root_name in ['cuComplex', 'cuDoubleComplex']:
            hip_name, const_cast_name, is_array = (
                hip_type(cuda_node, hip_node, env))
            assert not is_array
            if const_cast_name is None:
                return 'reinterpret-cast', hip_name
            else:
                arg = (const_cast_name, hip_name)
                return 'const-cast-reinterpret-cast', arg
        # Opaque types
        if _environment.is_opaque_type(root_name, env):
            return 'transparent', None
        # Enumerators
        if _environment.is_enum(root_name, env):
            _, is_transparent, _, _ = (
                _environment.enum_hip_spec(root_name, env))
            assert is_transparent is not None
            if is_transparent:
                return 'transparent', None
            else:
                return 'convert-cuda', f'convert_{root_name}'
        # Otherwise (e.g. int)
        hip_name, const_cast_name, is_array = (
            hip_type(cuda_node, hip_node, env))
        assert not is_array
        if const_cast_name is None:
            return 'transparent', None
        else:
            assert hip_name == const_cast_name
            return 'const-cast', hip_name
    elif _pycparser.is_array_type_decl_node(cuda_node):
        root_type = _pycparser.type_root_type(cuda_node)
        root_name = _pycparser.type_name(root_type)
        # Special types
        if root_name == 'cudaDataType':
            assert False
        if root_name == 'cudaDataType_t':
            assert False
        if root_name == 'libraryProperType':
            assert False
        if root_name == 'cudaStream_t':
            assert False
        if root_name in ['cuComplex', 'cuDoubleComplex']:
            hip_name, const_cast_name, is_array = (
                hip_type(cuda_node, hip_node, env))
            assert is_array
            if const_cast_name is None:
                return 'reinterpret-cast', hip_name + '*'
            else:
                arg = (const_cast_name + '*', hip_name + '*')
                return 'const-cast-reinterpret-cast', arg
        # Opaque types
        if _environment.is_opaque_type(root_name, env):
            assert False
        # Enumerators
        if _environment.is_enum(root_name, env):
            assert False
        # Otherwise (e.g. int)
        hip_name, const_cast_name, is_array = (
            hip_type(cuda_node, hip_node, env))
        assert is_array
        if const_cast_name is None:
            return 'transparent', None
        else:
            assert hip_name == const_cast_name
            return 'const-cast', hip_name + '*'
    else:
        raise TypeError('Invalid type')
