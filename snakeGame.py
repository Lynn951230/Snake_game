import pygame
import time
import random
from datetime import datetime
from datetime import timedelta

# 게임판에 그릴 요소들을 정의한다.
def drawBackground():
    """화면에 배경을 칠한다."""
    rect = pygame.Rect((0,0), (screenWidth, screenHeight))
    pygame.draw.rect(screen, GRAY, rect)
def drawRectangle(posi, color):
    """화면에 직사각형 격자를 그린다."""
    rect = pygame.Rect((posi[0] * screenBlock, posi[1] * screenBlock), (screenBlock, screenBlock))
    pygame.draw.rect(screen, color, rect)

# 스네이크 게임의 기본 설정을 정의한다.
screenWidth = 600 # 스크린의 가로 길이
screenHeight = 600 # 스크린의 세로 길이
screenBlock = 40 # 스크린의 격자 크기
appleCount = 3 # 사과의 갯수
turnLength = timedelta(seconds = 0.2) # 한 턴의 길이

# 스네이크 게임에서 잘못된 설정이 있는지 확인한다.
if screenWidth / screenBlock % 1 != 0 or screenHeight / screenBlock % 1 != 0:
    print("격자 크기가 가로 길이와 세로 길이에 맞게 설정해주세요.")
    exit()
if appleCount > (screenHeight / screenBlock) * (screenWidth / screenBlock) / 4:
    print("사과가 너무 많습니다. 적절한 사과의 수로 설정해주세요.")
    exit()

# 색깔을 정의한다.
GRAY = 190, 190, 190
LIME = 0, 230, 0
GREEN = 0, 200, 0
RED = 255, 0, 0

# pygame을 초기화 한다.
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
drawBackground()
pygame.display.update()

# 데이터 모델을 정의한다.
class GameOverException(Exception):
    """게임 오버 예외"""
class VictoryException(Exception):
    """게임 승리 예외"""
    pass
class Snake:
    """뱀"""
    def __init__(self):
        '''I-1. 뱀 생성하기 : 뱀 위치의 x와 y좌표를 저장할 self.position 리스트 생성하기'''
        self.position = [(2,1),(1,1),(0,1)]
        self.direction = "east"

    def draw(self):
        """자기 자신 그리기""" 
        '''I-1. 뱀 생성하기 : drawRectangle(위치 튜플, 색) 함수를 이용해서 뱀의 머리 그려주기'''
        for x in range(len(self.position)):
            if x == 0:
                drawRectangle(self.position[x], GREEN)
            else:
                drawRectangle(self.position[x], LIME)

    def turn(self, direction):
        """90도 방향인지 확인 후 회전하기"""
        '''I-3. 뱀 방향 설정하기 : self.moveDirection을 매개변수인 direction으로 정해줍니다.'''
        self.direction = direction

    def move(self):
        """현재 방향으로 움직이기"""
        '''I-2. 뱀 움직이기 : Snake.position의 값을 Snake.direction의 방향으로 1만큼 이동시킵니다.'''
        '''I-3. 뱀 방향 설정하기 : 방향에 따라 움직이는 좌표 설정하기 '''
        if self.direction == "east":
            self.position.insert(0, (self.position[0][0]+1, self.position[0][1]))
        if self.direction == "west":
            self.position.insert(0, (self.position[0][0]-1, self.position[0][1]))
        if self.direction == "south":
            self.position.insert(0, (self.position[0][0], self.position[0][1]+1))
        if self.direction == "north":
            self.position.insert(0, (self.position[0][0], self.position[0][1]-1))
        self.position.pop(len(self.position)-1)
        if self.position[0][0]  > 14 or self.position[0][0] < 0:
            raise GameOverException
        elif self.position[0][1] > 14 or self.position[0][1] < 0:
            raise GameOverException
        for x in range(len(self.position)):
            if x > 0:
                if self.position[x] == self.position[0]:
                    raise GameOverException
    def grow(self):
        """성장하게 하기"""
        '''II-4. 뱀 성장하기 : Snake.position에 항목을 하나 추가합니다.'''
        a = len(self.position)-1
        if self.direction == "east":
            self.position.append((self.position[a][0]-1, self.position[a][1]))
        elif self.direction == "west":
            self.position.append((self.position[a][0]+1, self.position[a][1]))
        elif self.direction == "south":
            self.position.append((self.position[a][0], self.position[a][1]-1))
        elif self.direction == "north":
            self.position.append((self.position[a][0], self.position[a][1]+1))
        self.draw()


class Apple:
    """사과"""
    color = RED # 색
    def __init__(self):
        '''II-1. 사과 생성하기 : x와 y좌표를 저장할 self.position 변수 생성하기'''
        self.position = []
        for y in range(3):
            b = (random.randint(0,13), random.randint(0,13))
            if y == 0:
                self.position.append(b)
            else:
                for i in range(len(self.position)):
                    if self.position[i] == b:
                        b = (random.randint(0,13), random.randint(0,13))
                self.position.append(b)
        self.color = []
        for s in range(3):
            self.color.append(255)

    def draw(self):
        """자기 자신 그리기"""
        for w in range(len(self.position)):
            drawRectangle(self.position[w] , (self.color[w],0,0))
    def corrupt(self):
        """부패하기"""
        '''II-5. 사과 부패하기 : 사과의 색을 점점 어둡게 바꾸어 주세요'''
        for i in range(len(self.color)):
            self.color[i] -= 5


