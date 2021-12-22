import yaml

class Config:


    def get(item):
        config_file = open("/home/marco/appNewsMail/master/config.yaml")
        config = yaml.load(config_file)
        return config[item]

    def getInnested(father,child):
        config_file = open("/home/marco/appNewsMail/master/config.yaml")
        config = yaml.load(config_file)
        return config[father][child]
