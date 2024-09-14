import os
import sys
import yaml

class Color():
    """ 终端配色方案 """

    def __init__(self):

        self.scheme = {}
        self.schemes = []
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.argv[0])
        else:
            base_dir = os.path.dirname(os.path.dirname(__file__))
        self.schemes_dir = os.path.join(base_dir, "schemes")

        self.great_scheme_bright = ["Homebrew Light"]
        self.great_scheme_dark = ["Horizon Dark"]

        self.getSchemes()
        self.setScheme("Horizon Dark")

    def getSchemes(self):
        if self.schemes:
            return self.schemes
        names = os.listdir(self.schemes_dir)
        for name in names:
            self.schemes.append(os.path.splitext(name)[0])


    def setScheme(self, scheme):
        if not scheme in self.schemes:
            return
        with open(os.path.join(self.schemes_dir, f'{scheme}.yml'), 'r') as file:
            scheme_dict = yaml.safe_load(file)
        
        self.scheme.clear()
        for key, value in scheme_dict.items():
            match key:
                case 'color_01':
                    self.scheme.update({'Black': value, '30': value})
                case 'color_02':
                    self.scheme.update({'Red': value, '31': value})
                case 'color_03':
                    self.scheme.update({'Green': value, '32': value})
                case 'color_04':
                    self.scheme.update({'Yellow': value, '33': value})
                case 'color_05':
                    self.scheme.update({'Blue': value, '34': value})
                case 'color_06':
                    self.scheme.update({'Magenta': value, '35': value})
                case 'color_07':
                    self.scheme.update({'Cyan': value, '36': value})
                case 'color_08':
                    self.scheme.update({'White': value, '37': value})
                case 'color_09':
                    self.scheme.update({'Bright Black': value, '40': value})
                case 'color_10':
                    self.scheme.update({'Bright Red': value, '41': value})
                case 'color_11':
                    self.scheme.update({'Bright Green': value, '42': value})
                case 'color_12':
                    self.scheme.update({'Bright Yellow': value, '43': value})
                case 'color_13':
                    self.scheme.update({'Bright Blue': value, '44': value})
                case 'color_14':
                    self.scheme.update({'Bright Magenta': value, '45': value})
                case 'color_15':
                    self.scheme.update({'Bright Cyan': value, '46': value})
                case 'color_16':
                    self.scheme.update({'Bright White': value, '47': value})
                case 'background':
                    self.scheme.update({'Background': value})
                case 'foreground':
                    self.scheme.update({'Foreground': value})
                case 'cursor':
                    self.scheme.update({'Cursor': value})
                


if __name__ == "__main__":

    c = Color()
    print(c.schemes)
    c.setScheme("Terminix Dark")
    print(c.scheme)