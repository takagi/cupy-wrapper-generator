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

cublasStatus_t cublasGetVersion_v2(cublasHandle_t handle, int *version) {
    // We use the rocBLAS version here because 1. it is the underlying workhorse,
    // and 2. we might get rid of the hipBLAS layer at some point (see TODO above).
    // ex: the rocBLAS version string is 2.22.0.2367-b2cceba in ROCm 3.5.0
    *version = 10000 * ROCBLAS_VERSION_MAJOR + 100 * ROCBLAS_VERSION_MINOR + ROCBLAS_VERSION_PATCH;
    return HIPBLAS_STATUS_SUCCESS;
}

cublasStatus_t cublasSgemmEx(cublasHandle_t handle, cublasOperation_t transa, cublasOperation_t transb,
			     int m, int n, int k, const float *alpha,
			     const void *A, cudaDataType_t Atype, int lda,
			     const void *B, cudaDataType_t Btype, int ldb,
			     const float *beta,
			     void *C, cudaDataType_t Ctype, int ldc) {
    if (Atype != 0 || Btype != 0 || Ctype != 0) {  // CUDA_R_32F
        return HIPBLAS_STATUS_NOT_SUPPORTED;
    }
    return hipblasSgemm(handle, convert_hipblasOperation_t(transa), convert_hipblasOperation_t(transb),
                        m, n, k, alpha,
                        static_cast<const float*>(A), lda,
                        static_cast<const float*>(B), ldb, beta,
                        static_cast<float*>(C), ldc);
}

cublasStatus_t cublasGemmEx(cublasHandle_t handle, cublasOperation_t transa, cublasOperation_t transb,
                            int m, int n, int k, const void *alpha,
                            const void *A, cudaDataType_t Atype, int lda,
                            const void *B, cudaDataType_t Btype, int ldb,
                            const void *beta,
                            void *C, cudaDataType_t Ctype, int ldc,
                            cudaDataType_t computeType, cublasGemmAlgo_t algo) {
    if (algo != -1) {  // must be CUBLAS_GEMM_DEFAULT
        return HIPBLAS_STATUS_NOT_SUPPORTED;
    }
    return hipblasGemmEx(handle, convert_hipblasOperation_t(transa), convert_hipblasOperation_t(transb),
                         m, n, k, alpha,
                         A, convert_hipblasDatatype_t(Atype), lda,
                         B, convert_hipblasDatatype_t(Btype), ldb,
                         beta,
                         C, convert_hipblasDatatype_t(Ctype), ldc,
                         convert_hipblasDatatype_t(computeType),
                         HIPBLAS_GEMM_DEFAULT);
}

cublasStatus_t cublasGemmEx_v11(...) {
    return HIPBLAS_STATUS_NOT_SUPPORTED;
}

cublasStatus_t cublasGemmBatchedEx(cublasHandle_t handle, cublasOperation_t transa, cublasOperation_t transb,
                                   int m, int n, int k, const void* alpha,
                                   const void* const A[], cudaDataType Atype, int lda,
                                   const void* const B[], cudaDataType Btype, int ldb,
                                   const void* beta,
                                   void* const C[],  cudaDataType Ctype, int ldc,
                                   int batchCount, cudaDataType_t computeType, cublasGemmAlgo_t algo) {
    if (algo != -1) {  // must be CUBLAS_GEMM_DEFAULT
        return HIPBLAS_STATUS_NOT_SUPPORTED;
    }
    return hipblasGemmBatchedEx(handle, convert_hipblasOperation_t(transa), convert_hipblasOperation_t(transb),
                                m, n, k, alpha,
                                const_cast<const void**>(A), convert_hipblasDatatype_t(Atype), lda,
                                const_cast<const void**>(B), convert_hipblasDatatype_t(Btype), ldb,
                                beta,
                                const_cast<void**>(C), convert_hipblasDatatype_t(Ctype), ldc,
                                batchCount, convert_hipblasDatatype_t(computeType),
				HIPBLAS_GEMM_DEFAULT);
}

cublasStatus_t cublasGemmBatchedEx_v11(...) {
    return HIPBLAS_STATUS_NOT_SUPPORTED;
}

cublasStatus_t cublasGemmStridedBatchedEx(cublasHandle_t handle, cublasOperation_t transa, cublasOperation_t transb,
					  int m, int n, int k, const void* alpha,
					  const void* A, cudaDataType Atype, int lda, long long int strideA,
					  const void* B, cudaDataType Btype, int ldb, long long int strideB,
					  const void* beta,
					  void* C, cudaDataType Ctype, int ldc, long long int strideC,
					  int batchCount, cudaDataType_t computeType, cublasGemmAlgo_t algo) {
    if (algo != -1) {  // must be CUBLAS_GEMM_DEFAULT
        return HIPBLAS_STATUS_NOT_SUPPORTED;
    }
    return hipblasGemmStridedBatchedEx(handle, convert_hipblasOperation_t(transa), convert_hipblasOperation_t(transb),
				       m, n, k, alpha,
				       A, convert_hipblasDatatype_t(Atype), lda, strideA,
				       B, convert_hipblasDatatype_t(Btype), ldb, strideB,
				       beta,
                                       C, convert_hipblasDatatype_t(Ctype), ldc, strideC,
                                       batchCount, convert_hipblasDatatype_t(computeType),
                                       HIPBLAS_GEMM_DEFAULT);
}

cublasStatus_t cublasGemmStridedBatchedEx_v11(...) {
    return HIPBLAS_STATUS_NOT_SUPPORTED;
}

} // extern "C"

#endif // #ifndef INCLUDE_GUARD_HIP_CUPY_HIPBLAS_H
