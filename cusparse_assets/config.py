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
        'headers': ['cusparse.h'],
        'patterns': {
            'function': r'cusparse([A-Z].*)',
            'type': r'cusparse([A-Z].*)_t',
        },
    },
    'hip': {
        'versions': [
            # ('3.10', '/opt/rocm-3.10.0/include/'),
            # ('4.0', '/opt/rocm-4.0.0/include/'),
            # ('4.1', '/opt/rocm-4.1.1/include/'),
            # ('4.2', '/opt/rocm-4.2.0/include/'),
            ('4.3', '/opt/rocm-4.3.1/include/'),
        ],
        'headers': ['hipsparse.h'],
        'prefix': 'hipsparse',
    },
    'functions': {
        # INITIALIZATION AND MANAGEMENT ROUTINES

        'cusparseCreate': {
            'return': 'handle',
        },
        'cusparseDestroy': {
            'return': None,
        },
        'cusparseSetStream': {
            'return': None,
        },
        'cusparseGetStream': {
            'return': 'streamId',
        },
        'cusparseGetPointerMode': {
            'return': 'mode',
        },
        'cusparseSetPointerMode': {
            'return': None,
        },

        # HELPER ROUTINES

        'cusparseCreateMatDescr': {
            'return': 'descrA',
        },
        'cusparseDestroyMatDescr': {
            'return': None,
        },
        'cusparseCopyMatDescr': 'skip',  # not documented
        'cusparseSetMatType': {
            'return': None,
        },
        'cusparseGetMatType': {
            'return': 'Transparent',
        },
        'cusparseSetMatFillMode': {
            'return': None,
        },
        'cusparseGetMatFillMode': {
            'return': 'Transparent',
        },
        'cusparseSetMatDiagType': {
            'return': None,
        },
        'cusparseGetMatDiagType': {
            'return': 'Transparent',
        },
        'cusparseSetMatIndexBase': {
            'return': None,
        },
        'cusparseGetMatIndexBase': {
            'return': 'Transparent',
        },
        'cusparseCreateSolveAnalysisInfo': {
            'return': 'info',
        },
        'cusparseDestroySolveAnalysisInfo': {
            'return': None,
        },
        'cusparseGetLevelInfo': {
            'return': None,
        },
        'cusparseCreateCsrsv2Info': {
            'return': 'info',
        },
        'cusparseDestroyCsrsv2Info': {
            'return': None,
        },
        'cusparseCreateCsric02Info': {
            'return': 'info',
        },
        'cusparseDestroyCsric02Info': {
            'return': None,
        },
        'cusparseCreateBsric02Info': {
            'return': 'info',
        },
        'cusparseDestroyBsric02Info': {
            'return': None,
        },
        'cusparseCreateCsrilu02Info': {
            'return': 'info',
        },
        'cusparseDestroyCsrilu02Info': {
            'return': None,
        },
        'cusparseCreateBsrilu02Info': {
            'return': 'info',
        },
        'cusparseDestroyBsrilu02Info': {
            'return': None,
        },
        'cusparseCreateBsrsv2Info': {
            'return': 'info',
        },
        'cusparseDestroyBsrsv2Info': {
            'return': None,
        },
        'cusparseCreateBsrsm2Info': {
            'return': 'info',
        },
        'cusparseDestroyBsrsm2Info': {
            'return': None,
        },
        'cusparseCreateHybMat': {
            'return': 'hybA',
        },
        'cusparseDestroyHybMat': {
            'return': None,
        },
        'cusparseCreateCsru2csrInfo': {
            'return': 'info',
        },
        'cusparseDestroyCsru2csrInfo': {
            'return': None,
        },
        'cusparseCreateColorInfo': {
            'return': 'info',
        },
        'cusparseDestroyColorInfo': {
            'return': None,
        },
        'cusparseSetColorAlgs': 'skip',  # not documented
        'cusparseGetColorAlgs': 'skip',  # not documented
        'cusparseCreatePruneInfo': {
            'return': 'info',
        },
        'cusparseDestroyPruneInfo': {
            'return': None,
        },

        # SPARSE LEVEL 1 ROUTINES

        'cusparse<t>axpyi': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>doti': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>dotci': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>gthr': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>gthrz': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>sctr': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>roti': {
            'return': None,
            'stream': 'set',
        },

        # SPARSE LEVEL 2 ROUTINES

        'cusparse<t>gemvi': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>gemvi_bufferSize': {
            'return': 'pBufferSize',
            'stream': 'set',
            'except?': 0,
        },
        'cusparse<t>csrmv': {
            'return': None,
            'stream': 'set',
        },
        'cusparseCsrmvEx': {
            'return': None,
            'stream': 'set',
        },
        'cusparseCsrmvEx_bufferSize': {
            'return': 'bufferSizeInBytes',
            'stream': 'set',
            'except?': 0,
        },
        'cusparse<t>csrmv_mp': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>hybmv': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>bsrmv': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>bsrxmv': {
            'return': None,
            'stream': 'set',
        },
        'cusparseCsrsv_analysisEx': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>csrsv_analysis': {
            'return': None,
            'stream': 'set',
        },
        'cusparseCsrsv_solveEx': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>csrsv_solve': {
            'return': None,
            'stream': 'set',
        },
        'cusparseXcsrsv2_zeroPivot': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>csrsv2_bufferSize': {
            'return': 'pBufferSizeInBytes',
            'stream': 'set',
            'except?': 0,
        },
        'cusparse<t>csrsv2_bufferSizeExt': {
            'return': 'pBufferSize',
            'stream': 'set',
            'except?': 0,
        },
        'cusparse<t>csrsv2_analysis': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>csrsv2_solve': {
            'return': None,
            'stream': 'set',
        },
        'cusparseXbsrsv2_zeroPivot': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>bsrsv2_bufferSize': {
            'return': 'pBufferSizeInBytes',
            'stream': 'set',
            'except?': 0,
        },
        'cusparse<t>bsrsv2_bufferSizeExt': {
            'return': 'pBufferSize',
            'stream': 'set',
            'except?': 0,
        },
        'cusparse<t>bsrsv2_analysis': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>bsrsv2_solve': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>hybsv_analysis': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>hybsv_solve': {
            'return': None,
            'stream': 'set',
        },

        # SPARSE LEVEL 3 ROUTINES

        'cusparse<t>csrmm': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>csrmm2': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>bsrmm': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>gemmi': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>csrsm_analysis': {
            'return': None,
            'stream': 'set',
        },
        'cusparse<t>csrsm_solve': {
            'return': None,
            'stream': 'set',
        },

        # PRECONDITIONERS

        # EXTRA ROUTINES

        # SPARSE MATRIX REORDERING

        # SPARSE FORMAT CONVERSION

        # SPARSE FORMAT CONVERSION #

        # SPARSE MATRIX SORTING

        # CSR2CSC

        # SPARSE VECTOR DESCRIPTOR

        # DENSE VECTOR DESCRIPTOR

        # SPARSE MATRIX DESCRIPTOR

        # DENSE MATRIX DESCRIPTOR

        # VECTOR-VECTOR OPERATIONS

        'cusparseAxpby': {
            'return': None,
            'stream': 'set',
        },
        'cusparseGather': {
            'return': None,
            'stream': 'set',
        },
        'cusparseScatter': {
            'return': None,
            'stream': 'set',
        },
        'cusparseRot': {
            'return': None,
            'stream': 'set',
        },
        'cusparseSpVV_bufferSize': {
            'return':  'bufferSize',
            'stream': 'set',
            'except?': 0,
        },
        'cusparseSpVV': {
            'return':  None,
            'stream': 'set',
        },

        # SPARSE TO DENSE

        'cusparseSparseToDense_bufferSize': {
            'return': 'bufferSize',
            'stream': 'set',
            'except?': 0,
        },
        'cusparseSparseToDense': {
            'return': None,
        },

        # DENSE TO SPARSE

        'cusparseDenseToSparse_bufferSize': {
            'return': 'bufferSize',
            'stream': 'set',
            'except?': 0,
        },
        'cusparseDenseToSparse_analysis': {
            'return': None,
            'stream': 'set',
        },
        'cusparseDenseToSparse_convert': {
            'return': None,
            'stream': 'set',
        },

        # SPARSE MATRIX-VECTOR MULTIPLICATION

        'cusparseSpMV': {
            'return': None,
            'stream': 'set',
        },
        'cusparseSpMV_bufferSize': {
            'return': 'bufferSize',
            'stream': 'set',
            'except?': 0,
        },

        # SPARSE TRIANGULAR VECTOR SOLVE

        'cusparseSpSV_createDescr': {
            'return': 'descr',
        },
        'cusparseSpSV_destroyDescr': {
            'return': None,
        },
        'cusparseSpSV_bufferSize': {
            'return': 'bufferSize',
            'stream': 'set',
            'except?': 0,
        },
        'cusparseSpSV_analysis': {
            'return': None,
            'stream': 'set',
        },
        'cusparseSpSV_solve': {
            'return': None,
            'stream': 'set',
        },

        # SPARSE TRIANGULAR MATRIX SOLVE

        'cusparseSpSM_createDescr': {
            'return': 'descr',
        },
        'cusparseSpSM_destroyDescr': {
            'return': None,
        },
        'cusparseSpSM_bufferSize': {
            'return': 'bufferSize',
            'stream': 'set',
            'except?': 0,
        },
        'cusparseSpSM_analysis': {
            'return': None,
            'stream': 'set',
        },
        'cusparseSpSM_solve': {
            'return': None,
            'stream': 'set',
        },

        # SPARSE MATRIX-MATRIX MULTIPLICATION

        'cusparseSpMM_bufferSize': {
            'return': 'bufferSize',
            'stream': 'set',
            'except?': 0
        },
        'cusparseSpMM_preprocess': {
            'return': None,
            'stream': 'set',
        },
        'cusparseSpMM': {
            'return': None,
            'stream': 'set',
        },

        # SPARSE MATRIX - SPARSE MATRIX MULTIPLICATION (SpGEMM)

        'cusparseSpGEMM_createDescr': {
            'return': 'descr',
        },
        'cusparseSpGEMM_destroyDescr': {
            'return': None,
        },
        'cusparseSpGEMM_workEstimation': {
            'return': None,
            'stream': 'set',
        },
        'cusparseSpGEMM_compute': {
            'return': None,
            'stream': 'set',
        },
        'cusparseSpGEMM_copy': {
            'return': None,
            'stream': 'set',
        },

        # SPARSE MATRIX - SPARSE MATRIX MULTIPLICATION (SpGEMM) STRUCTURE REUSE

        # SAMPLED DENSE-DENSE MATRIX MULTIPLICATION
    },
}
