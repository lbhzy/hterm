import os
import sys
import yaml

class Config:
    """ 配置文件处理 """
    def __init__(self, type):
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.argv[0])
        else:
            base_dir = os.path.dirname(os.path.dirname(__file__))
        self.dir = os.path.join(base_dir, "profiles")
        self.path = os.path.join(self.dir, f"{type}.yaml")

        # 文件路径不存在则创建
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        if not os.path.isfile(self.path):
            with open(self.path, 'w') as f:
                pass

        with open(self.path, 'r', encoding="utf-8") as file:
            self.cfg = yaml.safe_load(file)
        if not self.cfg:
            self.cfg = []

    def loadConfig(self):
        return self.cfg

    def addConfig(self, item):
        self.cfg.append(item)
        with open(self.path, 'w', encoding="utf-8") as file:
            for item in self.cfg:           
                yaml.safe_dump([item], file, sort_keys=False)
                file.write("\n")

    def getConfigByName(self, name):
        for item in self.cfg:
            if item['name'] == name:
                return item
            
    def saveNewConfig(self, cfg):
        self.cfg = cfg
        with open(self.path, 'w', encoding="utf-8") as file:
            for item in cfg:           
                yaml.safe_dump([item], file, sort_keys=False, allow_unicode=True)
                file.write("\n")


if __name__ == "__main__":

    config = Config("test")
    config.loadConfig()
    cfg = {
        'name': 'hello',
        'protocol': 'serial'
    }
    config.addConfig(cfg)
    cfg = config.getConfigByName("openwrt")
    print(cfg)