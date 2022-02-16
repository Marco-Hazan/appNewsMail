import yaml


class Config:

    def get(item):
        config_file = open("/home/marco/appNewsMail/master/config.yaml")
        config = yaml.safe_load(config_file)
        config_file.close()
        return config[item]

    def getInnested(father, child):
        config_file = open("/home/marco/appNewsMail/master/config.yaml")
        config = yaml.safe_load(config_file)
        config_file.close()
        return config[father][child]
