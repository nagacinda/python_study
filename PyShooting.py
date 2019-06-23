import pygame
import sys
import random
from time import sleep

BLACK = (0,0,0) #검은색 RGB값
padWidth = 480  #길이
padHeight = 640 #너비
rockImage = [
            './Resource/rock01.png', './Resource/rock02.png', './Resource/rock03.png', './Resource/rock04.png',
            './Resource/rock05.png',
            './Resource/rock06.png', './Resource/rock07.png', './Resource/rock08.png', './Resource/rock09.png',
            './Resource/rock10.png',
            './Resource/rock11.png', './Resource/rock12.png', './Resource/rock13.png', './Resource/rock14.png',
            './Resource/rock15.png',
            './Resource/rock16.png', './Resource/rock17.png', './Resource/rock18.png', './Resource/rock19.png',
            './Resource/rock20.png',
            './Resource/rock21.png', './Resource/rock22.png', './Resource/rock23.png', './Resource/rock24.png',
            './Resource/rock25.png',
            './Resource/rock26.png', './Resource/rock27.png', './Resource/rock28.png', './Resource/rock29.png',
            './Resource/rock30.png',
             ]

explosionSound = [
                 './Resource/explosion01.wav', './Resource/explosion02.wav', './Resource/explosion03.wav',
                 './Resource/explosion03.wav',
                 ]



def writeScore(count):
    global gamePad
    font = pygame.font.Font('./Resource/NanumGothic.ttf', 20)
    text = font.render('파괴한 운석수:' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))

def writePassed(count):
    global gamePad
    font = pygame.font.Font('./Resource/NanumGothic.ttf', 20)
    text = font.render('놓친 운석수:' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (350, 0))

