import pygame
import sys
import os
from math import sin, cos, radians
from random import randint

#initialize
os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (20,20)
successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))

#screen settings
screenWidth = 800
ScreenHeight = 800
pygame.display.set_caption("Particular Movement")
screen = pygame.display.set_mode((screenWidth, ScreenHeight))

#FPS settings
clock = pygame.time.Clock()
FPS = 60

#Colors
Black = (0, 0, 0)
White = (255, 255, 255)

n = 5
r = 6 
v0 = 10
g = 9.8
particles = []
frame = 0

def collisionCheck(newXpos, newYpos):
    if newXpos >= screenWidth- r or newXpos <= r or newYpos >= ScreenHeight-r or newYpos <= r:
        return True

    for particle in particles:
        check1 = particle[0] + r >= newXpos - r and particle[0] <= newXpos and particle[1] + r >= newYpos - r and particle[1] <= newYpos
        check2 = particle[0] - r <= newXpos + r and particle[0] >= newXpos and particle[1] - r <= newYpos + r and particle[1] >= newYpos 
        if check1 or check2:
            particle[5] *= -1
            return True
    
    return False
    


def particlePosRenewal():
    for i in range(len(particles)):
        newXpos = particles[i][0] + particles[i][5] * cos(radians(particles[i][2]))
        newYpos = particles[i][1] + particles[i][5] * sin(radians(particles[i][2]))
        
        if collisionCheck(newXpos, newYpos):
            particles[i][5] *= -1
            particles[i][0] = particles[i][0] + particles[i][5] * cos(radians(particles[i][2])) *2
            particles[i][1] = particles[i][1] + particles[i][5] * sin(radians(particles[i][2])) *2
        
        else: particles[i][0], particles[i][1] = newXpos, newYpos

def particleCreate(initialPos, t):
    col = (randint(0,200), randint(0,200), randint(0,200))
    for i in range(n):        
        particles.append([initialPos[0]+cos(radians(360/n*i)), initialPos[1]+sin(radians(360/n*i)), 360/n*i, t, col, v0])


while True:
    screen.fill(White)

    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            particleCreate(pygame.mouse.get_pos(), frame)

        if event.type == pygame.QUIT:
            sys.exit(0)

            
    particlePosRenewal()
    
    #graphics
    for i in range(len(particles)):
        pygame.draw.circle(screen, particles[i][4], (particles[i][0], particles[i][1]), r, 0)
    pygame.display.update()
    frame += 1
