// This code was automatically generated. Do not modify it directly.

#ifndef INCLUDE_GUARD_HIP_CUPY_HIPBLAS_H
#define INCLUDE_GUARD_HIP_CUPY_HIPBLAS_H

#include "cupy_hip_common.h"
#include <hipblas.h>
#include <hip/hip_version.h>  // for HIP_VERSION
#include <stdexcept>  // for gcc 10

extern "C" {

///////////////////////////////////////////////////////////////////////////////
// blas & lapack (hipBLAS/rocBLAS & rocSOLVER)
///////////////////////////////////////////////////////////////////////////////

/* As of ROCm 3.5.0 (this may have started earlier) many rocSOLVER helper functions
 * are deprecated and using their counterparts from rocBLAS is recommended. In
 * particular, rocSOLVER simply uses rocBLAS's handle for its API calls. This means
 * they are much more integrated than cuBLAS and cuSOLVER are, so it is better to
 * put all of the relevant function in one place.
 */

// TODO(leofang): investigate if we should just remove the hipBLAS layer and use
// rocBLAS directly, since we need to expose its handle anyway

$opaque_map

$enum_map

/* ---------- helpers ---------- */
static hipblasOperation_t convert_hipblasOperation_t(cublasOperation_t op) {
    return static_cast<hipblasOperation_t>(static_cast<int>(op) + 111);
}

static hipblasFillMode_t convert_hipblasFillMode_t(cublasFillMode_t mode) {
    switch(static_cast<int>(mode)) {
        case 0 /* CUBLAS_FILL_MODE_LOWER */: return HIPBLAS_FILL_MODE_LOWER;
        case 1 /* CUBLAS_FILL_MODE_UPPER */: return HIPBLAS_FILL_MODE_UPPER;
        default: throw std::runtime_error("unrecognized mode");
    }
}

static hipblasDiagType_t convert_hipblasDiagType_t(cublasDiagType_t type) {
    return static_cast<hipblasDiagType_t>(static_cast<int>(type) + 131);
}

static hipblasSideMode_t convert_hipblasSideMode_t(cublasSideMode_t mode) {
    return static_cast<hipblasSideMode_t>(static_cast<int>(mode) + 141);
}

static hipblasDatatype_t convert_hipblasDatatype_t(cudaDataType_t type) {
    switch(static_cast<int>(type)) {
        case 0 /* CUDA_R_32F */: return HIPBLAS_R_32F;
        case 1 /* CUDA_R_64F */: return HIPBLAS_R_64F;
        case 2 /* CUDA_R_16F */: return HIPBLAS_R_16F;
        case 3 /* CUDA_R_8I */ : return HIPBLAS_R_8I;
        case 4 /* CUDA_C_32F */: return HIPBLAS_C_32F;
        case 5 /* CUDA_C_64F */: return HIPBLAS_C_64F;
        case 6 /* CUDA_C_16F */: return HIPBLAS_C_16F;
        case 7 /* CUDA_C_8I */ : return HIPBLAS_C_8I;
        case 8 /* CUDA_R_8U */ : return HIPBLAS_R_8U;
        case 9 /* CUDA_C_8U */ : return HIPBLAS_C_8U;
        default: throw std::runtime_error("unrecognized type");
    }
}

$func_map

cublasStatus_t cublasGetVersion(cublasHandle_t handle, int *version) {
    // We use the rocBLAS version here because 1. it is the underlying workhorse,
    // and 2. we might get rid of the hipBLAS layer at some point (see TODO above).
    // ex: the rocBLAS version string is 2.22.0.2367-b2cceba in ROCm 3.5.0
    *version = 10000 * ROCBLAS_VERSION_MAJOR + 100 * ROCBLAS_VERSION_MINOR + ROCBLAS_VERSION_PATCH;
    return HIPBLAS_STATUS_SUCCESS;
}

} // extern "C"

#endif // #ifndef INCLUDE_GUARD_HIP_CUPY_HIPBLAS_H
