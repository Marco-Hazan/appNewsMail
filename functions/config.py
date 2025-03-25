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

    def set(item,value):
        with open('config.yaml') as f:
            doc = yaml.safe_load(f)
        doc[item] = value
        with open('config.yaml', 'w') as f:
            yaml.dump(doc, f)
