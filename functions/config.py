import yaml
import os


class Config:

    def get(item):
        script_dir = os.path.dirname(__file__)
        filename = os.path.join(script_dir,"../config.yaml")
        config_file = open(filename)
        config = yaml.safe_load(config_file)
        config_file.close()
        return config[item]

    def getInnested(father, child):
        script_dir = os.path.dirname(__file__)
        filename = os.path.join(script_dir,"../config.yaml")
        config_file = open(filename)
        config = yaml.safe_load(config_file)
        config_file.close()
        return config[father][child]
