// This file is a stub header file of cuBLAS for Read the Docs. Its code was
// automatically generated. Do not modify it directly.

#ifndef INCLUDE_GUARD_STUB_CUPY_CUBLAS_H
#define INCLUDE_GUARD_STUB_CUPY_CUBLAS_H

#include "cupy_cuda_common.h"

extern "C" {{

{opaque_stubs}

{enum_stubs}

{func_stubs}

cublasStatus_t cublasGemmEx(...) {{
    return CUBLAS_STATUS_SUCCESS;
}}

cublasStatus_t cublasGemmBatchedEx(...) {{
    return CUBLAS_STATUS_SUCCESS;
}}

cublasStatus_t cublasGemmStridedBatchedEx(...) {{
    return CUBLAS_STATUS_SUCCESS;
}}

#define cublasGemmEx_v11 cublasGemmEx
#define cublasGemmBatchedEx_v11 cublasGemmBatchedEx
#define cublasGemmStridedBatchedEx_v11 cublasGemmStridedBatchedEx

}} // extern "C"

#endif // #ifndef INCLUDE_GUARD_STUB_CUPY_CUBLAS_H