def writeMessage(text):
    global gamePad, gameOverSound
    textfont = pygame.font.Font('./Resource/NanumGothic.ttf', 60)
    text = textfont.render(text, True, (255,0,0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos) #출력
    pygame.display.update()

    pygame.mixer.music.stop()
    gameOverSound.play()

    sleep(2)        #2초쉬고 게임실행
    pygame.mixer.music.play(-1)
    runGame()
    
def crash():
    global gamePad
    writeMessage('전투기 파괴')


def gameOver():
    global gamePad
    writeMessage('게임오버')


def drawObject(obj, x, y):
    global gamePad #전역변수설정
    gamePad.blit(obj, (x, y))   #그림그리기


def initGame(): #게임초기화
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound  #전역변수설정
    pygame.init()  #pygame 초기화
    gamePad = pygame.display.set_mode((padWidth, padHeight))    #창만들기
    pygame.display.set_caption('PyShooting')        #타이틀명

    background = pygame.image.load('./Resource/background.png')     #배경화면
    fighter = pygame.image.load('./Resource/fighter.png')       #전투기
    missile = pygame.image.load('./Resource/missile.png')       #미사일
    explosion = pygame.image.load('./Resource/explosion.png') #운석

    #배경음악 및 사운드
    pygame.mixer.music.load('./Resource/music.wav')
    pygame.mixer.music.play(-1)
    missileSound = pygame.mixer.Sound('./Resource/missile.wav')
    gameOverSound = pygame.mixer.Sound('./Resource/gameover.wav')
    
    clock = pygame.time.Clock() #시간가져오기

def runGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound   #전역변수설정

    fighterSize = fighter.get_rect().size       #비행기크기 가져오기
    fighterWidth = fighterSize[0]               #비행기크기 X크기
    fighterHeight = fighterSize[1]              #비행기크기 Y크기

    x = padWidth * 0.45 #비행기 X위치
    y = padHeight * 0.9 #비행기 Y위치
    fighterX = 0    #전투기 좌우 움직임값
    
    missileXY = [] #무기 좌표 리스트

    rock = pygame.image.load(random.choice(rockImage)) #운석랜덤하게 가져오기
    rockSize = rock.get_rect().size #운석크기
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroySound = pygame.mixer.Sound(random.choice(explosionSound)) #운석폭파사운드 메모리

    rockX = random.randrange(0, padWidth - rockWidth)  #운석 초기 X위치
    rockY = 0   #운석 초기 Y 위치 위에서시작
    rockSpeed = 2
    #rockSpeed = 20

    isShot = False    #맞았을때
    shotCount = 0       #맞은개수
    rockPassed = 0      #지나쳤을때

    onGame = False
    while not onGame:   #반복실행시키기 위한 문구
        for event in pygame.event.get():

            if event.type in [pygame.QUIT]: #게임종료
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                        
                #alt + f4로 
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_ALT and event.key == pygame.K_F4:
                    pygame.quit()
                    sys.exit()
                        
                if event.key == pygame.K_LEFT: #왼쪽으로 이동
                    fighterX -= 5 #왼쪽으로 5이동

                elif event.key == pygame.K_RIGHT: #오른쪽으로 이동
                    fighterX += 5 #오른쪽으로 5이동

                elif event.key == pygame.K_SPACE: #미사일 발사
                    missileSound.play()
                    missileX = x + fighterWidth / 2    #미사일은 전투기의 몸체 X좌표 가운데
                    missileY = y + fighterHeight       #미사일은 몸체 Y좌표
                    missileXY.append([missileX, missileY])


            if event.type in [pygame.KEYUP]:    #키값 올라오면 
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:   #화면끝으로 가면 못 움직임
                    fighterX = 0    #전투기 움직임 0





        #gamePad.fill(BLACK)

        """배경화면 그리기"""
        drawObject(background, 0, 0)   #배경화면 그리기

        """비행기 그리기"""
        x += fighterX       #비행기 움직이기
        if x < 0 :          #왼쪽 끝으로 움직이면
            x = 0
        elif x > padWidth - fighterWidth:   #오른쪽 끝으로 움직이면
            x = padWidth - fighterWidth

        if y < rockY + rockHeight:  #비행기 Y좌표가 운석의 좌표보다 적을때
            if (rockX > x and rockX < x + fighterWidth) or (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth) : #겹칠때
                crash()


        drawObject(fighter, x, y) #비행기 그리기
        
        """미사일 그리기"""
        if len(missileXY) != 0:     #미사일좌표값이 있으면
            for i, bxy in enumerate(missileXY): #미사일좌표값을 열거형으로 뽑아냄
                bxy[1] -= 10    #미사일 Y값을 10씩 줄임
                missileXY[i][1] = bxy[1] #미사일 좌표값을 대체

                #미사일이 운석을 맞추었을 경우
                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:   #겹치는지 안겹치는지 확인
                        missileXY.remove(bxy) #미사일 좌표값 삭제
                        isShot = True
                        shotCount += 1


                if bxy[1] <= 0: #미사일이 화면 바깥으로 넘어가면
                    try:
                        missileXY.remove(bxy)   #미사일 제거
                    except:
                        pass    #아니면 패스
            
        if len(missileXY) != 0: #미사일좌표값이 있으면 미사일 생성
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        """맞추면 스코어 올려주기"""
        writeScore(shotCount)

        """운석"""

        rockY += rockSpeed #프레임당 운석이동
        
        
        """운석을 놓쳤을때"""
        if rockY > padHeight:   #운석이 화면 밖으로 나가면 새로 그리기
            rock = pygame.image.load(random.choice(rockImage))  # 운석랜덤하게 가져오기
            rockSize = rock.get_rect().size  # 운석크기
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            destroySound = pygame.mixer.Sound(random.choice(explosionSound)) #운석폭파사운드 메모리
            
            rockX = random.randrange(0, padWidth - rockWidth)  # 운석 초기 X위치
            rockY = 0  # 운석 초기 Y 위치 위에서시작
            rockPassed += 1


        if rockPassed == 3 :    #3개 놓치면 게임오버
            gameOver()

        writePassed(rockPassed)

        """운석 맞췄을때"""
        if isShot:
            drawObject(explosion, rockX, rockY) #운석폭파되면 새로 운석그리기
            destroySound.play() #미리 생성되어 있던 운석폭파사운드 실행

            rock = pygame.image.load(random.choice(rockImage))  # 운석랜덤하게 가져오기
            rockSize = rock.get_rect().size  # 운석크기
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]

            rockX = random.randrange(0, padWidth - rockWidth)  # 운석 초기 X위치
            rockY = 0  # 운석 초기 Y 위치 위에서시작
            
            isShot = False
            
            
            rockSpeed += 0.2 #속도증가
            if rockSpeed >= 10: #속도증가 10까지만
                rockSpeed = 10
            



        drawObject(rock, rockX, rockY) #운석그리기

        pygame.display.update() #다시 그리기

        clock.tick(60) #초당 60번

    pygame.quit()


initGame()
runGame()



