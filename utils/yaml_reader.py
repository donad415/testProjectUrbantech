import yaml
from yaml import Loader


def read_yaml(yaml_file_path):
    with open(yaml_file_path, 'rb') as f:
        cf = f.read()
    cf = yaml.load(cf, Loader=Loader)
    return cf
