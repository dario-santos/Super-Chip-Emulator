import random
import gpu
import input
import sound
import memory as mem

# PC : Program Counter
pc     = 0
# Adress Register - 16 bits
I      = 0
opcode = 0

# Timers 
timer_delay = 0
timer_sound = 0

def initialize():
  global pc, timer_delay, timer_sound

  # The first 512 bytes are occuped by the CHIP8 itself
  # So the starting position of the program counter is 0x200
  pc = 0x200

  # Reset timers
  timer_delay = 0
  timer_sound = 0

def cicle ():
  global timer_delay, timer_sound, opcode, pc
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
  opcode = (mem.memory[pc] << 8) | mem.memory[pc + 1]

  # 2 - Decode and Execute Opcode
  decode(opcode)

  # 3 - Update timers
  if timer_delay > 0: timer_delay -= 1

  if timer_sound > 0:
    if timer_sound == 1: sound.play()

    timer_sound -= 1
    
def decode(opcode):
  global timer_delay, timer_sound, pc, I
  oc  = opcode >> 12
  x   = (opcode & 0x0F00) >> 8
  y   = (opcode & 0x00F0) >> 4
  c   = opcode & 0x000F
  nn  = opcode & 0x00FF
  nnn = opcode & 0x0FFF
    
  if oc == 0x0 and x == 0x0 and y == 0xE and c == 0x0:   # CLS - Clead the display
    gpu.clear_display()
    pc += 2
  elif oc == 0x0 and x == 0x0 and y == 0xE and c == 0xE: # RET - Returns from a subroutine
    pc = mem.stack.pop()
    pc += 2
  elif oc == 0x0 and x == 0x0 and y == 0xC assert False
  elif oc == 0x0 and x == 0x0 and y == 0xF and c == 0xB assert False
  elif oc == 0x0 and x == 0x0 and y == 0xF and c == 0xC assert False
  elif oc == 0x0 and x == 0x0 and y == 0xF and c == 0xD assert False
  elif oc == 0x0 and x == 0x0 and y == 0xF and c == 0xE assert False
  elif oc == 0x0 and x == 0x0 and y == 0xF and c == 0xF assert False
  elif oc == 0x0: pc += 2 # Jump to a machine code routine at nnn. - Ignored by modern interpreters
  elif oc == 0x1: # JP addr - Jumps to location NNN
    pc = nnn
  elif oc == 0x2: # CALL addr - Calls subroutine at NNN
    mem.stack.append(pc)
    pc = nnn
  elif oc == 0x3: # Skips the next instruction if VN(X) equals NN.
    pc = pc + 4 if mem.vn[x] == nn else pc + 2
  elif oc == 0x4: # Skips the next instruction if VN(X) doesn't equal NN.
    pc = pc + 4 if mem.vn[x] != nn else pc + 2
  elif oc == 0x5 and c == 0x0: # Skips the next instruction if VX equals VY.
    pc = pc + 4 if mem.vn[x] == mem.vn[y] else pc + 2
  elif oc == 0x6: # Assigns the value of NN to VX.
    mem.vn[x] = nn & 0xFF
    pc += 2
  elif oc == 0x7: # Adds NN to VX.
    mem.vn[x] += nn
    mem.vn[x] &= 0xFF
    pc += 2
  elif oc == 0x8 and c == 0x0: # Sets VX to the value of VY.
    mem.vn[x] = mem.vn[y] & 0xFF
    pc += 2
  elif oc == 0x8 and c == 0x1: # Sets VX to VX or VY. (Bitwise OR operation)
    mem.vn[x] = mem.vn[x] | mem.vn[y]
    mem.vn[x] &= 0xFF
    pc += 2
  elif oc == 0x8 and c == 0x2: # Sets VX to VX and VY. (Bitwise AND operation)
    mem.vn[x] = mem.vn[x] & mem.vn[y]
    mem.vn[x] &= 0xFF
    pc += 2
  elif oc == 0x8 and c == 0x3: # Sets VX to VX xor VY. (Bitwise XOR operation)
    mem.vn[x] = mem.vn[x] ^ mem.vn[y]
    mem.vn[x] &= 0xFF
    pc += 2
  elif oc == 0x8 and c == 0x4: # Adds VY to VX. VF is set to 1 when there's a carry, and to 0 when there isn't.
    mem.vn[0xF] = 1  if mem.vn[y] > (0xFF - mem.vn[x]) else 0
    mem.vn[x] += mem.vn[y]
    mem.vn[x] &= 0xFF
    pc += 2
  elif oc == 0x8 and c == 0x5: # VY is subtracted from VX. VF is set to 0 when there's a borrow, and 1 when there isn't
    mem.vn[0xF] = 0 if mem.vn[y] > mem.vn[x] else 1
    mem.vn[x] -= mem.vn[y]
    mem.vn[x] &= 0xFF
    pc += 2
  elif oc == 0x8 and c == 0x6: # Stores the least significant bit of VX in VF and then shifts VX to the right by 1.
    mem.vn[0xF] = mem.vn[x] & 0x1
    mem.vn[x] = mem.vn[x] >> 1
    pc += 2
  elif oc == 0x8 and c == 0x7: # Sets VX to VY minus VX. VF is set to 0 when there's a borrow, and 1 when there isn't.
    mem.vn[0xF] = 0 if mem.vn[x] > mem.vn[y] else 1
    mem.vn[x] = mem.vn[y] - mem.vn[x]
    mem.vn[x] &= 0xFF
    pc += 2
  elif oc == 0x8 and c == 0xE: # Stores the most significant bit of VX in VF and then shifts VX to the left by 1.
    mem.vn[0xF] = mem.vn[x] >> 7
    mem.vn[x] = mem.vn[x] << 1
    mem.vn[x] &= 0xFF
    pc += 2
  elif oc == 0x9 and c == 0x0: # Skips the next instruction if VX doesn't equal VY.
    pc = pc + 4 if mem.vn[x] != mem.vn[y] else pc + 2
  elif oc == 0xA: # Sets I to the address NNN.
    I = nnn
    pc += 2
  elif oc == 0xB: # Jumps to the address NNN plus V0.
    pc = mem.vn[0x0] + nnn
  elif oc == 0xC: # Sets VX to the result of a bitwise and operation on a random number (Typically: 0 to 255) and NN.
    mem.vn[x] = (random.randint(0, 255)) & nn
    mem.vn[x] &= 0xFF
    pc += 2
  elif oc == 0xD: # Draws a sprite at coordinate (VX, VY).
    gpu.draw_sprite(mem.vn[x], mem.vn[y], c)
    pc += 2
  elif oc == 0xE and y == 0x9 and c == 0xE: # Skips the next instruction if the key stored in VX is pressed.
    pc = pc + 4 if input.is_key_pressed(mem.vn[x]) else pc + 2
  elif oc == 0xE and y == 0xA and c == 0x1: # Skips the next instruction if the key stored in VX isn't pressed.
    pc = pc + 4 if not input.is_key_pressed(mem.vn[x]) else pc + 2
  elif oc == 0xF and y == 0x0 and c == 0x7: # Sets VX to the value of the delay timer.
    mem.vn[x] = timer_delay
    pc += 2
  elif oc == 0xF and y == 0x0 and c == 0xA: # A key press is awaited, and then stored in VX. (Blocking Operation.)
    if 1 not in input.input_status: return

    for i in range(16):
      if input.input_status[i] == 1:
        mem.vn[x] = i

    pc += 2 
  elif oc == 0xF and y == 0x1 and c == 0x5: # Sets the delay timer to VX.
    timer_delay = mem.vn[x]
    pc += 2
  elif oc == 0xF and y == 0x1 and c == 0x8: # Sets the sound timer to VX.
    timer_sound = mem.vn[x]
    pc += 2
  elif oc == 0xF and y == 0x1 and c == 0xE: # Adds VX to I. VF is set to 1 when there is a range overflow 0 otherwise.
    mem.vn[0xF] = 1 if I + mem.vn[x] > 0xFFF else 0
    I += mem.vn[x] 
    pc += 2
  elif oc == 0xF and y == 0x2 and c == 0x9: # Sets I to the location of the sprite for the character in VX.
    I = mem.vn[x] * 0x5
    pc += 2
  elif oc == 0xF and y == 0x3 and c == 0x0: assert False
  elif oc == 0xF and y == 0x3 and c == 0x3: # Stores the binary-coded decimal representation of VX.
    mem.memory[I]     = int (mem.vn[x] / 100)        & 0xFF
    mem.memory[I + 1] = int ((mem.vn[x] / 10) % 10)  & 0xFF
    mem.memory[I + 2] = int ((mem.vn[x] % 100) % 10) & 0xFF
    pc += 2
  elif oc == 0xF and y == 0x5 and c == 0x5: # Stores V0 to VX (including VX) in memory starting at address I.
    for j in range(x + 1):
      mem.memory[I + j] = mem.vn[j]
    pc += 2 
  elif oc == 0xF and y == 0x6 and c == 0x5: # Fills V0 to VX (including VX) with values from memory starting at address I.
    for j in range(x + 1):
      mem.vn[j] = mem.memory[I + j]
    pc += 2
  elif oc == 0xF and y == 0x7 and c == 0x5: assert False
  elif oc == 0xF and y == 0x8 and c == 0x5: assert False
  else:
    print("The opcode:", hex(opcode), "is not implemented.")
    raise False
