import pygame
import cpu

# Window size
display_width  = 640
display_height = 320

screen = None

def initialize():
  global display_width, display_height, screen
  
  screen = pygame.display.set_mode((display_width, display_height))
  pygame.display.flip()
  pygame.display.update()


  pygame.display.set_caption('CHIP8 - Keypad Test')

def clear_display():
  global screen
  screen.fill((0, 0, 0))


def draw_pixel(color, x, y):
  r = pygame.Rect(x * 10, y * 10, 10, 10)
  pygame.draw.rect(screen, color, r)


def is_pixel_white(x, y):
  global screen
  return  1 if screen.get_at((x, y)) == (255, 255, 255) else 0
  
def draw_sprite(x, y, n):
  for dy in range(n):
    
    line = cpu.memory[cpu.I + dy]

    for dx in range(8):
      _x = (x + dx) % 64
      _y = y + dy 

      color = (line >> (7 - dx)) & 0x1

      cpu.vn[0xF] = color ^ is_pixel_white(_x, _y)

      if color == 1:  
        color = (255, 255, 255)
      else:
        color = (0,0,0)

      draw_pixel(color, _x, _y)
