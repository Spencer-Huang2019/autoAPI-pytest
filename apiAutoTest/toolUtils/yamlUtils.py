import yaml

class Yaml(object):

    def __init__(self, filePath):
        self.filePath = filePath

    def readYaml(self):
        with open(self.filePath, "r", encoding= "utf-8") as f:
            data = yaml.load(f.read(), Loader=yaml.FullLoader)
        return data