# distutils: language = c++

# This code was automatically generated. Do not modify it directly.

cimport cython  # NOQA

from cupy_backends.cuda.api cimport driver
from cupy_backends.cuda.api cimport runtime
from cupy_backends.cuda cimport stream as stream_module


###############################################################################
# Extern
###############################################################################

cdef extern from '../../cupy_complex.h':
    ctypedef struct cuComplex 'cuComplex'
    ctypedef struct cuDoubleComplex 'cuDoubleComplex'


# FIXME: move to runtime
cdef extern from *:
    ctypedef int LibraryPropertyType 'libraryPropertyType_t'


cdef extern from '../../cupy_blas.h' nogil:
{external_decls}

    # Define by hand for backward compatibility
    Status cublasGemmEx(Handle handle, Operation transa, Operation transb, int m, int n, int k, const void* alpha, const void* A, runtime.DataType Atype, int lda, const void* B, runtime.DataType Btype, int ldb, const void* beta, void* C, runtime.DataType Ctype, int ldc, runtime.DataType computeType, GemmAlgo algo)
    Status cublasGemmEx_v11(Handle handle, Operation transa, Operation transb, int m, int n, int k, const void* alpha, const void* A, runtime.DataType Atype, int lda, const void* B, runtime.DataType Btype, int ldb, const void* beta, void* C, runtime.DataType Ctype, int ldc, ComputeType computeType, GemmAlgo algo)


###############################################################################
# Error handling
###############################################################################

cdef dict STATUS = {{
    0: 'CUBLAS_STATUS_SUCCESS',
    1: 'CUBLAS_STATUS_NOT_INITIALIZED',
    3: 'CUBLAS_STATUS_ALLOC_FAILED',
    7: 'CUBLAS_STATUS_INVALID_VALUE',
    8: 'CUBLAS_STATUS_ARCH_MISMATCH',
    11: 'CUBLAS_STATUS_MAPPING_ERROR',
    13: 'CUBLAS_STATUS_EXECUTION_FAILED',
    14: 'CUBLAS_STATUS_INTERNAL_ERROR',
    15: 'CUBLAS_STATUS_NOT_SUPPORTED',
    16: 'CUBLAS_STATUS_LICENSE_ERROR',
}}


cdef dict HIP_STATUS = {{
    0: 'HIPBLAS_STATUS_SUCCESS',
    1: 'HIPBLAS_STATUS_NOT_INITIALIZED',
    2: 'HIPBLAS_STATUS_ALLOC_FAILED',
    3: 'HIPBLAS_STATUS_INVALID_VALUE',
    4: 'HIPBLAS_STATUS_MAPPING_ERROR',
    5: 'HIPBLAS_STATUS_EXECUTION_FAILED',
    6: 'HIPBLAS_STATUS_INTERNAL_ERROR',
    7: 'HIPBLAS_STATUS_NOT_SUPPORTED',
    8: 'HIPBLAS_STATUS_ARCH_MISMATCH',
    9: 'HIPBLAS_STATUS_HANDLE_IS_NULLPTR',
}}


class CUBLASError(RuntimeError):

    def __init__(self, status):
        self.status = status
        cdef str err
        if runtime._is_hip_environment:
            err = HIP_STATUS[status]
        else:
            err = STATUS[status]
        super(CUBLASError, self).__init__(err)

    def __reduce__(self):
        return (type(self), (self.status,))


@cython.profile(False)
cpdef inline check_status(int status):
    if status != 0:
        raise CUBLASError(status)


###############################################################################
# Wrapper functions
###############################################################################

{wrapper_defs}


# Define by hand for backward compatibility
cpdef gemmEx(intptr_t handle, int transa, int transb, int m, int n, int k, intptr_t alpha, intptr_t A, size_t Atype, int lda, intptr_t B, size_t Btype, int ldb, intptr_t beta, intptr_t C, size_t Ctype, int ldc, int computeType, int algo):
    setStream(handle, stream_module.get_current_stream_ptr())
    with nogil:
        if computeType >= CUBLAS_COMPUTE_16F:
            status = cublasGemmEx_v11(<Handle>handle, <Operation>transa, <Operation>transb, m, n, k, <const void*>alpha, <const void*>A, <runtime.DataType>Atype, lda, <const void*>B, <runtime.DataType>Btype, ldb, <const void*>beta, <void*>C, <runtime.DataType>Ctype, ldc, <ComputeType>computeType, <GemmAlgo>algo)
        else:
            status = cublasGemmEx(<Handle>handle, <Operation>transa, <Operation>transb, m, n, k, <const void*>alpha, <const void*>A, <runtime.DataType>Atype, lda, <const void*>B, <runtime.DataType>Btype, ldb, <const void*>beta, <void*>C, <runtime.DataType>Ctype, ldc, <runtime.DataType>computeType, <GemmAlgo>algo)
    check_status(status)
