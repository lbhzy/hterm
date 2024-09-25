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
        self.dir = os.path.join(base_dir, "profile")
        self.config = os.path.join(self.dir, f"{type}.yaml")

    def loadConfig(self):
        with open(self.config, 'r', encoding="utf-8") as file:
            cfg = yaml.safe_load(file)
        return cfg

    def addConfig(self, item):
        cfg = self.loadConfig()
        cfg.append(item)
        with open(self.config, 'w') as file:
            for item in cfg:           
                yaml.safe_dump([item], file, sort_keys=False)
                file.write("\n")

    def getConfigByName(self, name):
        cfg = self.loadConfig()
        for item in cfg:
            if item['name'] == name:
                return item



if __name__ == "__main__":

    config = Config("session")
    config.loadConfig()
    cfg = {
        'name': 'hello',
        'protocol': 'serial'
    }
    config.addConfig(cfg)
    cfg = config.getConfigByName("openwrt")
    print(cfg)