import os
import sys
import yaml

class Config:
    """ 配置文件处理 """
    def __init__(self) -> None:
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.argv[0])
        else:
            base_dir = os.path.dirname(os.path.dirname(__file__))
        self.dir = os.path.join(base_dir, "profile")
        self.session_config = os.path.join(self.dir, "session.yaml")
        self.treminal_config = os.path.join(self.dir, "terminal.yaml")

    def loadConfig(self):
        with open(self.session_config, 'r') as file:
            cfg = yaml.safe_load(file)
        return cfg

    def addConfig(self, item):
        cfg = self.loadConfig()
        cfg.append(item)
        with open(self.session_config, 'w') as file:
            for item in cfg:           
                yaml.safe_dump([item], file, sort_keys=False)
                file.write("\n")

    def getConfigByName(self, name):
        cfg = self.loadConfig()
        for item in cfg:
            if item['name'] == name:
                return item



if __name__ == "__main__":

    config = Config()
    config.loadConfig()
    cfg = {
        'name': 'hello',
        'protocol': 'serial'
    }
    config.addConfig(cfg)
    cfg = config.getConfigByName("openwrt")
    print(cfg)