import os
import sys
import yaml


class Color():
    """ 终端配色方案 """
    def __init__(self):
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.argv[0])
        else:
            base_dir = os.path.dirname(os.path.dirname(__file__))
        
        self.schemes_dir = os.path.join(base_dir, "schemes")

        self.great_scheme_bright = ["Homebrew Light"]
        self.great_scheme_dark = ["Horizon Dark"]

    def getSchemes(self):
        schemes = []
        names = os.listdir(self.schemes_dir)
        for name in names:
            schemes.append(os.path.splitext(name)[0])
        return schemes

    def getScheme(self, scheme):
        with open(os.path.join(self.schemes_dir, f'{scheme}.yml'), 'r') as file:
            scheme_dict = yaml.safe_load(file)

        scheme = {}
        for key, value in scheme_dict.items():
            match key:
                case 'color_01':
                    scheme.update({'Black': value, '30': value})
                case 'color_02':
                    scheme.update({'Red': value, '31': value})
                case 'color_03':
                    scheme.update({'Green': value, '32': value})
                case 'color_04':
                    scheme.update({'Yellow': value, '33': value})
                case 'color_05':
                    scheme.update({'Blue': value, '34': value})
                case 'color_06':
                    scheme.update({'Magenta': value, '35': value})
                case 'color_07':
                    scheme.update({'Cyan': value, '36': value})
                case 'color_08':
                    scheme.update({'White': value, '37': value})
                case 'color_09':
                    scheme.update({'Bright Black': value, '40': value})
                case 'color_10':
                    scheme.update({'Bright Red': value, '41': value})
                case 'color_11':
                    scheme.update({'Bright Green': value, '42': value})
                case 'color_12':
                    scheme.update({'Bright Yellow': value, '43': value})
                case 'color_13':
                    scheme.update({'Bright Blue': value, '44': value})
                case 'color_14':
                    scheme.update({'Bright Magenta': value, '45': value})
                case 'color_15':
                    scheme.update({'Bright Cyan': value, '46': value})
                case 'color_16':
                    scheme.update({'Bright White': value, '47': value})
                case 'background':
                    scheme.update({'Background': value})
                case 'foreground':
                    scheme.update({'Foreground': value})
                case 'cursor':
                    scheme.update({'Cursor': value})
        return scheme
                

if __name__ == "__main__":

    color = Color()
    print(color.getSchemes())
    print(color.getScheme("Terminix Dark"))