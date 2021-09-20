{
    'versions': [
        ('11.4', '/usr/local/cuda-11.4.1/include/'),
        ('11.3', '/usr/local/cuda-11.3.1/include/'),
        ('11.2', '/usr/local/cuda-11.2.2/include/'),
        ('11.1', '/usr/local/cuda-11.1.1/include/'),
        ('11.0', '/usr/local/cuda-11.0.3/include/'),
        ('10.2', '/usr/local/cuda-10.2.0/include/'),
    ],
    'headers': ['cublas_v2.h'],
    'patterns': {
        'function': r'cublas([A-Z][^_]*)(:?_v2|)',
        'type': r'cublas([A-Z].*)_t',
    },
    'functions': {

        # cuBLAS Helper Function

        'cublasCreate_v2': {
            'return': 'handle',
            'except?': 0
        },
        'cublasDestroy_v2': {
            'return': None,
        },
        'cublasGetVersion_v2': {
            'return': 'version',
            'except?': -1,
        },
        'cublasGetProperty': {
            'return': 'value',
            'except?': -1,
        },
        'cublasGetCudartVersion': {
            'return': 'Transparent',
        },
        'cublasSetWorkspace_v2': {
            'return': None,
        },
        'cublasSetStream_v2': {
            'return': None,
        },
        'cublasGetStream_v2': {
            'return': 'streamId',
            'except?': 0,
        },
        'cublasGetPointerMode_v2': {
            'return': 'mode',
            'except?': -1,
        },
        'cublasSetPointerMode_v2': {
            'return': None,
        },
        'cublasGetAtomicsMode': {
            'return': 'mode',
            'except?': -1,
        },
        'cublasSetAtomicsMode': {
            'return': None,
        },
        'cublasGetMathMode': {
            'return': 'mode',
            'except?': -1,
        },
        'cublasSetMathMode': {
            'return': None,
        },
        'cublasGetSmCountTarget': 'pass',
        'cublasSetSmCountTarget': 'pass',
        'cublasLoggerConfigure': 'pass',
        'cublasSetLoggerCallback': 'pass',
        'cublasGetLoggerCallback': 'pass',
        'cublasSetVector': {
            'return': None,
        },
        'cublasGetVector': {
            'return': None,
        },
        'cublasSetMatrix': {
            'return': None,
        },
        'cublasGetMatrix': {
            'return': None,
        },
        'cublasSetVectorAsync': {
            'return': None,
            'stream': 'pass',
        },
        'cublasGetVectorAsync': {
            'return': None,
            'stream': 'pass',
        },
        'cublasSetMatrixAsync': {
            'return': None,
            'stream': 'pass',
        },
        'cublasGetMatrixAsync': {
            'return': None,
            'stream': 'pass',
        },
        'cublasXerbla': 'pass',  # an error handler

        # cuBLAS Level-1 Function and BLAS-like Extension

        'cublasNrm2Ex': {
            'return': None,
            'stream': 'set',
        },
        'cublasSnrm2_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDnrm2_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasScnrm2_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDznrm2_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDotEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasDotcEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasSdot_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDdot_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCdotu_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCdotc_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZdotu_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZdotc_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasScalEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasSscal_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDscal_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCscal_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCsscal_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZscal_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZdscal_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasAxpyEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasSaxpy_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDaxpy_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCaxpy_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZaxpy_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCopyEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasScopy_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDcopy_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCcopy_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZcopy_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasSswap_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDswap_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCswap_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZswap_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasSwapEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasIsamax_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasIdamax_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasIcamax_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasIzamax_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasIamaxEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasIsamin_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasIdamin_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasIcamin_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasIzamin_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasIaminEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasAsumEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasSasum_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDasum_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasScasum_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDzasum_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasSrot_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDrot_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCrot_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCsrot_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZrot_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZdrot_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasRotEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasSrotg_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDrotg_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCrotg_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZrotg_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasRotgEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasSrotm_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDrotm_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasRotmEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasSrotmg_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDrotmg_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasRotmgEx': {
            'return': None,
            'stream': 'set',
        },

        # cuBLAS Level-2 Function and BLAS-like Extension

        'cublasSgemv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDgemv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgemv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZgemv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasSgbmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDgbmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgbmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZgbmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasStrmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDtrmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCtrmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZtrmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasStbmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDtbmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCtbmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZtbmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasStpmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDtpmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCtpmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZtpmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasStrsv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDtrsv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCtrsv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZtrsv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasStpsv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDtpsv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCtpsv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZtpsv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasStbsv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDtbsv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCtbsv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZtbsv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasSsymv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDsymv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCsymv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZsymv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasChemv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZhemv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasSsbmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDsbmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasChbmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZhbmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasSspmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDspmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasChpmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZhpmv_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasSger_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDger_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgeru_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgerc_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZgeru_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZgerc_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasSsyr_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDsyr_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCsyr_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZsyr_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCher_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZher_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasSspr_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDspr_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasChpr_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZhpr_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasSsyr2_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDsyr2_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCsyr2_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZsyr2_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCher2_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZher2_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasSspr2_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDspr2_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasChpr2_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZhpr2_v2': {
            'return': None,
            'stream': 'set',
        },

        # cuBLAS Level-3 Function and BLAS-like Extension

        'cublasSgemm_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDgemm_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgemm_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgemm3m': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgemm3mEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasZgemm_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZgemm3m': {
            'return': None,
            'stream': 'set',
        },
        'cublasSgemmEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasGemmEx': 'pass',  # by hand for compatibility
        'cublasCgemmEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasUint8gemmBias': {
            'return': None,
            'stream': 'set',
        },
        'cublasSsyrk_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDsyrk_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCsyrk_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZsyrk_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCsyrkEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasCsyrk3mEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasCherk_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZherk_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCherkEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasCherk3mEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasSsyr2k_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDsyr2k_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCsyr2k_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZsyr2k_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCher2k_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZher2k_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasSsyrkx': {
            'return': None,
            'stream': 'set',
        },
        'cublasDsyrkx': {
            'return': None,
            'stream': 'set',
        },
        'cublasCsyrkx': {
            'return': None,
            'stream': 'set',
        },
        'cublasZsyrkx': {
            'return': None,
            'stream': 'set',
        },
        'cublasCherkx': {
            'return': None,
            'stream': 'set',
        },
        'cublasZherkx': {
            'return': None,
            'stream': 'set',
        },
        'cublasSsymm_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDsymm_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCsymm_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZsymm_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasChemm_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZhemm_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasStrsm_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDtrsm_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCtrsm_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZtrsm_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasStrmm_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDtrmm_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCtrmm_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZtrmm_v2': {
            'return': None,
            'stream': 'set',
        },
        'cublasSgemmBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasDgemmBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgemmBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgemm3mBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasZgemmBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasGemmBatchedEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasGemmStridedBatchedEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasSgemmStridedBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasDgemmStridedBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgemmStridedBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgemm3mStridedBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasZgemmStridedBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasSgeam': {
            'return': None,
            'stream': 'set',
        },
        'cublasDgeam': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgeam': {
            'return': None,
            'stream': 'set',
        },
        'cublasZgeam': {
            'return': None,
            'stream': 'set',
        },
        'cublasSgetrfBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasDgetrfBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgetrfBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasZgetrfBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasSgetriBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasDgetriBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgetriBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasZgetriBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasSgetrsBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasDgetrsBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgetrsBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasZgetrsBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasStrsmBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasDtrsmBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasCtrsmBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasZtrsmBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasSmatinvBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasDmatinvBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasCmatinvBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasZmatinvBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasSgeqrfBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasDgeqrfBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgeqrfBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasZgeqrfBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasSgelsBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasDgelsBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgelsBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasZgelsBatched': {
            'return': None,
            'stream': 'set',
        },
        'cublasSdgmm': {
            'return': None,
            'stream': 'set',
        },
        'cublasDdgmm': {
            'return': None,
            'stream': 'set',
        },
        'cublasCdgmm': {
            'return': None,
            'stream': 'set',
        },
        'cublasZdgmm': {
            'return': None,
            'stream': 'set',
        },
        'cublasStpttr': {
            'return': None,
            'stream': 'set',
        },
        'cublasDtpttr': {
            'return': None,
            'stream': 'set',
        },
        'cublasCtpttr': {
            'return': None,
            'stream': 'set',
        },
        'cublasZtpttr': {
            'return': None,
            'stream': 'set',
        },
        'cublasStrttp': {
            'return': None,
            'stream': 'set',
        },
        'cublasDtrttp': {
            'return': None,
            'stream': 'set',
        },
        'cublasCtrttp': {
            'return': None,
            'stream': 'set',
        },
        'cublasZtrttp': {
            'return': None,
            'stream': 'set',
        },
    },
}
