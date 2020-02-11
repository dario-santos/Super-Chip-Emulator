import random
import video
import input

fontset = [
  0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
  0x20, 0x60, 0x20, 0x20, 0x70, # 1
  0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
  0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
  0x90, 0x90, 0xF0, 0x10, 0x10, # 4
  0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
  0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
  0xF0, 0x10, 0x20, 0x40, 0x40, # 7
  0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
  0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
  0xF0, 0x90, 0xF0, 0x90, 0x90, # A
  0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
  0xF0, 0x80, 0x80, 0x80, 0xF0, # C
  0xE0, 0x90, 0x90, 0x90, 0xE0, # D
  0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
  0xF0, 0x80, 0xF0, 0x80, 0x80  # F
]


# Memory ram - 4KB
memory = [0] * 4096

# Registers: One of the 16 available variables
vn = [0] * 16

# The Stack - Used for returns, normally has 48 bytes and 12 levels
stack = []

# Timers 
timer_delay = 0
timer_sound = 0

pc     = 0x200
opcode = 0
I      = 0

def initialize():
  global timer_delay, timer_sound, memory, fontset

  # Load fontset
  for i in range(80):
    memory[i] = fontset[i]

  # Reset timers
  timer_delay = 0
  timer_sound = 0

def cicle ():
  global opcode, timer_delay, timer_sound, memory, pc
  # One emulation cicle
      
  #1 - Fetch Opcode

  """
    Merging two successive bytes to form the opcode

    memory.(!pc)     = 00000000 10100010
    memory.(!pc + 1) = 00000000 11110000

    a) shift the top 8 bits
    10100010 << 8    = 10100010 00000000

    b) merge the two bytes
    10100010 00000000 | 
    00000000 11110000
    -------------------
    10100010 11110000

  """
  opcode = (memory[pc] << 8) | memory[pc + 1]

  # 2 - Decode and Execute Opcode
  decode(opcode)

  # 3 - Update timers
  timer_delay = timer_delay - 1 if timer_delay > 0 else timer_delay

  if timer_sound > 0:
    if timer_sound == 1: 
      print('Beep \a')

    timer_sound -= 1
    
