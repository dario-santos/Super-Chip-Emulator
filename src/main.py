import sys
import pygame
import time
import sound
import gpu
import input as i
import cpu
import memory as mem
import debug
import config

def main():
  pygame.init()

  # 1 - Start Chip8
  start_emulator(rom_path)

  # Emulation Loop
  running = True
  while running:
    time.sleep(0.0025)
    gpu.draw = False
    cpu.cicle()

    # Emulate one cicle
    if cpu.can_reload:
      running = False
    # Update Input
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

      if event.type == pygame.KEYDOWN and event.key in i.input_scheme:
        i.input_status[i.input_scheme.index(event.key)] = 1
      elif event.type == pygame.KEYUP and event.key in i.input_scheme:
        i.input_status[i.input_scheme.index(event.key)] = 0
    
    # Update GPU
    if gpu.draw:
      gpu.drawScreen()

def start_emulator(rom_path):
  # Start Memory
  mem.load_file(rom_path)
  # Start CPU
  cpu.initialize()
  # Start GPU
  gpu.initialize(rom_path)
  # Start Audio
  sound.initialize()
  # Start Input
  i.initialize()

import os

def print_dir(path):
  l = os.listdir(path)
  l.sort()

  for e in l:
    if os.path.isdir(os.path.join(path, e)): continue
    if os.path.splitext(e)[1] not in ['.ch8', '.c8']:
      l.remove(e)
      
  while True:

    print(0, '-', '../')
    for i, p in enumerate(l):
      tmp_path = path + '/' + p

      print(1 + i, '-', tmp_path)
  
    selected = int(input('Choose a folder/file: '))

    if selected in range(len(l) + 1):
      return os.path.split(path)[0] if selected == 0 else os.path.join(path, l[int(selected) - 1])
  
def room_selector():
  path = '../roms'

  while True:
    path = print_dir(path)
    if path is '': path = '..'
    if os.path.isfile(path): return path

# save_config()
config.load_config() 

if len(sys.argv) == 2:
  rom_path = sys.argv[1] 
    
  if os.path.splitext(rom_path)[1] not in ['.ch8', '.c8']: 
    print('Error - the givin file does not have the extension .ch8 or .c8')
    exit(-1)
else:
  rom_path = room_selector()
    
while True:
  main()
  if not cpu.can_reload: break