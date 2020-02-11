import pygame

beep = None

def initialize():
    global beep
    beep = pygame.mixer.Sound("beep.ogg")

def play():
    global beep

    pygame.mixer.Sound.play(beep)
    
    pygame.mixer.music.stop()
