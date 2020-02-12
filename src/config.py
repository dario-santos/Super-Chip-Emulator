import configparser

color_background = 0
color_foreground = 0

def save_config():

  config = configparser.ConfigParser()

  config['Chip8'] = {}
  config['Colors'] = {
    'background': '#000000',
    'foreground': '#FFFFFF'
    }

  with open('config.ini', 'w') as configfile:
    config.write(configfile)

def load_config():
  global color_background, color_foreground
  config = configparser.ConfigParser()
  config.read('config.ini')

  color_background = config['Colors']['background']
  color_foreground = config['Colors']['foreground']
