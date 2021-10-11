# This code was automatically generated. Do not modify it directly.

from libc.stdint cimport intptr_t


###############################################################################
# Types
###############################################################################

cdef extern from *:
{opaque_decls}

{enum_decls}


###############################################################################
# Enum
###############################################################################

{enum_values}


###############################################################################
# Functions
###############################################################################

{func_decls}

# Define by hand for backward compatibility
cpdef gemmEx(intptr_t handle, int transa, int transb, int m, int n, int k, intptr_t alpha, intptr_t A, size_t Atype, int lda, intptr_t B, size_t Btype, int ldb, intptr_t beta, intptr_t C, size_t Ctype, int ldc, int computeType, int algo)
