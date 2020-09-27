import pygame

pygame.init()
pygame.joystick.init()
j = pygame.joystick.Joystick(0)
j.init()

def event():
    a = pygame.event.get()
    print(j.get_axis(0))

while True:
    event()
