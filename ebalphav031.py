# Endless Breakout

DEBUGMODE = False
import pygame, random, sys
from pygame.locals import *

print('Initializing pygame')
pygame.init()
FPS = 62.5
FPSCLOCK = pygame.time.Clock()
defaultFontSize = 40 # Anything other than 40 is for debugging
fontMargin = 25
fontSlot = 0
fontValuesPositionX = fontMargin * 8
highscore = 0 # In the future I will program the game to write the player's highscore to a save file.

# Window, playfield and stats surfaces
WINDOWWIDTH = 960 # Anything other than 960 is for debugging
WINDOWHEIGHT = 600
PLAYFIELDSIZE = 600
window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Endless Breakout')
pygame.mouse.set_visible(False)
# set_grab prevents the mouse from leaving the window.
# This makes the paddle easier to control along the edges of the playfield.
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
PADWIDTH = 150.0
PADHEIGHT = 15.0
BALLSIZE = 18
baseSpeed = 7.0
speedMultiplier = 1.0
dimensions = 2
spawnInterval = 10 # Interval for spawning new balls, in seconds
spawnVariation = 20
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
    # and allow it to leave the game window.
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)
    playerInput = False
    pressedButton = False
    altpressed = False
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
                if event.key == K_LALT or event.key == K_RALT:
                    altpressed = True
                if altpressed and event.key == K_F4:
                    terminate()
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
    if color != BLACK or size != defaultFontSize:
        font = pygame.font.SysFont(None, size)
        textObj = font.render(text, 1, color)
        textRect = textObj.get_rect()
        textRect.topleft = (x, y)
        if surface != None:
            surface.blit(textObj, textRect)
##    elif text in PreRenderedText: # In case I want to prerender some commonly used words, so the
##        # function doesn't have to fetch prerendered letters one at a time.
##        PreRenderedText[text]['rect'].topleft = (x, y)
##        if surface != None:
##            surface.blit(PreRenderedText[text]['obj'], PreRenderedText[text]['rect'])
##        else: # If the program works as intended, this condition should never happen
##            print('Warning: None was passed to a drawText call for text that was already prerendered')
##            print('Program is trying to prerender the same text more than once')
    else:
        for char in text:
            if char in PreRenderedText:
                PreRenderedText[char]['rect'].topleft = (x, y)
                if surface != None:
                    surface.blit(PreRenderedText[char]['obj'], PreRenderedText[char]['rect'])
            else:
                font = pygame.font.SysFont(None, size)
                textObj = font.render(char, 1, color)
                textRect = textObj.get_rect()
                textRect.topleft = (x, y)
                PreRenderedText[char] = {'rect':textRect, 'obj':textObj}
                if surface != None:
                    surface.blit(textObj, textRect)
            x += PreRenderedText[char]['rect'].width

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

# Prerender text because calling .render on every frame is slow
print('Prerendering text')
PreRenderedText = {}
drawText('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz 0123456789:', None, 0, 0, BLACK)

# Set up the start of the game
print('Launching Endless Breakout')
while True:
    paddle = pygame.Rect(PLAYFIELDSIZE/2-PADWIDTH/2, PLAYFIELDSIZE-PADHEIGHT, PADWIDTH, PADHEIGHT)
    pygame.mouse.set_pos(paddle.centerx, paddle.centery)
