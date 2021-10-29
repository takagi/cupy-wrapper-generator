import os.path
import string
import sys

import gen


def _emit_cython_pyx(env, root_path, assets_path):
    print('Generating cuda/libs/cusparselt.pyx...')

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
    template_path = os.path.join(assets_path, 'cuda', 'libs', 'cusparselt.pyx')
    template = gen.read_template(template_path)

    # Write the .pyx file
    out_path = os.path.join(root_path, 'out', 'cuda', 'libs')
    os.makedirs(out_path, exist_ok=True)
    out_path = os.path.join(out_path, 'cusparselt.pyx')
    with open(out_path, 'w') as f:
        code = string.Template(template).substitute(
            external_decls=external_decls, wrapper_defs=wrapper_defs)
        f.write(code)


def _emit_cython_pxd(env, root_path, assets_path):
    print('Generating cuda/libs/cusparselt.pxd...')

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
    template_path = os.path.join(assets_path, 'cuda', 'libs', 'cusparselt.pxd')
    template = gen.read_template(template_path)

    # Write the .pxd file
    out_path = os.path.join(root_path, 'out', 'cuda', 'libs')
    os.makedirs(out_path, exist_ok=True)
    out_path = os.path.join(out_path, 'cusparselt.pxd')
    with open(out_path, 'w') as f:
        code = string.Template(template).substitute(
            opaque_decls=opaque_decls, enum_decls=enum_decls,
            enum_values=enum_values, func_decls=func_decls)
        f.write(code)


def main(args):
    root_path = os.path.dirname(__file__)
    assets_path = os.path.join(root_path, 'cusparselt_assets')

    # Read the configuration file
    config_path = os.path.join(assets_path, 'config.py')
    config = gen.read_config(config_path)

    # Read header files of each CUDA version
    headers = gen.parse_headers(config)

    # Analyze the header files across the CUDA versions and get an environment
    # out of them
    env = gen.analyze_headers(headers, [], config)

    # Emit output files
    _emit_cython_pyx(env, root_path, assets_path)  # cuda/libs/cusparselt.pyx
    _emit_cython_pxd(env, root_path, assets_path)  # cuda/libs/cusparselt.pxd


if __name__ == '__main__':
    main(sys.argv[1:])
