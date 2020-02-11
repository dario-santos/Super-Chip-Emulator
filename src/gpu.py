import pygame
import memory as mem
import cpu

# Window size
display_width  = 640
display_height = 320

screen = None

display_buffer = [0] * 32 * 64
draw = True


def initialize(rom):
  global display_width, display_height, screen
  
  screen = pygame.display.set_mode((display_width, display_height))
  pygame.display.flip()
  pygame.display.update()

  rom = rom.split('/')
  rom = rom[len(rom) - 1].split('.')[0]

  pygame.display.set_caption('CHIP8 - ' + rom.capitalize())

def clear_display():
  global draw, display_buffer
  display_buffer = [0] * 32 * 64 
  draw = True

def drawScreen():
  global screen, display_buffer
  black = (0, 0, 0)
  white = (255, 255, 255)
  screen.fill(black)
  for i in range(len(display_buffer)):
    x = int(i % 64)
    y = int(i / 64)
    if display_buffer[i] == 1:
      pygame.draw.rect(screen, white, (x * 10, y * 10, 10, 10))
    else:
      pygame.draw.rect(screen, black, (x * 10, y * 10, 10, 10))

  pygame.display.update()

def draw_sprite(x, y, n):
  global display_buffer, draw
  mem.vn[0xF] = 0

  for dy in range(n):
    line = mem.memory[cpu.I + dy]
    for dx in range(8):

      if (line & (0x80 >> dx)) != 0:
        loc = (x + dx + ((dy + y) << 6)) % 2048

        mem.vn[0xF] |= display_buffer[loc] & 1
        display_buffer[loc] ^= 1

  draw = True