def decode(opcode):
  global memory, vn, stack, timer_delay, timer_sound, pc, I
  oc  = opcode >> 12
  x   = (opcode & 0x0F00) >> 8
  y   = (opcode & 0x00F0) >> 4
  c   = opcode & 0x000F
  nn  = opcode & 0x00FF
  nnn = opcode & 0x0FFF
  
  # print_debug(opcode)
  
  if oc == 0x0 and x == 0x0 and y == 0xE and c == 0x0:   # Clears the screen.
    video.clear_display()
    pc += 2
  elif oc == 0x0 and x == 0x0 and y == 0xE and c == 0xE: # Returns from a subroutine.
    pc = stack.pop()
    pc += 2
  elif oc == 0x0:
    assert False
  elif oc == 0x1: # Jumps to address NNN.
    pc = nnn
  elif oc == 0x2: # Calls subroutine at NNN.
    stack.append(pc)
    pc = nnn
  elif oc == 0x3: # Skips the next instruction if VN(X) equals NN.
    pc = pc + 4 if vn[x] == nn else pc + 2
  elif oc == 0x4: # Skips the next instruction if VN(X) doesn't equal NN.
    pc = pc + 4 if vn[x] != nn else pc + 2
  elif oc == 0x5 and c == 0x0: # Skips the next instruction if VX equals VY.
    pc = pc + 4 if vn[x] == vn[y] else pc + 2
  elif oc == 0x6: # Assigns the value of NN to VX.
    vn[x] = nn
    pc += 2
  elif oc == 0x7: # Adds NN to VX.
    vn[x] += nn
    pc += 2
  elif oc == 0x8 and c == 0x0: # Sets VX to the value of VY.
    vn[x] = vn[y]
    pc += 2
  elif oc == 0x8 and c == 0x1: # Sets VX to VX or VY. (Bitwise OR operation)
    vn[x] = vn[x] | vn[y]
    pc += 2
  elif oc == 0x8 and c == 0x2: # Sets VX to VX and VY. (Bitwise AND operation)
    vn[x] = vn[x] & vn[y]
    pc += 2
  elif oc == 0x8 and c == 0x3: # Sets VX to VX xor VY. (Bitwise XOR operation)
    vn[x] = vn[x] ^ vn[y]
    pc += 2
  elif oc == 0x8 and c == 0x4: # Adds VY to VX. VF is set to 1 when there's a carry, and to 0 when there isn't.
    vn[0xF] = 1  if vn[y] > (0xFF - vn[x]) else 0
    vn[x] = vn[x] + vn[y]
    pc += 2
  elif oc == 0x8 and c == 0x5: # VY is subtracted from VX. VF is set to 0 when there's a borrow, and 1 when there isn't
    vn[0xF] = 0 if vn[y] > vn[x] else 1
    vn[x] -= vn[y]
    pc += 2
  elif oc == 0x8 and c == 0x6: # Stores the least significant bit of VX in VF and then shifts VX to the right by 1.
    vn[0xF] = vn[x] and 0x1
    vn[x] = vn[x] >> 1
    pc += 2
  elif oc == 0x8 and c == 0x7: # Sets VX to VY minus VX. VF is set to 0 when there's a borrow, and 1 when there isn't.
    vn[0xF] = 0 if vn[x] > vn[y] else 1
    vn[x] = vn[y] - vn[x]
    pc += 2
  elif oc == 0x8 and c == 0xE: # Stores the most significant bit of VX in VF and then shifts VX to the left by 1.
    vn[0xF] = vn[x] >> 7
    vn[x] = vn[x] << 1
    pc += 2
  elif oc == 0x9 and c == 0x0: # Skips the next instruction if VX doesn't equal VY.
    pc = pc + 4 if vn[x] != vn[y] else pc + 2
  elif oc == 0xA: # Sets I to the address NNN.
    I = nnn
    pc += 2
  elif oc == 0xB: # Jumps to the address NNN plus V0.
    pc = vn[0x0] + nnn
  elif oc == 0xC: # Sets VX to the result of a bitwise and operation on a random number (Typically: 0 to 255) and NN.
    vn[x] = (random.randint(0, 255)) & nn;
    pc += 2
  elif oc == 0xD: # Draws a sprite at coordinate (VX, VY).
    vn[0xF] = 0
    video.draw_sprite(vn[x], vn[y], c)
    pc += 2
  elif oc == 0xE and y == 0x9 and c == 0xE: # Skips the next instruction if the key stored in VX is pressed.
    if input.is_key_pressed(vn[x]): pc += 2
    pc += 2
  elif oc == 0xE and y == 0xA and c == 0x1: # Skips the next instruction if the key stored in VX isn't pressed.
    if not input.is_key_pressed(vn[x]): pc += 2
    pc += 2
  elif oc == 0xF and y == 0x0 and c == 0x7: # Sets VX to the value of the delay timer.
    vn[x] = timer_delay
    pc += 2
  elif oc == 0xF and y == 0x0 and c == 0xA:
    assert False
  elif oc == 0xF and y == 0x1 and c == 0x5: # Sets the delay timer to VX.
    timer_delay = vn[x]
    pc += 2
  elif oc == 0xF and y == 0x1 and c == 0x8: # Sets the sound timer to VX.
    timer_sound = vn[x]
    pc += 2
  elif oc == 0xF and y == 0x1 and c == 0xE: # Adds VX to I. VF is set to 1 when there is a range overflow 0 otherwise.
    vn[0xF] = 1 if I + vn[x] > 0xFFF else 0
    I += vn[x] 
    pc += 2
  elif oc == 0xF and y == 0x2 and c == 0x9: # Sets I to the location of the sprite for the character in VX.
    I = vn[x] * 0x5
    pc += 2
  elif oc == 0xF and y == 0x3 and c == 0x3:
    memory[I]     = int (vn[(opcode & 0x0F00) >> 8] / 100)
    memory[I + 1] = int ((vn[(opcode & 0x0F00) >> 8] / 10) % 10)
    memory[I + 2] = int ((vn[(opcode & 0x0F00) >> 8] % 100) % 10)
    pc += 2
  elif oc == 0xF and y == 0x5 and c == 0x5: # Stores V0 to VX (including VX) in memory starting at address I.
    for j in range(x + 1):
      memory[I + j] = vn[j]
    pc += 2 
  elif oc == 0xF and y == 0x6 and c == 0x5: # Fills V0 to VX (including VX) with values from memory starting at address I.
    for j in range(x + 1):
      vn[j] = memory[I + j]
    pc += 2
  else:
    assert False 

import os

def load_file(rom):
  global memory
  
  initialize()
  
  # Load the ROM into RAM.
  
  with open(rom, 'rb') as rom:
    rom_length = os.fstat(rom.fileno()).st_size

    if rom_length > 0xFFF - 0x200 + 1: 
      raise "The given file is too big to be a CHIP-8 ROM."
  
    for i in range(0, rom_length):
      memory[0x200 + i] = int.from_bytes(rom.read(1), "big")

load_file('pong2.c8')


import time
def print_debug(opcode):
  global memory, vn, stack, timer_delay, timer_sound, pc, I
  print('opcode:    ', hex(opcode))
  print('pc:    ', pc)
  print('I:    ', I)
  print('timer_delay:    ', timer_delay)
  print('timer_sound:    ', timer_sound)
  print('vn:    ', vn)
  #print('memory:    ', memory)

  time.sleep(0)