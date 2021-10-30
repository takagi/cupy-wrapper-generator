# distutils: language = c++

# This code was automatically generated. Do not modify it directly.

cimport cython  # NOQA

from cupy_backends.cuda cimport stream as stream_module


###############################################################################
# Extern
###############################################################################

cdef extern from '../../cupy_complex.h':
    ctypedef struct cuComplex 'cuComplex'
    ctypedef struct cuDoubleComplex 'cuDoubleComplex'

cdef extern from *:
    ctypedef void* Stream 'cudaStream_t'

cdef extern from '../../cupy_sparse.h' nogil:
$external_decls


###############################################################################
# Error handling
###############################################################################


###############################################################################
# Wrapper functions
###############################################################################

$wrapper_defs
