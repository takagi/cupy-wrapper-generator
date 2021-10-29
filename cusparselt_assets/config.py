{
    'versions': [
        ('0.2.0', '/home/ext-mtakagi/cusparselt/0.2.0/libcusparse_lt/include/'),
        ('0.1.0', '/home/ext-mtakagi/cusparselt/0.1.0/libcusparse_lt/include/'),
        ('0.0.1', '/home/ext-mtakagi/cusparselt/0.0.1/libcusparse_lt/include/'),
    ],
    'headers': ['cusparseLt.h'],
    'patterns': {
        'function': r'cusparseLt([A-Z][^_]*)',
        'type': r'cusparseLt([A-Z].*)_t',
    },
    'functions': {
        'cusparseLtMatDescriptorDestroy': {
            'return': None,
        },
        'cusparseLtMatmulDescSetAttribute': {
            'return': None,
        },
        'cusparseLtMatmulDescGetAttribute': {
            'return': None,
        },
        'cusparseLtMatDescSetAttribute': {
            'return': None,
        },
        'cusparseLtMatDescGetAttribute': {
            'return': None,
        },
    },
}
