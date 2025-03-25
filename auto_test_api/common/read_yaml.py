import yaml


class ReadYaml(object):

    def __init__(self, filename):
        self.filename = filename

    def read_yaml(self):
        with open(self.filename, encoding="utf-8") as f:
            datas = yaml.load(f, Loader=yaml.FullLoader)
            for value in datas:
                for casedatas in value["cases"]:
                    casedatas["json"] = str(casedatas["json"])
                    casedatas["expected"] = str(casedatas["expected"])
            if isinstance(value, dict):
                return value
