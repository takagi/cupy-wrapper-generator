# distutils: language = c++

# This code was automatically generated. Do not modify it directly.


###############################################################################
# Extern
###############################################################################

cdef extern from *:
    ctypedef int Status 'cusparseStatus_t'
    ctypedef int Order 'cusparseOrder_t'
    ctypedef int DataType 'cudaDataType'
    ctypedef int ComputeType 'cusparseComputeType'

cdef extern from '../../cupy_cusparselt.h' nogil:
$external_decls

    # Build-time version
    int CUSPARSELT_VERSION


###############################################################################
# Classes
###############################################################################

cdef class Handle:
    cdef void * _ptr

    def __init__(self):
        self._ptr = PyMem_Malloc(sizeof(cusparseLtHandle_t))

    def __dealloc__(self):
        PyMem_Free(self._ptr)
        self._ptr = NULL

    @property
    def ptr(self):
        return <intptr_t>self._ptr


cdef class MatDescriptor:
    cdef void * _ptr

    def __init__(self):
        self._ptr = PyMem_Malloc(sizeof(cusparseLtMatDescriptor_t))

    def __dealloc__(self):
        PyMem_Free(self._ptr)
        self._ptr = NULL

    @property
    def ptr(self):
        return <intptr_t>self._ptr


cdef class MatmulDescriptor:
    cdef void * _ptr

    def __init__(self):
        self._ptr = PyMem_Malloc(sizeof(cusparseLtMatmulDescriptor_t))

    def __dealloc__(self):
        PyMem_Free(self._ptr)
        self._ptr = NULL

    @property
    def ptr(self):
        return <intptr_t>self._ptr


cdef class MatmulAlgSelection:
    cdef void * _ptr

    def __init__(self):
        self._ptr = PyMem_Malloc(sizeof(cusparseLtMatmulAlgSelection_t))

    def __dealloc__(self):
        PyMem_Free(self._ptr)
        self._ptr = NULL

    @property
    def ptr(self):
        return <intptr_t>self._ptr


cdef class MatmulPlan:
    cdef void * _ptr

    def __init__(self):
        self._ptr = PyMem_Malloc(sizeof(cusparseLtMatmulPlan_t))

    def __dealloc__(self):
        PyMem_Free(self._ptr)
        self._ptr = NULL

    @property
    def ptr(self):
        return <intptr_t>self._ptr


###############################################################################
# Error handling
###############################################################################

@cython.profile(False)
cpdef inline check_status(int status):
    if status != 0:
        raise _cusparse.CuSparseError(status)


###############################################################################
# Wrapper functions
###############################################################################

$wrapper_defs
