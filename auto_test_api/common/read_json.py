import json




class ReadJson(object):

    def __init__(self, filename):
        self.filename = filename

    def read_json(self):
        with open(self.filename, 'rb') as f:
            datas = json.load(f)
            for value in datas:
                return value
        #     for casedatas in value["cases"]:
        #             return casedatas
        #             a = casedatas["json"]
        #             print(a )
        #             casedatas["expected"] = str(casedatas["expected"])
        #     if isinstance(value, dict):
        #             return value


if __name__ == '__main__':
    self_read_json = ReadJson("/test_data\\test_fdp_login_cases.json")
    ret = self_read_json.read_json()
    print(ret)