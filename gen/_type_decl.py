from gen import _environment
from gen import _pycparser


_special_types = {
    'cudaDataType': {
        'cupy_type': 'runtime.DataType',
        'erased_type': 'size_t',
    },
    'cudaDataType_t': {
        'cupy_type': 'runtime.DataType',
        'erased_type': 'size_t',
    },
    'libraryPropertyType': {
        'cupy_type': 'LibraryPropertyType',
        'erased_type': 'int',
    },
    'cudaStream_t': {
        'cupy_type': 'driver.Stream',
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
