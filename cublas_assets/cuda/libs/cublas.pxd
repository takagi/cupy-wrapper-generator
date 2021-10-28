# This code was automatically generated. Do not modify it directly.

from libc.stdint cimport intptr_t


###############################################################################
# Types
###############################################################################

cdef extern from *:
$opaque_decls

$enum_decls


###############################################################################
# Enum
###############################################################################

$enum_values


###############################################################################
# Functions
###############################################################################

$func_decls

# Define by hand for backward compatibility
cpdef gemmEx(intptr_t handle, int transa, int transb, int m, int n, int k, intptr_t alpha, intptr_t A, size_t Atype, int lda, intptr_t B, size_t Btype, int ldb, intptr_t beta, intptr_t C, size_t Ctype, int ldc, int computeType, int algo)
cpdef gemmBatchedEx(intptr_t handle, int transa, int transb, int m, int n, int k, intptr_t alpha, intptr_t Aarray, size_t Atype, int lda, intptr_t Barray, size_t Btype, int ldb, intptr_t beta, intptr_t Carray, size_t Ctype, int ldc, int batchCount, int computeType, int algo)
cpdef gemmStridedBatchedEx(intptr_t handle, int transa, int transb, int m, int n, int k, intptr_t alpha, intptr_t A, size_t Atype, int lda, long long int strideA, intptr_t B, size_t Btype, int ldb, long long int strideB, intptr_t beta, intptr_t C, size_t Ctype, int ldc, long long int strideC, int batchCount, int computeType, int algo)
