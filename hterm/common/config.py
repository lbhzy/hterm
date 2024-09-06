import os
import yaml

class Config:
    """ 配置文件处理 """
    def __init__(self) -> None:
        self.dir = f"{os.path.dirname(__file__)}/../profile/"
        self.session_config = self.dir + "session.yaml"
        self.treminal_config = self.dir + "terminal.yaml"

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