class Gameboard:
    """게임판"""
    def __init__(self):
        '''I-1. 뱀 생성하기 : Snake를 생성하여 self.snake로 정해줍니다.'''
        '''II-1. 사과 생성하기 : 사과 오브젝트를 저장할 self.apple리스트를 생성합니다.'''
        '''II-2. 사과 위치 설정하기 : 사과의 처음 위치를 Apple.appleReplace함수를 사용하여 설정합니다'''
        self.snake = Snake()
        self.apple = Apple()
        self.boardWidth = screenWidth / screenBlock # 게임판의 가로 길이
        self.boardHeight = screenHeight / screenBlock # 게임판의 세로 길이

    def draw(self):
        """자기 자신 그리기"""
        '''I-1. 뱀 생성하기 : Snake.draw()함수를 호출합니다.'''
        '''II-1. 사과 생성하기 : Apple.draw() 함수를 호출합니다.'''
        self.snake.draw()
        self.apple.draw()

    def appleReplace(self):
        """사과 새로 생성하기"""
        '''II-2. 사과 위치 설정하기 : 사과의 위치를 새로 정해줍니다.'''
        '''II-6. 게임 승리 만들기 : 사과를 생성할수 없을경우, 게임 끝내기.'''
        n = (random.randint(0,13), random.randint(0,13))
        for x in range(len(self.snake.position)):
            if self.snake.position[x] == n:
                n = (random.randint(0,13), random.randint(0,13))
                for y in range(len(self.snake.position)):
                    if self.snake.position[y] == n:
                        n = (random.randint(0,13), random.randint(0,13))
        for i in range(len(self.apple.position)):
            if self.apple.position[i] == n:
                n = (random.randint(0,13), random.randint(0,13))
                for s in range(len(self.apple.position)):
                    if self.apple.position[s] == n:
                        n = (random.randint(0,13), random.randint(0,13))
        self.apple.position.append(n)
        self.apple.color.append(255)
        self.apple.draw()

        

    def frame(self):
        """게임 한 턴 진행하기 (매 프레임마다 호출되는 함수)"""
        '''I-2. 뱀 움직이기 : Snake.move 함수를 호출합니다.'''
        '''I-4. 뱀 위치 확인하기 : 뱀이 벽 밖으로 나갔는지 확인합니다.'''
        '''II-2. 사과 먹기 : 사과의 위치와 뱀 머리의 위치가 같은지 확인하기'''
        '''II-5. 사과 부패하기 : 사과가 부패했을때 사과 새로 놓기'''
        self.snake.move()
        for i in range(len(self.apple.position)):
            if self.apple.position[i] == self.snake.position[0]:
                drawRectangle(self.apple.position[i] , GRAY)
                self.apple.position.pop(i)
                self.apple.color.pop(i)
                self.snake.grow()
                self.appleReplace()
        self.apple.corrupt()
        for y in range(len(self.apple.color)):
            if self.apple.color[y] == 0:
                self.apple.color.pop(y)
                self.apple.position.pop(y)
                self.appleReplace()

lastMovedTime = datetime.now() # 마지막으로 블록을 움직인 시간
gameLayer = Gameboard() # 게임보드 정의하기

# 게임을 진행한다.
while True:
    events = pygame.event.get() # 플레이어가 하는 이벤트 정의하기
    for event in events:
        # X 키를 눌렀을 시 게임 종료
        if event.type == pygame.QUIT: exit()

        # 화살표 키를 눌렀을 시 방향 변경
        key_event = pygame.key.get_pressed()
        if key_event[pygame.K_RIGHT]:
            direction = "east"
            gameLayer.snake.turn(direction)
            #if event.key in directionOnKey:
                #'''I-3. 뱀 방향 설정하기 : 이곳에서 Snake.turn함수를 호출합니다.'''       
        elif key_event[pygame.K_LEFT]:
            direction = "west"
            # Snake.turn()
            gameLayer.snake.turn(direction)
        elif key_event[pygame.K_DOWN]:
            direction = "south"
            # Snake.turn()
            gameLayer.snake.turn(direction)
        elif key_event[pygame.K_UP]:
            direction = "north"
            # Snake.turn()
            gameLayer.snake.turn(direction)
            # Snake.move()
    ''' ***매 turnLength마다 턴 진행*** '''
    if datetime.now() - lastMovedTime > turnLength:
        try:
            gameLayer.frame()
            lastMovedTime = datetime.now()
        except GameOverException:
            if gameLayer.snake.position[0][0]  > screenWidth or gameLayer.snake.position[0][0] < 0:
                raise GameOverException
            elif gameLayer.snake.position[0][1] > screenHeight or gameLayer.snake.position[0][1] < 0:
                raise GameOverException
            for x in range(len(gameLayer.snake.position)):
                if x > 0:
                    if gameLayer.snake.position[x] == gameLayer.snake.position[0]:
                        raise GameOverException
            exit()
        except VictoryException:
            exit()

    drawBackground() # 배경 그리기
    gameLayer.draw() # 게임판의 모든 요소 그리기
    pygame.display.update() # 스크린 업데이트하기