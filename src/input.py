import pygame as pg

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
  pg.K_x,   # X - 0x0

  pg.K_1,   # 1 - 0x1 
  pg.K_2,   # 2 - 0x2
  pg.K_3,   # 3 - 0x3
  
  pg.K_q,   # Q - 0x4
  pg.K_w,   # W - 0x5
  pg.K_e,   # E - 0x6
  
  pg.K_a,   # A - 0x7
  pg.K_s,   # S - 0x8
  pg.K_d,   # D - 0x9
  
  pg.K_z,   # Z - 0xA
  pg.K_c,   # C - 0xB
  pg.K_4,   # 4 - 0xC
  pg.K_r,   # R - 0xD
  pg.K_f,   # F - 0xE
  pg.K_v,   # V - 0xF
]

input_status = [0] * 16

def is_key_pressed(keycode):
  global input_status
  return input_status[keycode] == 1
