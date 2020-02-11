import pygame

input_scheme = [
  pygame.K_1,   # 1 - 0x0 
  pygame.K_2,   # 2 - 0x1
  pygame.K_3,   # 3 - 0x2
  pygame.K_4,   # 4 - 0x3
  
  pygame.K_q,   # Q - 0x4
  pygame.K_w,   # W - 0x5
  pygame.K_e,   # E - 0x6
  pygame.K_r,   # R - 0x7

  pygame.K_a,   # A - 0x4
  pygame.K_s,   # S - 0x5
  pygame.K_d,   # D - 0x6
  pygame.K_f,   # F - 0x7

  pygame.K_z,   # Z - 0x4
  pygame.K_x,   # X - 0x5
  pygame.K_c,   # C - 0x6
  pygame.K_v,   # V - 0x7
]

input_status = [0] * 16

def is_key_pressed(keycode):
  global input_status
  return input_status[keycode] == 1
