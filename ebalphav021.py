# Endless Breakout

DEBUGMODE = False
import pygame, random, sys
from pygame.locals import *

pygame.init()
FPS = 62.5
FPSCLOCK = pygame.time.Clock()
defaultFontSize = 40
fontMargin = 25
fontSlot = 0
fontValuesPositionX = fontMargin * 8
highscore = 0 # In the future I will program the game to write the player's highscore to a save file.

# Window, playfield and stats surfaces
WINDOWWIDTH = 960
WINDOWHEIGHT = 600
PLAYFIELDSIZE = 600
window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Endless Breakout')
pygame.mouse.set_visible(False)
# set_grab prevents the mouse from leaving the window.
# This makes the paddle easier to control along the edges of the screen.
pygame.event.set_grab(True)
playfield = pygame.Surface((PLAYFIELDSIZE, PLAYFIELDSIZE))
playfieldTopLeftCorner = (0, 0)
statsSurfaceTopLeftCorner = (PLAYFIELDSIZE, 0)
statsSurface = pygame.Surface((WINDOWWIDTH-PLAYFIELDSIZE, WINDOWHEIGHT))
statsSurfaceRect = statsSurface.get_rect()
statsSurfaceRect.topleft = statsSurfaceTopLeftCorner

# Colors   R    G    B
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
GREY  = (128, 128, 128)
colorList = (WHITE, BLACK, RED, GREEN, BLUE)
color = 0

# Ball and paddle variables
PADWIDTH = 150
PADHEIGHT = 20
BALLSIZE = 20
baseSpeed = 8
speedMultiplier = 1
spawnInterval = 10 # Interval for spawning new balls, in seconds
spawnVariation = 75
DOWNLEFT = 1
DOWNRIGHT = 3
UPLEFT = 7
UPRIGHT = 9

# Functions
def terminate():
    pygame.quit()
    sys.exit()

def waitForInput(): # Pauses game
    # When the game is paused, make the mouse visible
    # and allow it to leave the screen.
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)
    playerInput = False
    pressedButton = False
    while not playerInput:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONDOWN:
                pressedButton = True
            if event.type == MOUSEBUTTONUP:
                if pressedButton:
                    playerInput = True
            if event.type == KEYDOWN:
                pressedButton = True
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                else:
                    if pressedButton:
                        playerInput = True
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    pygame.mouse.set_pos(paddle.centerx, paddle.centery)
    return paddle.centerx, paddle.centery

def drawText(text, surface, x, y, color, size=defaultFontSize):
    font = pygame.font.SysFont(None, size)
    textObj = font.render(text, 1, color)
    textRect = textObj.get_rect()
    textRect.topleft = (x, y)
    surface.blit(textObj, textRect)

