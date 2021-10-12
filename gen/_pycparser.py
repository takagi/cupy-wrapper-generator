from pycparser import c_ast


# Function declarations

def is_func_decl_node(node):
    return (isinstance(node, c_ast.Decl) and
            isinstance(node.type, c_ast.FuncDecl))


def function_ret_type_node(node):
    assert is_func_decl_node(node)
    return node.type.type


def function_name(node):
    assert is_func_decl_node(node)
    return node.name


def function_arg_nodes(node):
    assert is_func_decl_node(node)
    params = node.type.args.params
    # 'void' parameter
    if len(params) == 1 and _is_void_type_decl_node(params[0].type):
        return []
    return params


def _is_argument_node(node):
    if (
        isinstance(node, c_ast.Decl) and
        isinstance(
            node.type, (c_ast.TypeDecl, c_ast.PtrDecl, c_ast.ArrayDecl))
    ):
        return True
    if isinstance(node, c_ast.Typename):  # without variable name
        return True
    return False


def argument_name(node):
    assert _is_argument_node(node)
    return node.name


def argument_type_node(node):
    assert _is_argument_node(node)
    return node.type


# Type declarations

def is_type_decl_node(node):
    return isinstance(node, (c_ast.TypeDecl, c_ast.PtrDecl, c_ast.ArrayDecl))


def is_raw_type_decl_node(node):
    return isinstance(node, c_ast.TypeDecl)


def is_pointer_type_decl_node(node):
    return isinstance(node, c_ast.PtrDecl)


def is_array_type_decl_node(node):
    return isinstance(node, c_ast.ArrayDecl)


def _is_void_type_decl_node(node):
    return (isinstance(node, c_ast.TypeDecl) and
            isinstance(node.type, c_ast.IdentifierType) and
            node.type.names == ['void'])


def type_name(node):
    assert is_raw_type_decl_node(node)
    assert isinstance(node.type, c_ast.IdentifierType)
    names = node.type.names
    return ' '.join(names)


def type_qualifiers(node):
    assert is_raw_type_decl_node(node) or is_pointer_type_decl_node(node)
    return node.quals


def type_base_type(node):
    assert is_pointer_type_decl_node(node) or is_array_type_decl_node(node)
    return node.type


deref = type_base_type


# Opaque type declarations

def is_opaque_type_decl_node(node):
    return (isinstance(node, c_ast.Typedef) and
            isinstance(node.type, c_ast.PtrDecl) and
            isinstance(node.type.type, c_ast.TypeDecl) and
            isinstance(node.type.type.type, c_ast.Struct))


def opaque_type_name(node):
    assert is_opaque_type_decl_node(node)
    return node.name


# Enum declarations

def is_enum_decl_node(node):
    return (isinstance(node, c_ast.Typedef) and
            isinstance(node.type, c_ast.TypeDecl) and
            isinstance(node.type.type, c_ast.Enum))


def enum_name(node):
    assert is_enum_decl_node(node)
    return node.name


def enum_items(node):
    assert is_enum_decl_node(node)
    return [(e.name, e.value) for e in node.type.type.values.enumerators]


def is_status_enum_decl_node(node):
    if not is_enum_decl_node(node):
        return False
    return 'Status_t' in enum_name(node)


def status_enum_success(node):
    assert is_status_enum_decl_node(node)
    for e in node.type.type.values.enumerators:
        if 'STATUS_SUCCESS' in e.name:
            return e.name, e.value
    raise ValueError('Success status not found')


# Expressions

def is_constant_node(node):
    return isinstance(node, c_ast.Constant)


def constant_type(node):
    assert is_constant_node(node)
    return node.type


def constant_value(node):
    assert is_constant_node(node)
    return node.value


def is_id_node(node):
    return isinstance(node, c_ast.ID)


def id_name(node):
    assert is_id_node(node)
    return node.name


def is_unary_op_node(node):
    return isinstance(node, c_ast.UnaryOp)


def unary_op_op(node):
    assert is_unary_op_node(node)
    return node.op


def unary_op_expr(node):
    assert is_unary_op_node(node)
    return node.expr


def is_binary_op_node(node):
    return isinstance(node, c_ast.BinaryOp)


def binary_op_op(node):
    assert is_binary_op_node(node)
    return node.op


def binary_op_left(node):
    assert is_binary_op_node(node)
    return node.left


def binary_op_right(node):
    assert is_binary_op_node(node)
    return node.right
