from gen import _pycparser


def gen_expr(node):
    if _pycparser.is_constant_node(node):
        type_ = _pycparser.constant_type(node)
        value = _pycparser.constant_value(node)
        assert type_ in ['int', 'unsigned int']
        return value
    elif _pycparser.is_id_node(node):
        return _pycparser.id_name(node)
    elif _pycparser.is_unary_op_node(node):
        op = _pycparser.unary_op_op(node)
        expr = gen_expr(_pycparser.unary_op_expr(node))
        return f'{op}{expr}'
    elif _pycparser.is_binary_op_node(node):
        op = _pycparser.binary_op_op(node)
        left = gen_expr(_pycparser.binary_op_left(node))
        right = gen_expr(_pycparser.binary_op_right(node))
        return f'{left} {op} {right}'
    else:
        raise TypeError('Invalid type')
