import configparser

color_background = 0
color_foreground = 0

keyboard_keys = []

def save_config():
  config = configparser.ConfigParser()

  config['Chip8'] = {}
  
  config['Colors'] = {
    'background': '#2C3A47',
    'foreground': '#ecf0f1'
    }
  
  config['Keyboard'] = {
    'key_0x0': 'x',
    'key_0x1': '1',
    'key_0x2': '2',
    'key_0x3': '3',
    'key_0x4': 'q',
    'key_0x5': 'w',
    'key_0x6': 'e',
    'key_0x7': 'a',
    'key_0x8': 's',
    'key_0x9': 'd',
    'key_0xA': 'z',
    'key_0xB': 'c',
    'key_0xC': '4',
    'key_0xD': 'r',
    'key_0xE': 'f',
    'key_0xF': 'v'
    }

  with open('config.ini', 'w') as configfile:
    config.write(configfile)

def load_config():
  global color_background, color_foreground, keyboard_keys
  config = configparser.ConfigParser()
  config.read('config.ini')

  color_background = config['Colors']['background']
  color_foreground = config['Colors']['foreground']

  for i in config['Keyboard']:
    keyboard_keys.append(config['Keyboard'][i])
