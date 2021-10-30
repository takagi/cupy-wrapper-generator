import os
import os.path
import sys

import gen
import gen.util


def _emit_cython_pyx(env, assets_dir, out_dir):
    print('Generating cuda/libs/cusparse.pyx...')

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

    # Emit the outcome
    template_path = os.path.join(assets_dir, 'cuda', 'libs', 'cusparse.pyx')
    out_path = os.path.join(out_dir, 'cuda', 'libs', 'cusparse.pyx')
    gen.util.emit(out_path, template_path,
                  external_decls=external_decls,
                  wrapper_defs=wrapper_defs)


def main(args):
    root_dir = os.path.dirname(__file__)
    assets_dir = os.path.join(root_dir, 'cusparse_assets')
    out_dir = os.path.join(root_dir, 'out')

    # Read the configuration file
    config_path = os.path.join(assets_dir, 'config.py')
    config = gen.read_config(config_path)

    # Read header files of each CUDA version
    cuda_nodes = gen.parse_headers(config['cuda'], 'cuda')
    hip_nodes = gen.parse_headers(config['hip'], 'hip')

    # Analyze the header files across the CUDA versions and get an environment
    # out of them
    env = gen.analyze_headers(cuda_nodes, hip_nodes, config)

    # Emit output files
    _emit_cython_pyx(env, assets_dir, out_dir)     # cuda/libs/cusparse.pyx
    print('Done.')


if __name__ == '__main__':
    main(sys.argv[1:])
