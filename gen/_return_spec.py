def is_none(spec):
    return spec is None


def is_transparent(spec):
    return isinstance(spec, str) and spec == 'Transparent'


def is_single(spec):
    return isinstance(spec, str) and spec != 'Transparent'


def single_return_spec(spec):
    assert is_single(spec)
    return spec


def is_multi(spec):
    if not isinstance(spec, tuple):
        return False
    assert len(spec) == 2
    assert isinstance(spec[0], str)
    assert isinstance(spec[1], tuple)
    return True


def multi_return_spec(spec):
    assert is_multi(spec)
    raise NotImplementedError()