def displayElapsedTime(ElapsedTime):
    totalSeconds = int(ElapsedTime // 1000)
    totalMinutes = totalSeconds // 60
    if int(ElapsedTime % 1000 < 10):
        displayMilliseconds = '00'+str(int(ElapsedTime % 1000))
    elif int(ElapsedTime % 1000 < 100):
        displayMilliseconds = '0'+str(int(ElapsedTime % 1000))
    else:
        displayMilliseconds = str(int(ElapsedTime % 1000))
    if totalSeconds % 60 < 10:
        displaySeconds = '0'+str(totalSeconds % 60)
    else:
        displaySeconds = str(totalSeconds % 60)
    displayMinutes = str(totalMinutes)
    return displayMinutes+':'+displaySeconds+'.'+displayMilliseconds
    

# Set up the start of the game
while True:
    paddle = pygame.Rect(PLAYFIELDSIZE/2-PADWIDTH/2, PLAYFIELDSIZE-PADHEIGHT, PADWIDTH, PADHEIGHT)
    pygame.mouse.set_pos(paddle.centerx, paddle.centery)
    newballs = []
    balls = []
    spawnframe = 0
    gameOver = False
    frame = 0
    score = 0
    ElapsedTime = 0
    speedBall = False
    slowBall = False
    energy = 100
    godMode = False
    statsSurface.fill(GREEN)
    fontSlot = 0
    drawText('Highscore:', statsSurface, fontMargin, defaultFontSize * fontSlot + fontMargin, BLACK)
    drawText(str(highscore), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
    fontSlot = 1
    drawText('Score:', statsSurface, fontMargin, defaultFontSize * fontSlot + fontMargin, BLACK)
    drawText(str(score), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
    fontSlot = 2
    drawText('Time:', statsSurface, fontMargin, defaultFontSize * fontSlot + fontMargin, BLACK)
    drawText(str(len(balls)+len(newballs)), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
    fontSlot = 3
    drawText('Balls:', statsSurface, fontMargin, defaultFontSize * fontSlot + fontMargin, BLACK)
    drawText(str(frame), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
    fontSlot = 4
    drawText('Energy:', statsSurface, fontMargin, defaultFontSize * fontSlot + fontMargin, BLACK)
    drawText(str(int(energy)), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
    if DEBUGMODE:
        fontSlot = 5
        drawText('FPS:', statsSurface, fontMargin, defaultFontSize * fontSlot + fontMargin, BLACK)
        drawText(str(FPSCLOCK.get_fps()), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
        fontSlot = 6
        drawText('Frame:', statsSurface, fontMargin, defaultFontSize * fontSlot + fontMargin, BLACK)
        drawText(str(frame), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
        fontSlot = 7
        drawText('godMode:', statsSurface, fontMargin, defaultFontSize * fontSlot + fontMargin, BLACK)
        drawText(str(godMode), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
        
    # Main game loop
    while gameOver == False:
        
        # Events
        ballsUpdated = False
        godModeUpdated = False
        energyUpdated = False
        gameWasPaused = False
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                if event.key == K_ESCAPE or event.key == ord('p'):
                    mousex, mousey = waitForInput()
                    gameWasPaused = True
                if DEBUGMODE:
                    if event.key == ord('g'):
                        godMode = not godMode
                        godModeUpdated = True
                        score = 0
                    if event.key == ord('b'): # Spawn one ball
                        balls.append({'rect':pygame.Rect(PLAYFIELDSIZE/2-BALLSIZE/2, PLAYFIELDSIZE/2-BALLSIZE/2, BALLSIZE, BALLSIZE),
                        'speed':baseSpeed * speedMultiplier, 'direction':DOWNRIGHT, 'xangle':45, 'yangle':45})
                        # 'xangle', 'yangle' and 'speed' currently don't do anything, but I've left them in
                        # in case I want to do something with them in the future.
                        ballsUpdated = True
                    if event.key == ord('x'): # Spawn 100 balls in random locations
                        for i in range(0, 100):
                            balls.append({'rect':pygame.Rect(random.randint(BALLSIZE, PLAYFIELDSIZE-BALLSIZE),
                            random.randint(BALLSIZE, PLAYFIELDSIZE-BALLSIZE), BALLSIZE, BALLSIZE),
                            'speed':baseSpeed * speedMultiplier, 'direction':DOWNRIGHT, 'xangle':45, 'yangle':45})
                        ballsUpdated = True
            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    speedBall = True
                    slowBall = False
                if event.button == 3:
                    slowBall = True
                    speedBall = False
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    speedBall = False
                if event.button == 3:
                    slowBall = False
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos[0], event.pos[1]
        if gameWasPaused:
            speedBall = False
            slowBall = False

        # Game state
        paddle.centerx, paddle.centery = mousex, mousey
        # Spawn a new ball every spawnInterval seconds
        if frame % (FPS * spawnInterval) == 0:
                newballs.append({'rect':pygame.Rect(random.randint(PLAYFIELDSIZE/2-BALLSIZE/2-spawnVariation, PLAYFIELDSIZE/2-BALLSIZE/2+spawnVariation),
                random.randint(PLAYFIELDSIZE/2-BALLSIZE/2-spawnVariation, PLAYFIELDSIZE/2-BALLSIZE/2+spawnVariation), BALLSIZE, BALLSIZE),
                'speed':baseSpeed * speedMultiplier, 'direction':random.choice([DOWNLEFT, DOWNRIGHT]), 'xangle':45, 'yangle':45})
                spawnframe = frame
                ballsUpdated = True
        if len(newballs) != 0 and frame - spawnframe >= 60:
            balls.append(newballs[0])
            del newballs[0]
        
        # Update the state of existing balls.
        if energy <= 0 or speedBall:
            slowBall = False
        if slowBall:
            speedMultiplier = 0.5
            energy -= 0.5
            energyUpdated = True
        else:
            if energy < 100:
                energy += 0.25
                energyUpdated = True
            if speedBall:
                speedMultiplier = 2
            else:
                speedMultiplier = 1

        collisionsResolved = False
        pixelsLeft = baseSpeed * speedMultiplier
        while collisionsResolved == False:
            for ball in balls:
                # Move each ball 1 pixel at a time for more accurate collisions.
                if ball['direction'] == DOWNLEFT:
                    ball['rect'].left -= 1
                    ball['rect'].top += 1
                if ball['direction'] == DOWNRIGHT:
                    ball['rect'].left += 1
                    ball['rect'].top += 1
                if ball['direction'] == UPLEFT:
                    ball['rect'].left -= 1
                    ball['rect'].top -= 1
                if ball['direction'] == UPRIGHT:
                    ball['rect'].left += 1
                    ball['rect'].top -= 1

                # Check for collisions
                if ball['rect'].top < 0:
                    if ball['direction'] == UPLEFT:
                        ball['direction'] = DOWNLEFT
                    if ball['direction'] == UPRIGHT:
                        ball['direction'] = DOWNRIGHT
                if ball['rect'].left < 0:
                    if ball['direction'] == UPLEFT:
                        ball['direction'] = UPRIGHT
                    if ball['direction'] == DOWNLEFT:
                        ball['direction'] = DOWNRIGHT
                if ball['rect'].right > PLAYFIELDSIZE:
                    if ball['direction'] == UPRIGHT:
                        ball['direction'] = UPLEFT
                    if ball['direction'] == DOWNRIGHT:
                        ball['direction'] = DOWNLEFT
                if ball['rect'].colliderect(paddle):
                    if ball['direction'] == DOWNLEFT:
                        ball['direction'] = UPLEFT
##                    elif ball['direction'] == UPLEFT:
##                        ball['direction'] = DOWNLEFT
                    if ball['direction'] == DOWNRIGHT:
                        ball['direction'] = UPRIGHT
##                    elif ball['direction'] == UPRIGHT:
##                        ball['direction'] = DOWNRIGHT
                if ball['rect'].bottom > PLAYFIELDSIZE+BALLSIZE:
                    if godMode:
                        if ball['direction'] == DOWNLEFT:
                            ball['direction'] = UPLEFT
                        if ball['direction'] == DOWNRIGHT:
                            ball['direction'] = UPRIGHT
                    else:
                        for ball in balls:
                            del ball
                        collisionsResolved = True
                        gameOver = True
            pixelsLeft -= 1
            if pixelsLeft <= 0:
                collisionsResolved = True
                
        # playfield drawing
        playfield.fill(WHITE)
        fontSlot = 1
        statsSurface.fill(GREEN, pygame.Rect(fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, WINDOWWIDTH-PLAYFIELDSIZE, defaultFontSize * 2))
        pygame.draw.rect(playfield, GREY, paddle)
        for ball in balls:
            pygame.draw.rect(playfield, RED, ball['rect'])
        for ball in newballs:
            pygame.draw.rect(playfield, RED, ball['rect'])
        window.blit(playfield, playfieldTopLeftCorner)
        
        # statsSurface drawing
        fontSlot = 1
        drawText(str(score), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
        fontSlot = 2
        ElapsedTime = float(frame) / FPS * 1000
        drawText(displayElapsedTime(ElapsedTime), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
        if ballsUpdated:
            fontSlot = 3
            statsSurface.fill(GREEN, pygame.Rect(fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, WINDOWWIDTH-PLAYFIELDSIZE, defaultFontSize))
            drawText(str(len(balls)+len(newballs)), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
        if energyUpdated:
            fontSlot = 4
            statsSurface.fill(GREEN, pygame.Rect(fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, WINDOWWIDTH-PLAYFIELDSIZE, defaultFontSize))
            drawText(str(int(energy)), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
        if DEBUGMODE:
            fontSlot = 5
            statsSurface.fill(GREEN, pygame.Rect(fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, WINDOWWIDTH-PLAYFIELDSIZE, defaultFontSize * 2))
            drawText(str(FPSCLOCK.get_fps()), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
            fontSlot = 6
            drawText(str(frame), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
            if godModeUpdated:
                fontSlot = 7
                statsSurface.fill(GREEN, pygame.Rect(fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, WINDOWWIDTH-PLAYFIELDSIZE, defaultFontSize))
                drawText(str(godMode), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
        window.blit(statsSurface, statsSurfaceTopLeftCorner)
        
        # Update screen
        pygame.display.update()
        FPSCLOCK.tick(FPS)

        # Check for game over
        if gameOver:
            if score > highscore:
                highscore = score
                fontSlot = 0
                drawText('New highscore!', playfield, PLAYFIELDSIZE / 2 - 96 * 2.5, PLAYFIELDSIZE / 2 - 72 / 2, BLACK, 96)
                window.blit(statsSurface, statsSurfaceTopLeftCorner)
            else:
                playfield.fill(RED)
                drawText('Game over!', playfield, PLAYFIELDSIZE / 2 - 96 * 2, PLAYFIELDSIZE / 2 - 72 / 2, BLACK, 96)
            window.blit(playfield, playfieldTopLeftCorner)
            pygame.display.update()
            mousex, mousey = waitForInput()
        else:
            frame += 1
            if frame >= 60:
                if not godMode:
                    if speedBall:
                        score += 2
                    else:
                        score += 1

