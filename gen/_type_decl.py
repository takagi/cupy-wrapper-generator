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
        if _environment.environment_is_opaque_type(name, env):
            pattern = _environment.environment_type_pattern(env)
            match = pattern.fullmatch(name)
            if match is not None:
                return match[1]
        # Enumerators
        if _environment.environment_is_enum(name, env):
            pattern = _environment.environment_type_pattern(env)
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
        if _environment.environment_is_opaque_type(name, env):
            return 'intptr_t'
        # Enumerators
        if _environment.environment_is_enum(name, env):
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


def cuda_type(node):
    if _pycparser.is_raw_type_decl_node(node):
        name = _pycparser.type_name(node)
        quals = _pycparser.type_qualifiers(node)
        return ' '.join(quals + [name]), False
    elif _pycparser.is_pointer_type_decl_node(node):
        base_type = _pycparser.type_base_type(node)
        quals = _pycparser.type_qualifiers(node)
        base_name, is_array = cuda_type(base_type)
        assert not is_array
        return ' '.join([base_name + '*'] + quals), False
    elif _pycparser.is_array_type_decl_node(node):
        base_type = _pycparser.type_base_type(node)
        base_name, is_array = cuda_type(base_type)
        assert not is_array
        return base_name, True
    else:
        raise TypeError('Invalid type')


def hip_type(node, env):
    def aux(name, env):
        name = _pycparser.type_name(node)
        # Special types
        if name == 'cudaDataType':
            return 'hipblasDataType_t'
        if name =='cudaDataType_t':
            return 'hipblasDataType_t'
        if name == 'libraryProperType':
            assert False
        if name == 'cudaStream_t':
            return 'hipStream_t'
        if name == 'cuComplex':
            return 'hipblasComplex'
        if name == 'cuDoubleComplex':
            return 'hipblasDoubleComplex'
        # Opaque types
        if _environment.environment_is_opaque_type(name, env):
            return _environment.environment_opaque_type_hip_name(name, env)
        # Enumerators
        if _environment.environment_is_enum(name, env):
            return _environment.environment_enum_hip_name(name, env)
        # Otherwise (e.g. int)
        return name

    if _pycparser.is_raw_type_decl_node(node):
        name = _pycparser.type_name(node)
        quals = _pycparser.type_qualifiers(node)
        hip_name = aux(name, env)
        return ' '.join(quals + [hip_name]), False
    elif _pycparser.is_pointer_type_decl_node(node):
        base_type = _pycparser.type_base_type(node)
        quals = _pycparser.type_qualifiers(node)
        base_hip_name, is_array = hip_type(base_type, env)
        assert not is_array
        return ' '.join([base_hip_name + '*'] + quals), False
    elif _pycparser.is_array_type_decl_node(node):
        base_type = _pycparser.type_base_type(node)
        base_hip_name, is_array = hip_type(base_type, env)
        assert not is_array
        return base_hip_name, True
    else:
        raise TypeError('Invalid type')


def hip_mapping(node, env):
    if _pycparser.is_raw_type_decl_node(node):
        name = _pycparser.type_name(node)
        # Special types
        if name == 'cudaDataType':
            return 'convert-hip', 'convert_hipblasDatatype_t'
        if name == 'cudaDataType_t':
            return 'convert-hip', 'convert_hipblasDatatype_t'
        if name == 'libraryProperType':
            assert False
        if name == 'cudaStream_t':
            return 'transparent', None
        if name == 'cuComplex':
            raise NotImplementedError
        if name == 'cuDoubleComplex':
            raise NotImplementedError
        # Opaque types
        if _environment.environment_is_opaque_type(name, env):
            return 'transparent', None
        # Enumerators
        if _environment.environment_is_enum(name, env):
            hip_name = _environment.environment_enum_hip_name(name, env)
            return 'convert-hip', f'convert_{hip_name}'
        # Otherwise (e.g. int)
        return 'transparent', None
    elif _pycparser.is_pointer_type_decl_node(node):
        base_type = _pycparser.type_base_type2(node)
        base_name = _pycparser.type_name(base_type)
        # Special types
        if base_name == 'cudaDataType':
            assert False
        if base_name == 'cudaDataType_t':
            assert False
        if base_name == 'libraryProperType':
            assert False
        if base_name == 'cudaStream_t':
            return 'transparent', None
        if base_name == 'cuComplex':
            hip_name, is_array = hip_type(node, env)
            assert not is_array
            return 'reinterpret-cast', hip_name
        if base_name == 'cuDoubleComplex':
            hip_name, is_array = hip_type(node, env)
            assert not is_array
            return 'reinterpret-cast', hip_name
        # Opaque types
        if _environment.environment_is_opaque_type(base_name, env):
            return 'transparent', None
        # Enumerators
        if _environment.environment_is_enum(base_name, env):
            return 'convert-cuda', f'convert_{base_name}'
        # Otherwise (e.g. int)
        return 'transparent', None
    elif _pycparser.is_array_type_decl_node(node):
        base_type = _pycparser.type_base_type2(node)
        base_name = _pycparser.type_name(base_type)
        # Special types
        if base_name == 'cudaDataType':
            assert False
        if base_name == 'cudaDataType_t':
            assert False
        if base_name == 'libraryProperType':
            assert False
        if base_name == 'cudaStream_t':
            assert False
        if base_name == 'cuComplex':
            hip_name, is_array = hip_type(node, env)
            assert is_array
            return 'reinterpret-cast', hip_name + '*'
        if base_name == 'cuDoubleComplex':
            hip_name, is_array = hip_type(node, env)
            assert is_array
            return 'reinterpret-cast', hip_name + '*'
        # Opaque types
        if _environment.environment_is_opaque_type(base_name, env):
            assert False
        # Enumerators
        if _environment.environment_is_enum(base_name, env):
            assert False
        # Otherwise (e.g. int)
        return 'transparent', None
    else:
        raise TypeError('Invalid type')
