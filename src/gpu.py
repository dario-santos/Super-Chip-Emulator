import pygame
import memory as mem
import cpu
# Exented mode 64 * 128
# Non extended mode 32 * 64

modifier_normal   = 2
modifier_extended = 1

# Window size
display_width  = 128
display_height = 64

screen = None
display_buffer = []
draw = True

def initialize(rom):
  global display_width, display_height, screen, display_buffer, modifier_normal, modifier_extended

  modifier = modifier_extended if cpu.is_extended else modifier_normal

  display_buffer = [0] * display_height * display_width * modifier

  screen = pygame.display.set_mode((display_width* 10, display_height* 10))
  pygame.display.flip()
  pygame.display.update()

  rom = rom.split('/')
  rom = rom[len(rom) - 1].split('.')[0]

  pygame.display.set_caption('CHIP8/SCHIP - ' + rom.capitalize())

def clear_display():
  global draw, display_buffer, modifier_normal, modifier_extended, display_height, display_width
  modifier = modifier_extended if cpu.is_extended else modifier_normal
  display_buffer = [0] * display_height * display_width

  draw = True

def drawScreen():
  global screen, display_buffer, modifier_extended, modifier_normal
  modifier = modifier_extended if cpu.is_extended else modifier_normal
  display_width = int(128 / modifier)
  
  black = (44, 58, 71)
  white = (236, 240, 241)
  screen.fill(black)
  for i in range(len(display_buffer)):
    x = int(i % display_width)
    y = int(i / display_width)
    if display_buffer[i] == 1:
      pygame.draw.rect(screen, white, (x * 10 * modifier, y * 10 * modifier, 10 * modifier, 10 * modifier))
    else:
      pygame.draw.rect(screen, black, (x * 10 * modifier, y * 10 * modifier, 10 * modifier, 10 * modifier))

  pygame.display.update()

def draw_sprite(x, y, n):
  global display_buffer, draw, modifier_normal, modifier_extended
  
  modifier = modifier_extended if cpu.is_extended else modifier_normal
  display_width = int(128 / modifier) 
  mem.vn[0xF] = 0

  for dy in range(n):
    line = mem.memory[cpu.I + dy]
    for dx in range(8):
      _x = (x + dx) % display_width
      _y = y + dy

      if _y > display_width - 1 or _y < 0 : continue

      if (line & (0x80 >> dx)) != 0:
        loc = (_x+ (_y << 6))

        mem.vn[0xF] |= display_buffer[loc] & 1
        display_buffer[loc] ^= 1

  draw = True
