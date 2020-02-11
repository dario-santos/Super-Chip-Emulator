# CHIP8-Emulator
![CHIP8 logo](https://lh3.googleusercontent.com/proxy/qjht3M2ykiJgaJs6pOteCleRm5t-blsgDTb21ugkm8d1cpQMh_17Wbswum3PYbQPqaeSpa3SwDHCtCeE04jzC77i5QHiJKZUJG_SR5Fk7Q)

This is a Chip8 emulator done with Python 3.6 and Pygame.
This project is divided in several modules for a better organization.

## CPU
The CPU module as the variables

PC     : Program Counter - The current address memory
I      : The address register
Opcode : The opcode that will be executed by the CPU

Delay timer: This timer is intended to be used for timing the events of games
Sound timer: This timer is used for sound effects

The CPU as the methods

Cycle:  Reponsible to do emulate a single cpu cycle
Decode: Executes the requested opcode
