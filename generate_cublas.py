import sys
import os
import os.path

import gen
import gen.util


def _emit_cython_pyx(env, root_path, assets_path):
    print('Generating cuda/libs/cublas.pyx...')

    # Generate external declarations
    external_decls = []
    for name in gen.environment_functions(env):
        external_decls.append(gen.generate_external_declaration(name, env))
    external_decls = gen.util.indent('\n'.join(external_decls))

    # Generate wrapper definitions
    wrapper_defs = []
    for name in gen.environment_functions(env):
        wrapper_defs.append(gen.generate_wrapper_definition(name, env))
    wrapper_defs = '\n\n\n'.join(wrapper_defs)

    # Read the template file
    template_path = os.path.join(assets_path, 'cuda', 'libs', 'cublas.pyx')
    template = gen.read_template(template_path)

    # Write the .pyx file
    out_path = os.path.join(root_path, 'out', 'cuda', 'libs')
    os.makedirs(out_path, exist_ok=True)
    out_path = os.path.join(out_path, 'cublas.pyx')
    with open(out_path, 'w') as f:
        code = template.format(external_decls=external_decls,
                               wrapper_defs=wrapper_defs)
        f.write(code)


def _emit_cython_pxd(env, root_path, assets_path):
    print('Generating cuda/libs/cublas.pxd...')

    # Generate opaque type declarations
    opaque_decls = []
    for name in gen.environment_opaque_types(env):
        opaque_decls.append(gen.generate_opaque_type_declaration(name, env))
    opaque_decls = gen.util.indent('\n'.join(opaque_decls))

    # Generate enum declarations
    enum_decls = []
    enum_values = []
    for name in gen.environment_enums(env):
        decl, values = gen.generate_enum_declaration(name, env)
        enum_decls.append(decl)
        enum_values.append(values)
    enum_decls = gen.util.indent('\n'.join(enum_decls))
    enum_values = '\n\n\n'.join(enum_values)

    # Generate wrapper declarations
    func_decls = []
    for name in gen.environment_functions(env):
        func_decls.append(gen.generate_wrapper_declaration(name, env))
    func_decls = '\n'.join(func_decls)

    # Read the template file
    template_path = os.path.join(assets_path, 'cuda', 'libs', 'cublas.pxd')
    template = gen.read_template(template_path)

    # Write the .pxd file
    out_path = os.path.join(root_path, 'out', 'cuda', 'libs')
    os.makedirs(out_path, exist_ok=True)
    out_path = os.path.join(out_path, 'cublas.pxd')
    with open(out_path, 'w') as f:
        code = template.format(opaque_decls=opaque_decls,
                               enum_decls=enum_decls,
                               enum_values=enum_values,
                               func_decls=func_decls)
        f.write(code)


def _emit_compat_header(env, root_path, assets_path):
    print('Generating cuda/cupy_cublas.h...')

    # Generate compat stubs
    compat = []
    versions = gen.environment_versions(env)
    for old, new in zip(versions[:-1], versions[1:]):
        opaque_added, opaque_removed = (
            gen.environment_opaque_types_diff(env, old, new))
        enum_added, enum_removed = gen.environment_enums_diff(env, old, new)
        func_added, func_removed = (
            gen.environment_functions_diff(env, old, new))

        if enum_added or opaque_added or func_added:
            compat.append(gen.util.compat_section_header(new, 'added'))
        for name in enum_added:
            compat.append(gen.generate_enum_stub(name, env))
        for name in opaque_added:
            compat.append(gen.generate_opaque_type_stub(name, env))
        for name in func_added:
            compat.append(gen.generate_function_stub(name, env))
        if enum_added or opaque_added or func_added:
            compat.append(gen.util.compat_section_footer(new, 'added'))

        if enum_removed or opaque_removed or func_removed:
            compat.append(gen.util.compat_section_header(new, 'removed'))
        for name in enum_removed:
            compat.append(gen.generate_enum_stub(name, env))
        for name in opaque_removed:
            compat.append(gen.generate_opaque_type_stub(name, env))
        for name in func_removed:
            compat.append(gen.generate_function_stub(name, env))
        if enum_removed or opaque_removed or func_removed:
            compat.append(gen.util.compat_section_footer(new, 'removed'))
    compat = '\n\n'.join(compat)

    # Read the template file
    template_path = os.path.join(assets_path, 'cuda', 'cupy_cublas.h')
    template = gen.read_template(template_path)

    # Write the header file
    out_path = os.path.join(root_path, 'out', 'cuda')
    os.makedirs(out_path, exist_ok=True)
    out_path = os.path.join(out_path, 'cupy_cublas.h')
    with open(out_path, 'w') as f:
        code = template.format(compat=compat)
        f.write(code)


def _emit_stub_header(env, root_path, assets_path):
    print('Generating stub/cupy_cublas.h...')

    # Generate function stubs
    stubs = []
    for name in gen.environment_functions(env):
        stubs.append(gen.generate_function_stub(name, env))
    stubs = '\n\n'.join(stubs)

    # Read the template file
    template_path = os.path.join(assets_path, 'stub', 'cupy_cublas.h')
    template = gen.read_template(template_path)

    # Write the header file
    out_path = os.path.join(root_path, 'out', 'stub')
    os.makedirs(out_path, exist_ok=True)
    out_path = os.path.join(out_path, 'cupy_cublas.h')
    with open(out_path, 'w') as f:
        code = template.format(stubs=stubs)
        f.write(code)


def main(args):
    root_path = os.path.dirname(__file__)
    assets_path = os.path.join(root_path, 'cublas_assets')

    # Read the configuration file
    config_path = os.path.join(assets_path, 'config.py')
    config = gen.read_config(config_path)

    # Read header files of each CUDA version
    headers = gen.parse_headers(config)

    # Analyze the header files across the CUDA versions and get an environment
    # out of them
    env = gen.analyze_headers(headers, config)

    # Emit output files
    _emit_cython_pyx(env, root_path, assets_path)     # cuda/libs/cublas.pyx
    _emit_cython_pxd(env, root_path, assets_path)     # cuda/libs/cublas.pxd
    _emit_compat_header(env, root_path, assets_path)  # cuda/cupy_cublas.h
    _emit_stub_header(env, root_path, assets_path)    # stub/cupy_cublas.h
    # _emit_hip_header()     # hip/cupy_hipblas.h
    print('Done')


if __name__ == '__main__':
    main(sys.argv[1:])
