import pygame as pg
import config

# The input scheme
#
#  Original Keyboard     Emulator Keyboard
#  +---+---+---+---+     +---+---+---+---+
#  |0x1|0x2|0x3|0xC|     | 1 | 2 | 3 | 4 |
#  +---+---+---+---+     +---+---+---+---+
#  |0x4|0x5|0x6|0xD|     | Q | W | E | R | 
#  +---+---+---+---+  >> +---+---+---+---+ 
#  |0x7|0x8|0x9|0xE|     | A | S | D | F | 
#  +---+---+---+---+     +---+---+---+---+
#  |0xA|0x0|0xB|0xF|     | Z | X | C | V |
#  +---+---+---+---+     +---+---+---+---+
#

input_scheme = [
  'x',   # X - 0x0

  '1',   # 1 - 0x1 
  '2',   # 2 - 0x2
  '3',   # 3 - 0x3
  
  'q',   # Q - 0x4
  'w',   # W - 0x5
  'e',   # E - 0x6
  
  'a',   # A - 0x7
  's',   # S - 0x8
  'd',   # D - 0x9
  
  'z',   # Z - 0xA
  'c',   # C - 0xB
  '4',   # 4 - 0xC
  'r',   # R - 0xD
  'f',   # F - 0xE
  'v',   # V - 0xF
]

input_status = [0] * 16

def initialize():
  global input_status, input_scheme
  input_scheme = config.keyboard_keys.copy()
  input_status = [0] * 16

def is_key_pressed(keycode):
  global input_status
  return input_status[keycode] == 1
