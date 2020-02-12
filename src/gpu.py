import pygame
import memory as mem
import cpu
import config

# Exented mode      64 * 128
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
  global screen, display_buffer, display_width, display_height, modifier_normal, modifier_extended

  modifier = modifier_extended if cpu.is_extended else modifier_normal

  display_buffer = [0] * int((display_height * display_width) / modifier)

  screen = pygame.display.set_mode((display_width * 10, display_height * 10))
  pygame.display.flip()
  pygame.display.update()

  rom = rom.split('/')
  rom = rom[len(rom) - 1].split('.')[0]

  pygame.display.set_caption('CHIP8/SCHIP - ' + rom.capitalize())

def clear_display():
  global draw, display_buffer, modifier_normal, modifier_extended, display_height, display_width
  modifier = modifier_extended if cpu.is_extended else modifier_normal

  display_buffer = [0] * int((display_height * display_width) / modifier)

  draw = True

def drawScreen():
  global screen, display_buffer, modifier_extended, modifier_normal
  modifier = modifier_extended if cpu.is_extended else modifier_normal
  display_width = int(128 / modifier)
  
  black = pygame.Color(config.color_background)
  white = pygame.Color(config.color_foreground)
  screen.fill(black)
  for i in range(len(display_buffer)):
    x = int(i % display_width)
    y = int(i / display_width)
    if display_buffer[i] == 1:
      pygame.draw.rect(screen, white, (x * 10 * modifier, y * 10 * modifier, 10 * modifier, 10 * modifier))
    else:
      pygame.draw.rect(screen, black, (x * 10 * modifier, y * 10 * modifier, 10 * modifier, 10 * modifier))

  pygame.display.update()

def draw_super_sprite(x, y):
  global display_buffer, draw
  
  if not cpu.is_extended:
    draw_sprite(x, y, 16)
    return

  mem.vn[0xF] = 0

  for dy in range(16):
    line = (mem.memory[cpu.I + dy] << 8) | mem.memory[cpu.I + dy + 1]

    for dx in range(16):
      _x = (x + dx) % 128
      _y = y + dy

      if _y > 63 or _y < 0 : continue

      if (line & (0x8000 >> dx)) != 0:
        loc = (_x + (_y << 7))

        # print('SUPER DRAW', _x, _y, loc, len(display_buffer))
        mem.vn[0xF] |= display_buffer[loc] & 1
        display_buffer[loc] ^= 1

  draw = True

def draw_sprite(x, y, n):
  global display_buffer, draw, modifier_normal, modifier_extended
  modifier = modifier_extended if cpu.is_extended else modifier_normal

  display_width = 128 if cpu.is_extended else 64
  display_height = 64 if cpu.is_extended else 32
  mem.vn[0xF] = 0

  for dy in range(n):
    line = mem.memory[cpu.I + dy]
    for dx in range(8):
      _x = (x + dx) % display_width
      _y = y + dy

      if _y > display_height - 1 or _y < 0 : continue

      if (line & (0x80 >> dx)) != 0:
        loc = (_x + (_y << (8 - modifier)))
        mem.vn[0xF] |= display_buffer[loc] & 1
        display_buffer[loc] ^= 1

  draw = True

def change_mode():
  global display_buffer, display_height, display_width, modifier
  modifier = modifier_extended if cpu.is_extended else modifier_normal

  display_buffer = [0] * int((display_height * display_width) / modifier)

def scroll_down(n):
  global display_buffer, draw

  old_display_buffer = display_buffer.copy()
  display_buffer = [0] * 128 * 64

  for y in range(64 - n):
    for x in range(128):
      display_buffer[x + (y + n) * 128] = old_display_buffer[x + y * 128]
        
  draw = True

def scroll_right(is_extended):
  global display_buffer, draw

  translation = 4 if is_extended else 2

  old_display_buffer = display_buffer.copy()
  display_buffer = [0] * 128 * 64

  for y in range(64):
    for x in range(128 - translation):
      display_buffer[(x + translation) + y * 128] = old_display_buffer[x + y * 128]
     
  draw = True

def scroll_left(is_extended):
  global display_buffer, draw

  translation = 4 if is_extended else 2

  old_display_buffer = display_buffer.copy()
  display_buffer = [0] * 128 * 64

  for y in range(64):
    for x in range(128 - translation):
      display_buffer[x + y * 128] = old_display_buffer[(x + translation) + y * 128]
     
  draw = True
