import video
import input
import cpu
import pygame


def main():
  # Setup graphics and Input
  pygame.init()

  # Initialize Chip8 system and load the game
  cpu.load_file("pong2.c8")
  video.initialize()

  # Emulation Loop
  running = True
  
  while running:
    # Emulate one cicle *)
    cpu.cicle()
    
    # Update Input
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

      if event.type == pygame.KEYDOWN and event.key in input.input_scheme:
        input.input_status[input.input_scheme.index(event.key)] = 1
      elif event.type == pygame.KEYUP and event.key in input.input_scheme:
        input.input_status[input.input_scheme.index(event.key)] = 0
    
    pygame.display.flip()
    pygame.display.update()

main()