from math import trunc
import pygame
import sys
import os
from random import randint
from time import sleep

#initialize
os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (0,0)
successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))
screenWidth = 1920
ScreenHeight = 1080
pygame.display.set_caption("Kicker")
screen = pygame.display.set_mode((screenWidth, ScreenHeight))
exitProcess = False
over = False
font = pygame.font.SysFont('freesans', 30)
font2 = pygame.font.SysFont('freesans', 150)

#FPS settings
clock = pygame.time.Clock()
FPS = 60

#var
chracsize = 48
kickcount = 5
hitBox = 20
knockBackRatio = 20

#main init
mainlook = True
mainkick = False
mainkickstart = 0
mainstat = 'stable'
mainchracpos = (screenWidth/2 - chracsize/2, ScreenHeight/2 - chracsize/2)
mainSPDRatio = 20
life = 10
hit = 0

#enemy init
enemyList = [[[randint(0, screenWidth - chracsize), randint(0, ScreenHeight - chracsize)], 'stable', True, 0]]
spawnDelay = 30
lastSpawn = 0
maxEnemy = 5
enemySPDRatio = 80
warigari = 6

#Colors
Black = (0, 0, 0)
White = (255, 255, 255)


main = [pygame.image.load('chrac\mainStableR.png'),
pygame.image.load('chrac\mainStableL.png'),
pygame.image.load('chrac\mainKick1R.png'),
pygame.image.load('chrac\mainKick1L.png'),
pygame.image.load('chrac\mainKick2R.png'),
pygame.image.load('chrac\mainKick2L.png'),
pygame.image.load('chrac\mainHitR.png'),
pygame.image.load('chrac\mainHitL.png')]

enemy = [pygame.image.load('chrac\enemyStableR.png'),
pygame.image.load('chrac\enemyStableL.png'),
pygame.image.load('chrac\enemyKick1R.png'),
pygame.image.load('chrac\enemyKick1L.png'),
pygame.image.load('chrac\enemyKick2R.png'),
pygame.image.load('chrac\enemyKick2L.png'),
pygame.image.load('chrac\enemyHitR.png'),
pygame.image.load('chrac\enemyHitL.png')]

def enemyDetLR(xVal):
    if mainchracpos[0] - xVal > 1: return True
    if mainchracpos[0] - xVal < -1: return False


def spawnEnemy():
    x, y = randint(0, screenWidth - chracsize), randint(0, ScreenHeight - chracsize)
    enemyList.append([[x,y], 'stable', enemyDetLR(x), frame])

def drawMain(mainlook, stat):
    if stat == 'stable':
        if mainlook: screen.blit(main[0], mainchracpos)
        else: screen.blit(main[1], mainchracpos)
    elif stat == 'kick1':
        if mainlook: screen.blit(main[2], mainchracpos)
        else: screen.blit(main[3], mainchracpos)
    elif stat == 'kick2':
        if mainlook: screen.blit(main[4], mainchracpos)
        else: screen.blit(main[5], mainchracpos)
    elif stat == 'hit':
        if mainlook: screen.blit(main[6], mainchracpos)
        else: screen.blit(main[7], mainchracpos)

def drawEnemy(enemypos, enemystat, enemylook):
    if enemystat == 'stable':
        if enemylook: screen.blit(enemy[0], enemypos)
        else: screen.blit(enemy[1], enemypos)
    elif enemystat == 'kick1':
        if enemylook: screen.blit(enemy[2], enemypos)
        else: screen.blit(enemy[3], enemypos)
    elif enemystat == 'kick2':
        if enemylook: screen.blit(enemy[4], enemypos)
        else: screen.blit(enemy[5], enemypos)
    elif enemystat == 'hit':
        if enemylook: screen.blit(enemy[6], enemypos)
        else: screen.blit(enemy[7], enemypos)

frame = 0

while not exitProcess:
    screen.fill((150, 150, 150))
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONUP:
            mainkick = True
        if event.type == pygame.KEYUP:
            if event.key == ord('q'):
                exitProcess = True

    mouseCrnt = pygame.mouse.get_pos()
    mainXSPD, mainYSPD = (mouseCrnt[0] - mainchracpos[0])/mainSPDRatio, (mouseCrnt[1] - mainchracpos[1])/mainSPDRatio
    mainchracpos = (mainchracpos[0] + mainXSPD - chracsize/mainSPDRatio, mainchracpos[1] + mainYSPD - chracsize/mainSPDRatio)
    
    #main cal
    if mainkick == False:
        mainkickstart = frame
        mainstat = 'stable'

    if mainkick == True and frame - mainkickstart > kickcount *3 :
        mainkick = False

    if mainXSPD > 1:
        mainlook = True
    if mainXSPD < -1:
        mainlook = False
    
    if mainkick:
        if frame - mainkickstart < kickcount or frame - mainkickstart > kickcount * 2: mainstat = 'kick1'
        elif frame - mainkickstart >= kickcount: mainstat = 'kick2'
    
    #enemyspawn
    if len(enemyList) < maxEnemy and frame - lastSpawn >= spawnDelay:
        lastSpawn = frame
        spawnEnemy()
    
    #enemyMove:
    for ene in enemyList:
        eneXdif, eneydif = mainchracpos[0] - ene[0][0], mainchracpos[1] - ene[0][1]
        eneXspd, eneYspd = eneXdif/enemySPDRatio, eneydif/enemySPDRatio
        

        if abs(eneXdif) <= hitBox and abs(eneydif) <= hitBox and frame - ene[3] > kickcount * 10:
            ene[3] = frame
        
        if ene[1] != 'hit':
            ene[0][0] += eneXspd + randint(-1*warigari, warigari)
            ene[0][1] += eneYspd + randint(-1*warigari, warigari)

            if frame - ene[3] < kickcount or frame - ene[3] > kickcount * 2: ene[1] = 'kick1'
            elif frame - ene[3] > kickcount: ene[1] = 'kick2'
            if frame - ene[3] > kickcount * 3: ene[1] = 'stable'

            drawEnemy(ene[0], ene[1], enemyDetLR(ene[0][0]))

        if mainstat and abs(eneXdif) <= hitBox and abs(eneydif) <= hitBox:
            if mainstat == 'kick2':
                ene[1] = 'hit'
            elif ene[1] == 'kick2':
                mainstat = 'hit'

        if ene[1] == 'hit':
            ene[0][0] += eneXspd * -2
            ene[0][1] += eneYspd * -2
            drawEnemy(ene[0], ene[1], ene[2])
            if abs(eneXdif) >= screenWidth/ 1.5 and abs(eneydif) >= ScreenHeight / 1.5:
                enemyList.pop(enemyList.index(ene))
                hit += 1

    #graphics
    drawMain(mainlook, mainstat)
    lifetxt = "LIFE: " + str(life)
    killtxt = "KILL: " + str(hit)
    text1 = font.render(lifetxt,True,(28,0,0))  #텍스트가 표시된 Surface 를 만듬
    text2 = font.render(killtxt,True,(28,0,0))  #텍스트가 표시된 Surface 를 만듬
    screen.blit(text1, (0,0))
    screen.blit(text2, (0,30))
    pygame.display.update()

    if mainstat == 'hit':
        life -= 1
        sleep(0.5)
        if life == 0:
            sleep(1)
            break

    frame += 1

while not over:
    screen.fill((0,0,0))
    screen.blit(font2.render('GAME OVER',True,(255,255,255)), (200,ScreenHeight/2-200))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYUP:
            if event.key == ord('q'):
                over = True

sys.exit(0)