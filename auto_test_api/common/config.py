from configparser import ConfigParser
from common.contants import CONF_DIR
import os



class myconf(ConfigParser):

    def __init__(self, filename, encoding="utf8"):
        # 调用父类原来的init方法
        super().__init__()
        self.filename = filename
        self.encoding = encoding
        self.read(filename, encoding)
        #section 包含的是ini配置文件中[]的内容
    def write_data(self, section, option, value):
        self.set(section, option, value)  #这里只是更新了从ini文件中读取出来的键值，实际ini文件内容没有被修改
        # with open(self.filename, 'w') as f:
        #     conf.write(f)
        self.write(open(self.filename, "w", encoding=self.encoding)) #这一步修改原ini文件中内容

conf = myconf(os.path.join(CONF_DIR, "conf.ini"))



