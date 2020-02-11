import sys
import pygame
import sound
import gpu
import input
import cpu
import memory as mem

def main():

  if len(sys.argv) != 2:
    print("Error: invalid number of arguments.")
    print("Example of usage: python3 main.py path/to/rom.c8")
    return
  
  rom_path = sys.argv[1]
  pygame.init()

  # 1 - Start Chip8
  
  # Load and setup memory
  mem.load_file(rom_path)

  # Setup CPU and GPU
  cpu.initialize()
  gpu.initialize(rom_path)
  sound.initialize()

  # Emulation Loop
  running = True
  
  while running:
    # Emulate one cicle
    cpu.cicle()
    
    # Update Input
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

      if event.type == pygame.KEYDOWN and event.key in input.input_scheme:
        input.input_status[input.input_scheme.index(event.key)] = 1
      elif event.type == pygame.KEYUP and event.key in input.input_scheme:
        input.input_status[input.input_scheme.index(event.key)] = 0
    
    # Update GPU
    pygame.display.flip()
    pygame.display.update()

main()