##    newballs = []
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
    drawText(str(len(balls)), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
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
        fontSlot = 8
        drawText('ms/frame:', statsSurface, fontMargin, defaultFontSize * fontSlot + fontMargin, BLACK)
        drawText(str(FPSCLOCK.get_time()), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
        fontSlot = 9
        drawText('ftime 1:', statsSurface, fontMargin, defaultFontSize * fontSlot + fontMargin, BLACK)
        drawText(str(pygame.time.get_ticks()), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
        fontSlot = 10
        drawText('ftime 2:', statsSurface, fontMargin, defaultFontSize * fontSlot + fontMargin, BLACK)
        drawText(str(pygame.time.get_ticks()), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
        fontSlot = 11
        drawText('ftime 3:', statsSurface, fontMargin, defaultFontSize * fontSlot + fontMargin, BLACK)
        drawText(str(pygame.time.get_ticks()), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
        fontSlot = 12
        drawText('total raw:', statsSurface, fontMargin, defaultFontSize * fontSlot + fontMargin, BLACK)
        drawText(str(FPSCLOCK.get_rawtime()), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
        fontSlot = 13
        drawText('ball 0 angle:', statsSurface, fontMargin, defaultFontSize * fontSlot + fontMargin, BLACK)
        drawText('-', statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)

    laltpressed = False
    raltpressed = False
        
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
            if event.type == KEYDOWN:
                if event.key == K_LALT:
                    laltpressed = True
                if event.key == K_RALT:
                    raltpressed = True
                if (laltpressed or raltpressed) and event.key == K_F4:
                    terminate()
            if event.type == KEYUP:
                if event.key == K_LALT:
                    laltpressed = False
                if event.key == K_RALT:
                    raltpressed = False
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
                        'localspeed':1.0, 'direction':DOWNRIGHT, 'angle':45.0, 'Xdecimal':0, 'Ydecimal':0, 'freshlyspawned':False})
                        # 'angle' ranges from 0-90. 0 is sideways, 90 is vertical
                        # Ball should move 'angle' pixels vertically for every 90 - 'angle' pixels horizontally
                        # Eg: With 'angle' == 80 and 'direction' == UPRIGHT, ball moves 80 pixels up and 10 pixels right
                        # 'localspeed' is a local multiplier of the global speed for individual balls
                        # Rect.top and rect.left use integers. For greater precision, decimal places are stored in Xdecimal
                        # and Ydecimal.
                        ballsUpdated = True
                    if event.key == ord('x'): # Spawn 100 balls in random locations
                        for i in range(0, 100):
                            balls.append({'rect':pygame.Rect(random.randint(BALLSIZE, PLAYFIELDSIZE-BALLSIZE),
                            random.randint(BALLSIZE, PLAYFIELDSIZE-BALLSIZE), BALLSIZE, BALLSIZE),
                            'localspeed':1.0, 'direction':DOWNRIGHT, 'angle':45.0, 'Xdecimal':0, 'Ydecimal':0, 'freshlyspawned':False})
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
                balls.append({'rect':pygame.Rect(random.randint(PLAYFIELDSIZE/2-BALLSIZE/2-spawnVariation, PLAYFIELDSIZE/2-BALLSIZE/2+spawnVariation),
                random.randint(PLAYFIELDSIZE/2-BALLSIZE/2-spawnVariation, PLAYFIELDSIZE/2-BALLSIZE/2+spawnVariation), BALLSIZE, BALLSIZE),
                'localspeed':0.0, 'direction':random.choice([DOWNLEFT, DOWNRIGHT]), 'angle':float(random.randint(20, 70)), 'Xdecimal':0, 'Ydecimal':0, 'freshlyspawned':True})
                spawnframe = frame
                ballsUpdated = True
        
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
                speedMultiplier = 2.0
            else:
                speedMultiplier = 1.0

        # frametime check 1
        if DEBUGMODE:
            fontSlot = 9
            statsSurface.fill(GREEN, pygame.Rect(fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, WINDOWWIDTH-PLAYFIELDSIZE, defaultFontSize))
            drawText(str(pygame.time.get_ticks()), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)

        # Ball movement
        collisionsResolved = False
        globalSpeed = baseSpeed * speedMultiplier * dimensions
        # Ball movement is done over multiple iterations per frame for more accurate collisions.
        iterations = 8
        iterationsLeft = iterations
        while collisionsResolved == False:
            for ball in balls:
                
                Yangle = ball['angle']
                Xangle = 90 - ball['angle']

                # From what I can tell, if you assign a float value to a rect position attribute (eg: .top),
                # pygame will round it to the nearest integer.
                # I want floats for more precise angles, so as a workaround, I store the decimal places
                # separately.
                
                Xmovement = ball['localspeed'] * ((Xangle/float(90)) * float(globalSpeed) / float(iterations))
                Ymovement = ball['localspeed'] * ((Yangle/float(90)) * float(globalSpeed) / float(iterations))
                ball['Xdecimal'] += Xmovement - int(Xmovement)
                ball['Ydecimal'] += Ymovement - int(Ymovement)
                if ball['Xdecimal'] >= 1:
                    ball['Xdecimal'] -= 1
                    Xmovement += 1
                if ball['Ydecimal'] >= 1:
                    ball['Ydecimal'] -= 1
                    Ymovement += 1

                # int(movement) is used here to ensure that the values are always rounded down.
                # If I don't do this, the physics glitch out, especially at a higher iterations
                # value.
                if ball['direction'] == DOWNLEFT:
                    ball['rect'].left -= int(Xmovement)
                    ball['rect'].top += int(Ymovement)
                if ball['direction'] == DOWNRIGHT:
                    ball['rect'].left += int(Xmovement)
                    ball['rect'].top += int(Ymovement)
                if ball['direction'] == UPLEFT:
                    ball['rect'].left -= int(Xmovement)
                    ball['rect'].top -= int(Ymovement)
                if ball['direction'] == UPRIGHT:
                    ball['rect'].left += int(Xmovement)
                    ball['rect'].top -= int(Ymovement)

                # If a ball is freshly spawned, gradually accelerate it to full speed
                # after a second has passed
                if iterationsLeft == iterations:
                    if ball['freshlyspawned'] == True and frame - spawnframe >= FPS:
                        ball['localspeed'] += 0.02
                        if ball['localspeed'] >= 1.0:
                            ball['localspeed'] = 1.0
                            ball['freshlyspawned'] = False
##                    print(str(ball['rect'].left))
##                    print(str(ball['rect'].top))

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
                    if ball['direction'] == DOWNLEFT or ball['direction'] == DOWNRIGHT:
                        ball['angle'] = 90 - 80 * ( ( abs(ball['rect'].centerx-paddle.centerx) ) / float(paddle.width/2 + BALLSIZE/2) )
                        if ball['angle'] > 88:
                            ball['angle'] = 88
                        elif ball['angle'] < 10:
                            ball['angle'] = 10
                        if ball['rect'].centerx-paddle.centerx > 0:
                            ball['direction'] = UPRIGHT
                        else:
                            ball['direction'] = UPLEFT
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
            iterationsLeft -= 1
            if iterationsLeft <= 0:
                collisionsResolved = True
                
        # frametime check 2
        if DEBUGMODE:
            fontSlot = 10
            statsSurface.fill(GREEN, pygame.Rect(fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, WINDOWWIDTH-PLAYFIELDSIZE, defaultFontSize))
            drawText(str(pygame.time.get_ticks()), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
            
        # playfield drawing
        playfield.fill(WHITE)
        pygame.draw.rect(playfield, GREY, paddle)
        for ball in balls:
            pygame.draw.rect(playfield, RED, ball['rect'])
        window.blit(playfield, playfieldTopLeftCorner)
        
        # statsSurface drawing
        fontSlot = 1
        statsSurface.fill(GREEN, pygame.Rect(fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, WINDOWWIDTH-PLAYFIELDSIZE, defaultFontSize * 2))
        drawText(str(score), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
        fontSlot = 2
        ElapsedTime = float(frame) / FPS * 1000
        drawText(displayElapsedTime(ElapsedTime), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
        if ballsUpdated:
            fontSlot = 3
            statsSurface.fill(GREEN, pygame.Rect(fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, WINDOWWIDTH-PLAYFIELDSIZE, defaultFontSize))
            drawText(str(len(balls)), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
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
            fontSlot = 8
            statsSurface.fill(GREEN, pygame.Rect(fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, WINDOWWIDTH-PLAYFIELDSIZE, defaultFontSize))
            drawText(str(FPSCLOCK.get_time()), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
            fontSlot = 11
            statsSurface.fill(GREEN, pygame.Rect(fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, WINDOWWIDTH-PLAYFIELDSIZE, defaultFontSize))
            drawText(str(pygame.time.get_ticks()), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
            fontSlot = 12
            statsSurface.fill(GREEN, pygame.Rect(fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, WINDOWWIDTH-PLAYFIELDSIZE, defaultFontSize))
            drawText(str(FPSCLOCK.get_rawtime()), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
            fontSlot = 13
            statsSurface.fill(GREEN, pygame.Rect(fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, WINDOWWIDTH-PLAYFIELDSIZE, defaultFontSize))
            drawText(str(balls[0]['angle']), statsSurface, fontValuesPositionX, defaultFontSize * fontSlot + fontMargin, BLACK)
        window.blit(statsSurface, statsSurfaceTopLeftCorner)

        # Updating the entire screen every frame is apparently inefficient.
        # I still do it here for the following reasons:
        #
        # According to the debug data, it only takes 1 ms of frametime on my
        # computer. I also tested it on an older machine, and even then, it
        # still only took 3 ms of frametime.
        #
        # I tried using the dirty rects method and it caused the shapes of
        # moving rects to glitch out and become deformed at framerates above
        # 30. At 30fps and below, the balls appear to look ok, but it also makes
        # the game quite a bit choppier, making it less fun to play.
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

