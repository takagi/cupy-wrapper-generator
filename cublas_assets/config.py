{
    'cuda': {
        'versions': [
            ('10.2', '/usr/local/cuda-10.2.0/include/'),
            ('11.0', '/usr/local/cuda-11.0.3/include/'),
            ('11.1', '/usr/local/cuda-11.1.1/include/'),
            ('11.2', '/usr/local/cuda-11.2.2/include/'),
            ('11.3', '/usr/local/cuda-11.3.1/include/'),
            ('11.4', '/usr/local/cuda-11.4.1/include/'),
        ],
        'headers': ['cublas_v2.h'],
        'patterns': {
            'function': r'cublas([A-Z][^_]*)',
            'type': r'cublas([A-Z].*)_t',
        },
    },
    'hip': {
        'versions': [
            ('3.10', '/opt/rocm-3.10.0/include/'),
            ('4.0', '/opt/rocm-4.0.0/include/'),
            ('4.1', '/opt/rocm-4.1.1/include/'),
            ('4.2', '/opt/rocm-4.2.0/include/'),
            ('4.3', '/opt/rocm-4.3.1/include/'),
        ],
        'headers': ['hipblas.h'],
        'prefix': 'hipblas',
    },
    'functions': {

        # cuBLAS Helper Function

        'cublasCreate': {
            'return': 'handle',
            'except?': 0,
        },
        'cublasDestroy': {
            'return': None,
        },
        'cublasGetVersion': {
            'return': 'version',
            'except?': -1,
            'hip': 'skip',  # by hand
        },
        'cublasGetProperty': {
            'return': 'value',
            'except?': -1,
        },
        'cublasGetCudartVersion': {
            'return': 'Transparent',
        },
        'cublasSetWorkspace': {
            'return': None,
        },
        'cublasSetStream': {
            'return': None,
        },
        'cublasGetStream': {
            'return': 'streamId',
            'except?': 0,
        },
        'cublasGetPointerMode': {
            'return': 'mode',
            'except?': -1,
        },
        'cublasSetPointerMode': {
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
            'hip': 'not-supported',
        },
        'cublasSetMathMode': {
            'return': None,
        },
        'cublasGetSmCountTarget': 'skip',
        'cublasSetSmCountTarget': 'skip',
        'cublasLoggerConfigure': 'skip',
        'cublasSetLoggerCallback': 'skip',
        'cublasGetLoggerCallback': 'skip',
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
        'cublasXerbla': 'skip',  # an error handler

        # cuBLAS Level-1 Function and BLAS-like Extension

        'cublasNrm2Ex': {
            'return': None,
            'stream': 'set',
        },
        'cublasSnrm2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDnrm2': {
            'return': None,
            'stream': 'set',
        },
        'cublasScnrm2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDznrm2': {
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
        'cublasSdot': {
            'return': None,
            'stream': 'set',
        },
        'cublasDdot': {
            'return': None,
            'stream': 'set',
        },
        'cublasCdotu': {
            'return': None,
            'stream': 'set',
        },
        'cublasCdotc': {
            'return': None,
            'stream': 'set',
        },
        'cublasZdotu': {
            'return': None,
            'stream': 'set',
        },
        'cublasZdotc': {
            'return': None,
            'stream': 'set',
        },
        'cublasScalEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasSscal': {
            'return': None,
            'stream': 'set',
        },
        'cublasDscal': {
            'return': None,
            'stream': 'set',
        },
        'cublasCscal': {
            'return': None,
            'stream': 'set',
        },
        'cublasCsscal': {
            'return': None,
            'stream': 'set',
        },
        'cublasZscal': {
            'return': None,
            'stream': 'set',
        },
        'cublasZdscal': {
            'return': None,
            'stream': 'set',
        },
        'cublasAxpyEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasSaxpy': {
            'return': None,
            'stream': 'set',
        },
        'cublasDaxpy': {
            'return': None,
            'stream': 'set',
        },
        'cublasCaxpy': {
            'return': None,
            'stream': 'set',
        },
        'cublasZaxpy': {
            'return': None,
            'stream': 'set',
        },
        'cublasCopyEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasScopy': {
            'return': None,
            'stream': 'set',
        },
        'cublasDcopy': {
            'return': None,
            'stream': 'set',
        },
        'cublasCcopy': {
            'return': None,
            'stream': 'set',
        },
        'cublasZcopy': {
            'return': None,
            'stream': 'set',
        },
        'cublasSswap': {
            'return': None,
            'stream': 'set',
        },
        'cublasDswap': {
            'return': None,
            'stream': 'set',
        },
        'cublasCswap': {
            'return': None,
            'stream': 'set',
        },
        'cublasZswap': {
            'return': None,
            'stream': 'set',
        },
        'cublasSwapEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasIsamax': {
            'return': None,
            'stream': 'set',
        },
        'cublasIdamax': {
            'return': None,
            'stream': 'set',
        },
        'cublasIcamax': {
            'return': None,
            'stream': 'set',
        },
        'cublasIzamax': {
            'return': None,
            'stream': 'set',
        },
        'cublasIamaxEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasIsamin': {
            'return': None,
            'stream': 'set',
        },
        'cublasIdamin': {
            'return': None,
            'stream': 'set',
        },
        'cublasIcamin': {
            'return': None,
            'stream': 'set',
        },
        'cublasIzamin': {
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
        'cublasSasum': {
            'return': None,
            'stream': 'set',
        },
        'cublasDasum': {
            'return': None,
            'stream': 'set',
        },
        'cublasScasum': {
            'return': None,
            'stream': 'set',
        },
        'cublasDzasum': {
            'return': None,
            'stream': 'set',
        },
        'cublasSrot': {
            'return': None,
            'stream': 'set',
        },
        'cublasDrot': {
            'return': None,
            'stream': 'set',
        },
        'cublasCrot': {
            'return': None,
            'stream': 'set',
        },
        'cublasCsrot': {
            'return': None,
            'stream': 'set',
        },
        'cublasZrot': {
            'return': None,
            'stream': 'set',
        },
        'cublasZdrot': {
            'return': None,
            'stream': 'set',
        },
        'cublasRotEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasSrotg': {
            'return': None,
            'stream': 'set',
        },
        'cublasDrotg': {
            'return': None,
            'stream': 'set',
        },
        'cublasCrotg': {
            'return': None,
            'stream': 'set',
        },
        'cublasZrotg': {
            'return': None,
            'stream': 'set',
        },
        'cublasRotgEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasSrotm': {
            'return': None,
            'stream': 'set',
        },
        'cublasDrotm': {
            'return': None,
            'stream': 'set',
        },
        'cublasRotmEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasSrotmg': {
            'return': None,
            'stream': 'set',
        },
        'cublasDrotmg': {
            'return': None,
            'stream': 'set',
        },
        'cublasRotmgEx': {
            'return': None,
            'stream': 'set',
        },

        # cuBLAS Level-2 Function and BLAS-like Extension

        'cublasSgemv': {
            'return': None,
            'stream': 'set',
        },
        'cublasDgemv': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgemv': {
            'return': None,
            'stream': 'set',
        },
        'cublasZgemv': {
            'return': None,
            'stream': 'set',
        },
        'cublasSgbmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasDgbmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgbmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasZgbmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasStrmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasDtrmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasCtrmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasZtrmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasStbmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasDtbmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasCtbmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasZtbmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasStpmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasDtpmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasCtpmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasZtpmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasStrsv': {
            'return': None,
            'stream': 'set',
        },
        'cublasDtrsv': {
            'return': None,
            'stream': 'set',
        },
        'cublasCtrsv': {
            'return': None,
            'stream': 'set',
        },
        'cublasZtrsv': {
            'return': None,
            'stream': 'set',
        },
        'cublasStpsv': {
            'return': None,
            'stream': 'set',
        },
        'cublasDtpsv': {
            'return': None,
            'stream': 'set',
        },
        'cublasCtpsv': {
            'return': None,
            'stream': 'set',
        },
        'cublasZtpsv': {
            'return': None,
            'stream': 'set',
        },
        'cublasStbsv': {
            'return': None,
            'stream': 'set',
        },
        'cublasDtbsv': {
            'return': None,
            'stream': 'set',
        },
        'cublasCtbsv': {
            'return': None,
            'stream': 'set',
        },
        'cublasZtbsv': {
            'return': None,
            'stream': 'set',
        },
        'cublasSsymv': {
            'return': None,
            'stream': 'set',
        },
        'cublasDsymv': {
            'return': None,
            'stream': 'set',
        },
        'cublasCsymv': {
            'return': None,
            'stream': 'set',
        },
        'cublasZsymv': {
            'return': None,
            'stream': 'set',
        },
        'cublasChemv': {
            'return': None,
            'stream': 'set',
        },
        'cublasZhemv': {
            'return': None,
            'stream': 'set',
        },
        'cublasSsbmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasDsbmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasChbmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasZhbmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasSspmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasDspmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasChpmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasZhpmv': {
            'return': None,
            'stream': 'set',
        },
        'cublasSger': {
            'return': None,
            'stream': 'set',
        },
        'cublasDger': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgeru': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgerc': {
            'return': None,
            'stream': 'set',
        },
        'cublasZgeru': {
            'return': None,
            'stream': 'set',
        },
        'cublasZgerc': {
            'return': None,
            'stream': 'set',
        },
        'cublasSsyr': {
            'return': None,
            'stream': 'set',
        },
        'cublasDsyr': {
            'return': None,
            'stream': 'set',
        },
        'cublasCsyr': {
            'return': None,
            'stream': 'set',
        },
        'cublasZsyr': {
            'return': None,
            'stream': 'set',
        },
        'cublasCher': {
            'return': None,
            'stream': 'set',
        },
        'cublasZher': {
            'return': None,
            'stream': 'set',
        },
        'cublasSspr': {
            'return': None,
            'stream': 'set',
        },
        'cublasDspr': {
            'return': None,
            'stream': 'set',
        },
        'cublasChpr': {
            'return': None,
            'stream': 'set',
        },
        'cublasZhpr': {
            'return': None,
            'stream': 'set',
        },
        'cublasSsyr2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDsyr2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCsyr2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZsyr2': {
            'return': None,
            'stream': 'set',
        },
        'cublasCher2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZher2': {
            'return': None,
            'stream': 'set',
        },
        'cublasSspr2': {
            'return': None,
            'stream': 'set',
        },
        'cublasDspr2': {
            'return': None,
            'stream': 'set',
        },
        'cublasChpr2': {
            'return': None,
            'stream': 'set',
        },
        'cublasZhpr2': {
            'return': None,
            'stream': 'set',
        },

        # cuBLAS Level-3 Function and BLAS-like Extension

        'cublasSgemm': {
            'return': None,
            'stream': 'set',
        },
        'cublasDgemm': {
            'return': None,
            'stream': 'set',
        },
        'cublasCgemm': {
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
        'cublasZgemm': {
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
            'hip': 'skip',  # by hand
        },
        'cublasGemmEx': 'skip',  # by hand for compatibility
        'cublasCgemmEx': {
            'return': None,
            'stream': 'set',
        },
        'cublasUint8gemmBias': {
            'return': None,
            'stream': 'set',
        },
        'cublasSsyrk': {
            'return': None,
            'stream': 'set',
        },
        'cublasDsyrk': {
            'return': None,
            'stream': 'set',
        },
        'cublasCsyrk': {
            'return': None,
            'stream': 'set',
        },
        'cublasZsyrk': {
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
        'cublasCherk': {
            'return': None,
            'stream': 'set',
        },
        'cublasZherk': {
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
        'cublasSsyr2k': {
            'return': None,
            'stream': 'set',
        },
        'cublasDsyr2k': {
            'return': None,
            'stream': 'set',
        },
        'cublasCsyr2k': {
            'return': None,
            'stream': 'set',
        },
        'cublasZsyr2k': {
            'return': None,
            'stream': 'set',
        },
        'cublasCher2k': {
            'return': None,
            'stream': 'set',
        },
        'cublasZher2k': {
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
        'cublasSsymm': {
            'return': None,
            'stream': 'set',
        },
        'cublasDsymm': {
            'return': None,
            'stream': 'set',
        },
        'cublasCsymm': {
            'return': None,
            'stream': 'set',
        },
        'cublasZsymm': {
            'return': None,
            'stream': 'set',
        },
        'cublasChemm': {
            'return': None,
            'stream': 'set',
        },
        'cublasZhemm': {
            'return': None,
            'stream': 'set',
        },
        'cublasStrsm': {
            'return': None,
            'stream': 'set',
        },
        'cublasDtrsm': {
            'return': None,
            'stream': 'set',
        },
        'cublasCtrsm': {
            'return': None,
            'stream': 'set',
        },
        'cublasZtrsm': {
            'return': None,
            'stream': 'set',
        },
        'cublasStrmm': {
            'return': None,
            'stream': 'set',
            'hip': 'not-supported',
        },
        'cublasDtrmm': {
            'return': None,
            'stream': 'set',
            'hip': 'not-supported',
        },
        'cublasCtrmm': {
            'return': None,
            'stream': 'set',
            'hip': 'not-supported',
        },
        'cublasZtrmm': {
            'return': None,
            'stream': 'set',
            'hip': 'not-supported',
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
        'cublasGemmBatchedEx': 'skip',  # by hand for compatibility
        'cublasGemmStridedBatchedEx': 'skip',  # by hand for compatibility
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
