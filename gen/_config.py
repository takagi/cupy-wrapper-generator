import ast


def read_config(path):
    with open(path, 'r') as f:
        config_str = f.read()
    return ast.literal_eval(config_str)
