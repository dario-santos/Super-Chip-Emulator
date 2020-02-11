import pygame

sound_beep = None

def initialize():
    global sound_beep
    sound_beep = pygame.mixer.Sound("beep.ogg")

def play():
    global sound_beep

    pygame.mixer.Sound.play(sound_beep)
    
    pygame.mixer.music.stop()
