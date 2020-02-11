import memory as mem
import input as inp
import cpu
import gpu
import sound

skip = 0

def debug():
  global skip
  print_key_status()
  print_cpu_info()
  print_memory_debug()

  while True:
    i = input('Press c to do 1 step, z to do 1000: ')
    if i is 'c':
      break
    if i is 'z':
      skip = 1000
      break



def print_key_status():
  st = '+---+---+---+---+\n'
  color = '\033[95m' if inp.input_status[1] == 1 else '\033[94m'
  st += color + '| 1 |'
  color = '\033[95m' if inp.input_status[2] == 1 else '\033[94m'
  st += color + ' 2 |'
  color = '\033[95m' if inp.input_status[3] == 1 else '\033[94m'
  st += color + ' 3 |'
  color = '\033[95m' if inp.input_status[12] == 1 else '\033[94m'
  st += color + ' 4 |\n'

  st += '\033[94m' + '+---+---+---+---+\n'
  color = '\033[95m' if inp.input_status[4] == 1 else '\033[94m'
  st += color + '| Q |'
  color = '\033[95m' if inp.input_status[5] == 1 else '\033[94m'
  st += color + ' W |'
  color = '\033[95m' if inp.input_status[6] == 1 else '\033[94m'
  st += color + ' E |'
  color = '\033[95m' if inp.input_status[13] == 1 else '\033[94m'
  st += color + ' R |\n'

  st += '\033[94m' + '+---+---+---+---+\n'
  color = '\033[95m' if inp.input_status[7] == 1 else '\033[94m'
  st += color + '| A |'
  color = '\033[95m' if inp.input_status[8] == 1 else '\033[94m'
  st += color + ' S |'
  color = '\033[95m' if inp.input_status[9] == 1 else '\033[94m'
  st += color + ' D |'
  color = '\033[95m' if inp.input_status[14] == 1 else '\033[94m'
  st += color + ' F |\n'

  st += '\033[94m' + '+---+---+---+---+\n'
  color = '\033[95m' if inp.input_status[10] == 1 else '\033[94m'
  st += color + '| Z |'
  color = '\033[95m' if inp.input_status[0] == 1 else '\033[94m'
  st += color + ' X |'
  color = '\033[95m' if inp.input_status[11] == 1 else '\033[94m'
  st += color + ' C |'
  color = '\033[95m' if inp.input_status[15] == 1 else '\033[94m'
  st += color + ' V |\n'
  st += '\033[94m' + '+---+---+---+---+\n'

  print(st)

def print_cpu_info():
  print('\033[92mI      : ', hex(cpu.I))
  print('PC     : ', hex(cpu.pc))
  print('OPCODE : ', hex(cpu.opcode))


def print_memory_debug():
  st = '\033[92m' + 'VN     :  '
  for v in mem.vn:
    st += str(v) + ", "
  print(st)


  sts = 'Stack: ' + str(mem.stack)
  print(sts)


  sts = 'Memory: ' + str(mem.memory)
  ##print(sts)